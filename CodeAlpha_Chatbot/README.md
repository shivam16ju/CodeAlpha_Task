# 🤖 AlphaBot: Basic Rule-Based Chatbot

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</div>

## 📌 Project Overview
This project is part of the **CodeAlpha Python Programming Internship**. The goal was to build a simple rule-based chatbot capable of accepting user inputs like greetings and goodbyes, and responding with predefined replies using basic `if-elif` logic.

## ✨ Key Features
- **Typing Effect Simulation**: AlphaBot uses a custom delayed-printing algorithm to simulate human-like typing speeds, creating a highly immersive terminal experience.
- **Input Sanitization**: Automatically strips whitespace and converts input to lowercase to ensure robust matching even if the user types erratically.
- **Graceful Error Handling**: Includes fallback rules for unrecognized inputs and safely handles keyboard interrupts (`Ctrl+C`) to exit cleanly.
- **Cross-Platform Compatibility**: Written with pure standard ASCII formatting to prevent `UnicodeEncodeError` crashes on standard Windows Command Prompts.

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/CodeAlpha_Chatbot.git
   cd CodeAlpha_Chatbot
   ```

2. **Run the Chatbot:**
   No external dependencies are required! Just run:
   ```bash
   python chatbot.py
   ```

---
*Built with ❤️ during the CodeAlpha Internship.*
