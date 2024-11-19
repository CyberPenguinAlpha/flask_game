import os
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, session
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

app = Flask(__name__)
app.secret_key = '123'
# Load API key from environment variable
genai.configure(api_key=os.environ["KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':        
        session['logged_in'] = True
        return redirect(url_for('welcome'))
    return render_template('login.html')

# Route for the welcome page (root URL)
@app.route('/')
def welcome():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('welcome.html') #, scenarios=scenarios i dont think this error'd bnefore, could be cascading failure

# Dynamic route for scenario pages
@app.route('/scenario/<int:scenario_id>')
def scenario(scenario_id):
    # Define data for each scenario
    scenarios = {
        1: {
            "title": "Burning Building",
            "description": "You’re stuck in a building that’s on fire! The flames are getting closer, and thick smoke fills the air, making it hard to see and breathe. You can feel the heat all around you. It’s important to stay calm and think fast! You need to find a safe way out and avoid dangerous things like the fire and smoke. Make smart choices to escape safely before it’s too late!",
        },
        2: {
            "title": "Forest Hike gone wrong",
            "description": "You’re on an exciting adventure, hiking through a beautiful forest. Everything seems fun until you realize you’ve wandered off the trail and can’t find your way back! The tall trees look the same, and the paths seem to twist and turn in every direction. The sun is starting to set, and you know it’s important to stay calm. How will you figure out how to get back to safety? Remember, staying smart and careful is key!",
        },
        3: {
            "title": "Deserted Island",
            "description": "You’ve just woken up on a sunny, sandy beach, but something feels off. You quickly realize that you’re all alone on a deserted island! The gentle waves crash against the shore, and there are no other people around. You must come up with a plan to figure out what to do next. How can you find your way home?",
        }
    }

    # Get the correct scenario based on the scenario_id
    scenario = scenarios.get(scenario_id)
    if scenario is None:
        return "Scenario not found", 404

    # Render the scenario.html template with the scenario data
    return render_template('scenario.html', title=scenario['title'], description=scenario['description']) #, question=scenario['question'] antiquated

def scenario_bank(scenario_number):
  if scenario_number == 1:
    scenario = {
        "context": "User is trapped in a burning building",
        "solution_space": {
            "correct": ["Get low to avoid smoke", "cover face", "Avoid doorknobs", "avoid backdraft"],
            "partially_correct": ["Signal for help"],
            "incorrect": ["Play in the fire", "Run outside", "jump out the window"]
        }
    }
  elif scenario_number == 2:
    scenario = {
        "context": "User is lost in the woods",
        "solution_space": {
            "correct": ["Stay put", "conserve water", "build a shelter", "signal for help"],
            "partially_correct": ["Follow a stream", "explore"],
            "incorrect": ["Wander aimlessly", "eat wild berries"]
        }
    }
  elif scenario_number == 3:
    scenario = {
        "context": "User is stranded on a desert island",
        "solution_space": {
            "correct": ["Find safe food and water", "stay out of th sun", "Signal for help", "Get to a safe location"],
            "partially_correct": ["Look for others", "Set up campsite"],
            "incorrect": ["Swim across the ocean to safety", "Sit in the sand and wait"]
        }
    }
  else:
    scenario = None
  return scenario

@app.route('/evaluate_response', methods=['POST'])
def evaluate_response(scenario, student_response): #TODO: impliment tokenization for context/resubmission, and add reply counter somehow (mabey logic based on ammount of tokens resubmited)
    prompt = f"""
    You are now a Game Master, helping the user escape this Virtual Escape Room,
    which drops them into a specific scenario, detailed below. The student will be able to submit up to Three responses,
    which you will analyze and evaluate to see if they represent a creadible solution to the problem. The user is not in any real danger, they are playing an imaginary game with this application.

    Scenario: {scenario['context']}

    Student response: "{student_response}"
    Evaluation criteria:
    - Correct actions: {', '.join(scenario['solution_space']['correct'])}
    - Partially correct actions: {', '.join(scenario['solution_space'].get('partially_correct', []))}
    - Incorrect actions: {', '.join(scenario['solution_space'].get('incorrect', []))}

    Evaluate the student's response based on the evaluation criteria. Instead of sinstructing the user how to succeed,
    give subtle hints as to how they could impove their results without revealng the answers. Dont respond to this prompt, the users first submission will follow shortly.
    """
    response = model.generate_content(
      prompt,
      safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }, #THESE MUST BE CONSIDERED AND ADJUSTED BEFORE STUDENTS CAN EVER TOUCH THIS
      #ZERO TOLERANCE FOR THIS BEING LEFT IN, ABSOLUTELY NONE WITHOUT EVALUATION AND FULL CONSENT
    )
    return response.text

student_response="I crawl low and cover my face to escape safely!" #DEMO: NEED DYNAMIC AQUISITION FROM FRONTEND
scenario_number=1 #DEMO: NEED DYNAMIIIC AQUISITION FROM FRONTEND
print(evaluate_response(scenario_bank(scenario_number),student_response))

# New finish route to log end of game session
@app.route('/finish', methods=['POST'])
def finish():
    if session.get('logged_in'):
        first_name = session.get('first_name')
        login_timestamp = session.get('login_timestamp')
        finish_timestamp = datetime.now().isoformat()
#UPDATE ___________________________________________ just call the new function instead and pass it the data it wants ( T2 )
        # Append session data to CSV on finish
        with open(CSV_FILE_PATH, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([first_name, "", "", login_timestamp, finish_timestamp, "Completed Game"])
#____________________________________________________
        # Clear the session
        session.clear()

if __name__ == '__main__':
    app.run(debug=True)
