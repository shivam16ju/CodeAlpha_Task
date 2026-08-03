from flask import Flask, render_template, request, jsonify, session
import random
import os

app = Flask(__name__)
# Secure random key for session management
app.secret_key = os.urandom(24)

WORDS = ["ALGORITHM", "ENCRYPTION", "DATABASE", "PYTHON", "NETWORK"]
MAX_GUESSES = 6

def init_game():
    session['word'] = random.choice(WORDS)
    session['guessed_letters'] = []
    session['incorrect_guesses'] = 0

@app.route('/')
def index():
    # Initialize a new game when loading the page if one doesn't exist
    if 'word' not in session:
        init_game()
    return render_template('index.html')

@app.route('/api/state')
def get_state():
    if 'word' not in session:
        init_game()
    
    word = session['word']
    guessed = session['guessed_letters']
    incorrect = session['incorrect_guesses']
    
    display_word = [letter if letter in guessed else "_" for letter in word]
    is_won = "_" not in display_word
    is_lost = incorrect >= MAX_GUESSES
    
    return jsonify({
        "display_word": display_word,
        "guessed_letters": guessed,
        "incorrect_guesses": incorrect,
        "max_guesses": MAX_GUESSES,
        "status": "won" if is_won else ("lost" if is_lost else "playing"),
        "answer": word if is_lost else None
    })

@app.route('/api/guess', methods=['POST'])
def guess():
    if 'word' not in session:
        init_game()
        
    data = request.json
    letter = data.get('letter', '').upper()
    
    if not letter.isalpha() or len(letter) != 1:
        return jsonify({"error": "Invalid guess"}), 400
        
    guessed = session['guessed_letters']
    incorrect = session['incorrect_guesses']
    
    # Don't process if game is over
    word = session['word']
    is_won = all(l in guessed for l in word)
    is_lost = incorrect >= MAX_GUESSES
    if is_won or is_lost:
        return get_state()
        
    if letter not in guessed:
        guessed.append(letter)
        if letter not in session['word']:
            session['incorrect_guesses'] += 1
        session.modified = True
            
    return get_state()

@app.route('/api/reset', methods=['POST'])
def reset():
    init_game()
    return get_state()

if __name__ == '__main__':
    app.run(debug=True)
