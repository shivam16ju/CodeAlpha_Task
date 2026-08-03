import time

def print_slow(text, delay=0.03):
    """Simulates a typing effect for the chatbot's responses to make it feel alive."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def get_bot_response(user_input):
    """Contains the if-elif rules for the chatbot's predefined replies."""
    # Convert input to lowercase and remove extra spaces for easier matching
    cleaned_input = user_input.lower().strip()
    
    # Rule-based logic using if-elif as strictly required by the prompt
    if cleaned_input in ['hello', 'hi', 'hey', 'greetings', 'yo']:
        return "Hi there! I am AlphaBot. How can I assist you today?"
    
    elif cleaned_input in ['how are you', 'how are you?', 'how are you doing', 'how are things']:
        return "I'm just a simple Python script, but I'm doing fantastic! Thanks for asking. How are you?"
    
    elif cleaned_input in ['fine', 'good', 'great', 'doing well']:
        return "I'm glad to hear that!"
        
    elif 'name' in cleaned_input:
        return "My name is AlphaBot. I'm a basic rule-based chatbot built for the CodeAlpha internship."
        
    elif 'weather' in cleaned_input:
        return "I don't have internet access yet, but it's always 100% sunny inside my code!"
        
    elif 'joke' in cleaned_input:
        return "Why do Python programmers prefer dark mode? Because light attracts bugs!"
        
    elif 'help' in cleaned_input:
        return "I can respond to basic greetings, tell you my name, tell a programming joke, or say goodbye. Try saying 'hello'!"
        
    elif cleaned_input in ['bye', 'goodbye', 'exit', 'quit']:
        return "Goodbye! Have a great day!"
        
    else:
        # Fallback response for unknown inputs
        return "I'm sorry, my rules don't cover that yet. Type 'help' to see what I can understand!"

def run_chat():
    """Main loop for the chat interface."""
    print("\n" + "=" * 50)
    print(" " * 15 + "[O_O] ALPHABOT [O_O]")
    print("=" * 50)
    print_slow("AlphaBot: System initialized. Type 'bye' or 'exit' to quit.\n")
    
    # Infinite loop to keep the chat running
    while True:
        try:
            # Get user input
            user_input = input("You: ")
            
            # Prevent empty inputs from being processed
            if not user_input.strip():
                continue
            
            # Check if the user wants to quit
            if user_input.lower().strip() in ['bye', 'goodbye', 'exit', 'quit']:
                print("AlphaBot: ", end="")
                print_slow(get_bot_response('bye'))
                break
                
            # Get the predefined bot response
            response = get_bot_response(user_input)
            
            # Print response with simulated typing effect
            print("AlphaBot: ", end="")
            print_slow(response)
            print("-" * 50) # Divider for readability
            
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\nAlphaBot: ", end="")
            print_slow("Force quit detected. Goodbye!")
            break

if __name__ == "__main__":
    run_chat()
