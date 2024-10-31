import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load API key from environment variable
genai.configure(api_key=os.environ.get("KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")
# Route for the welcome page (root URL)
@app.route('/')
def welcome():
    return render_template('welcome.html')

# Dynamic route for scenario pages
@app.route('/scenario/<int:scenario_id>')
def scenario(scenario_id):
    # Define data for each scenario
    scenarios = {
        1: {
            "title": "Burning Building",
            "description": "You’re stuck in a building that’s on fire! The flames are getting closer, and thick smoke fills the air...",
            "question": "What actions will you take to stay safe and find a way out?"
        },
        2: {
            "title": "Forest Hike Gone Wrong",
            "description": "You’re on an exciting adventure, hiking through a beautiful forest. Everything seems fun until you realize you’ve wandered off...",
            "question": "What steps will you take to find your way back to safety?"
        },
        3: {
            "title": "Deserted Island",
            "description": "You’ve just woken up on a sunny, sandy beach, but something feels off...",
            "question": "How will you survive and find a way back home?"
        }
    }

    # Get the correct scenario based on the scenario_id
    scenario = scenarios.get(scenario_id)
    if scenario is None:
        return "Scenario not found", 404

    # Render the scenario.html template with the scenario data
    return render_template('scenario.html', title=scenario['title'], description=scenario['description'], question=scenario['question'])

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
    give subtle hints as to how they could impove their results without revealng the answers.
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
#TODO: loging in external JSON file (needs to be reconfigured to store all responses, mabey just append a conversation log text file within each? figure out how JSON's work ig)
#---------------------------
if __name__ == '__main__':
    app.run(debug=True)
