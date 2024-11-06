from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "your_fallback_secret_key")

# Configure the OpenAI API key
genai.configure(api_key=os.environ.get("KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Define the scenarios
scenarios = {
    1: {
        "title": "The Forest Path",
        "description": "You’re lost in the woods and must find your way back.",
        "question": "What steps will you take to find your way back to safety?"
    },
    2: {
        "title": "The Mystery of the Hidden Treasure",
        "description": "You’re on a treasure hunt and must solve clues to find the hidden treasure.",
        "question": "How will you solve the mystery to uncover the treasure?"
    },
    3: {
        "title": "Escape from the Wizard's Castle",
        "description": "You’re trapped in a castle with magical traps. Find a way to escape!",
        "question": "What actions will you take to navigate the traps and escape?"
    }
}

# CSV path
CSV_FILE_PATH = "user_data.csv"

# Function to provide context and evaluation criteria for each scenario
def scenario_bank(scenario_number):
    if scenario_number == 1:
        return {
            "context": "User is lost in the woods and must find their way back.",
            "solution_space": {
                "correct": ["Stay put", "conserve water", "build a shelter", "signal for help"],
                "partially_correct": ["Follow a stream", "explore cautiously"],
                "incorrect": ["Wander aimlessly", "eat unknown wild berries"]
            }
        }
    elif scenario_number == 2:
        return {
            "context": "User is on a treasure hunt and needs to solve clues to find the hidden treasure.",
            "solution_space": {
                "correct": ["Analyze the clues carefully", "stay alert", "follow the map"],
                "partially_correct": ["Look for landmarks", "seek help if available"],
                "incorrect": ["Ignore clues", "rush without thinking"]
            }
        }
    elif scenario_number == 3:
        return {
            "context": "User is trapped in a wizard's castle with magical traps and must find a way to escape.",
            "solution_space": {
                "correct": ["Stay calm", "look for hidden doors", "avoid dangerous areas"],
                "partially_correct": ["Examine surroundings carefully", "try spells cautiously"],
                "incorrect": ["Touch everything without caution", "panic and run around"]
            }
        }
    else:
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_initial = request.form['last_initial']
        grade_level = request.form['grade_level']
        login_timestamp = datetime.now().isoformat()

        # Log user login in CSV
        with open(CSV_FILE_PATH, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([first_name, last_initial, grade_level, login_timestamp, "", "Login"])

        # Store user info in session
        session['logged_in'] = True
        session['first_name'] = first_name
        return redirect(url_for('welcome'))

    return render_template('login.html')

@app.route('/')
def welcome():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('welcome.html', scenarios=scenarios)

# Route to handle each scenario selection
@app.route('/scenario/<int:scenario_id>')
def scenario(scenario_id):
    scenario = scenarios.get(scenario_id)
    if scenario is None:
        return "Scenario not found", 404
    return render_template('scenario.html', scenario_id=scenario_id, title=scenario['title'], description=scenario['description'], question=scenario['question'])

@app.route('/get_hint', methods=['POST'])
def get_hint():
    data = request.get_json()
    user_input = data.get("user_input")
    scenario_id = int(data.get("scenario"))
    scenario_data = scenario_bank(scenario_id)

    if scenario_data is None:
        return jsonify({"error": "Scenario not found"}), 404

    prompt = f"""
    Scenario: {scenario_data['context']}
    Student response: "{user_input}"
    Evaluation criteria:
    - Correct actions: {', '.join(scenario_data['solution_space']['correct'])}
    - Partially correct actions: {', '.join(scenario_data['solution_space'].get('partially_correct', []))}
    - Incorrect actions: {', '.join(scenario_data['solution_space'].get('incorrect', []))}
    Provide feedback: if the response is correct, encourage them; if partially correct, give hints; if incorrect, guide them subtly.
    """

    response = model.generate_content(prompt, safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    })
    # Parse the response from the model
    if response and response.text:
        hint_and_score = response.text.strip()
    else:
        hint_and_score = "Couldn't generate a hint or score at this time."
    return jsonify({"hint_and_score": hint_and_score})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
