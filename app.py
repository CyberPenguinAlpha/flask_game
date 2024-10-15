from flask import Flask, render_template

app = Flask(__name__)

# Dictionary to store scenarios
scenarios = {
    1: {
        "title": "The Lost Forest Path",
        "description": "You are in a magical forest, and you've wandered off the path while chasing a glowing butterfly. Now you're lost! Around you are tall trees, and you can hear strange rustling noises. To find your way back, you need to solve three riddles from the talking animals who live in the forest. A squirrel asks, 'What has roots as nobody sees, and is taller than trees?' Solve this and follow the direction the squirrel gives you to find your way back to the main trail.",
        "question": "How do you solve the riddle and safely find your way back to the path?"
    },
    2: {
        "title": "The Mystery of the Hidden Treasure",
        "description": "You’re an explorer in a pirate’s cove, and you’ve just found a mysterious map. It shows a secret treasure hidden deep in the caves, but it’s guarded by a clever parrot who loves puzzles. The parrot tells you, 'To find the treasure, you need to find three colored stones hidden in the cave. The red stone is hidden where water drips, the blue stone is hidden under a glowing rock, and the yellow stone is where bats sleep.' Collect all three stones, and the parrot will reveal the location of the treasure.",
        "question": "How do you find the three stones, and what will you do to solve the parrot's puzzle?"
    },
    3: {
        "title": "Escape from the Wizard's Castle",
        "description": "You’ve accidentally entered a mysterious wizard's castle, and the door has locked behind you! The wizard will let you leave only if you can figure out the secret spell to unlock the door. There are four potion bottles on the table. One of them will make the key appear. The bottles are labeled with symbols: a star, a moon, a sun, and a lightning bolt. A friendly mouse whispers, 'The symbol you need is connected to something that appears in the sky only during the day.'",
        "question": "Which potion do you drink to unlock the door and escape the castle?"
    }
}

# Welcome page route
@app.route('/')
def welcome():
    return render_template('welcome.html')

# Scenario route (dynamically handles different scenarios)
@app.route('/scenario/<int:scenario_id>')
def scenario(scenario_id):
    scenario = scenarios.get(scenario_id, None)
    if scenario:
        return render_template('scenario.html', title=scenario['title'], description=scenario['description'], question=scenario['question'])
    else:
        return "Scenario not found.", 404

if __name__ == "__main__":
    app.run(debug=True)
