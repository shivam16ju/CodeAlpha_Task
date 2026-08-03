document.addEventListener('DOMContentLoaded', () => {
    const wordDisplay = document.getElementById('wordDisplay');
    const keyboard = document.getElementById('keyboard');
    const statusMessage = document.getElementById('statusMessage');
    const resetBtn = document.getElementById('resetBtn');
    
    // Create keyboard layout
    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split('');
    letters.forEach(letter => {
        const button = document.createElement('button');
        button.className = 'key';
        button.textContent = letter;
        button.id = `key-${letter}`;
        button.addEventListener('click', () => makeGuess(letter));
        keyboard.appendChild(button);
    });

    // Handle physical keyboard input
    document.addEventListener('keydown', (e) => {
        const letter = e.key.toUpperCase();
        if (letters.includes(letter)) {
            const btn = document.getElementById(`key-${letter}`);
            if (btn && !btn.disabled) {
                makeGuess(letter);
            }
        }
    });

    resetBtn.addEventListener('click', resetGame);

    // Initial load
    fetchState();

    async function fetchState() {
        try {
            const res = await fetch('/api/state');
            const data = await res.json();
            updateUI(data);
        } catch (error) {
            console.error("Error fetching state:", error);
        }
    }

    async function makeGuess(letter) {
        try {
            const res = await fetch('/api/guess', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ letter })
            });
            const data = await res.json();
            updateUI(data);
        } catch (error) {
            console.error("Error making guess:", error);
        }
    }

    async function resetGame() {
        try {
            const res = await fetch('/api/reset', { method: 'POST' });
            const data = await res.json();
            
            // Reset UI animations
            document.querySelectorAll('.body-part').forEach(part => {
                part.classList.remove('visible');
            });
            
            updateUI(data);
        } catch (error) {
            console.error("Error resetting game:", error);
        }
    }

    function updateUI(data) {
        // Update Word Display
        wordDisplay.innerHTML = '';
        data.display_word.forEach(char => {
            const span = document.createElement('span');
            span.className = 'letter-box';
            if (char !== '_') {
                span.textContent = char;
                span.classList.add('revealed');
            } else {
                span.textContent = '';
            }
            wordDisplay.appendChild(span);
        });

        // Update Keyboard
        document.querySelectorAll('.key').forEach(btn => {
            const letter = btn.textContent;
            if (data.guessed_letters.includes(letter)) {
                btn.disabled = true;
                // Check if it was correct or incorrect
                if (data.display_word.includes(letter) || (data.answer && data.answer.includes(letter))) {
                    btn.classList.add('correct');
                } else {
                    btn.classList.add('incorrect');
                }
            } else {
                btn.disabled = false;
                btn.classList.remove('correct', 'incorrect');
            }
        });

        // Update Hangman Drawing
        for (let i = 1; i <= 6; i++) {
            const part = document.getElementById(`part-${i}`);
            if (i <= data.incorrect_guesses) {
                part.classList.add('visible');
            } else {
                part.classList.remove('visible');
            }
        }

        // Update Status
        if (data.status === 'won') {
            statusMessage.textContent = '🌟 You Won! Brilliant! 🌟';
            statusMessage.style.color = 'var(--success)';
            disableKeyboard();
        } else if (data.status === 'lost') {
            statusMessage.textContent = `💀 Game Over! The word was ${data.answer}`;
            statusMessage.style.color = 'var(--error)';
            disableKeyboard();
        } else {
            statusMessage.textContent = `${data.max_guesses - data.incorrect_guesses} guesses remaining`;
            statusMessage.style.color = 'var(--text-muted)';
        }
    }

    function disableKeyboard() {
        document.querySelectorAll('.key').forEach(btn => {
            btn.disabled = true;
        });
    }
});
