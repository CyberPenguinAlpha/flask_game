import openai
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

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
            "title": "The Forest Path",
            "description": "You are in a magical forest, and you've wandered off the path while chasing a glowing butterfly. Now you're lost!",
            "question": "How do you solve the riddle and safely find your way back to the path?"
        },
        2: {
            "title": "The Mystery of the Hidden Treasure",
            "description": "You’re an explorer in a pirate’s cove, and you’ve just found a mysterious map.",
            "question": "How do you find the three stones and solve the parrot's puzzle?"
        },
        3: {
            "title": "Escape from the Wizard's Castle",
            "description": "You’ve accidentally entered a mysterious wizard's castle, and the door has locked behind you!",
            "question": "Which potion do you drink to unlock the door and escape the castle?"
        }
    }

    # Get the correct scenario based on the scenario_id
    scenario = scenarios.get(scenario_id)
    if scenario is None:
        return "Scenario not found", 404

    # Render the scenario.html template with the scenario data
    return render_template('scenario.html', title=scenario['title'], description=scenario['description'], question=scenario['question'])

# Route to get a hint or help based on user input
@app.route('/get_hint', methods=['POST'])
def get_hint():
    user_input = request.json.get('user_input')
    scenario = request.json.get('scenario')

    messages = [
        {"role": "system", "content": f"This is a game scenario: {scenario}. Provide helpful hints to the user."},
        {"role": "user", "content": user_input}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or use "gpt-4" if you're using GPT-4
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        hint = response['choices'][0]['message']['content'].strip()
        return jsonify({'hint': hint})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)