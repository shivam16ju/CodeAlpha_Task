# ⚙️ Auto-Master Pro: Task Automation Suite

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</div>

## 📌 Project Overview
This project is part of the **CodeAlpha Python Programming Internship**. The task was to automate a small, real-life repetitive task (choosing between organizing files, extracting emails, or scraping a webpage). 

Instead of picking just one, this project implements a **comprehensive 3-in-1 Unified Automation Suite** to demonstrate advanced Python scripting, object-oriented programming (OOP), and mastery of standard libraries.

## ✨ Key Features
- **Object-Oriented Design**: Built entirely around an `AutoMaster` class for clean, maintainable, and scalable architecture.
- **Tool 1: JPG Organizer (`os`, `shutil`)**: Automatically scans a directory and moves all `.jpg` files into a dedicated organized folder.
- **Tool 2: Email Extractor (`re`)**: Parses large text files and extracts all unique email addresses using Regular Expressions, saving them to a timestamped report.
- **Tool 3: Web Scraper (`requests`)**: Fetches live webpages and parses the HTML to extract the webpage title.
- **Ultimate Demo Mode**: Includes an automated demo function that instantly generates dummy files and tests all three tools simultaneously.

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/CodeAlpha_Automation_Tool.git
   cd CodeAlpha_Automation_Tool
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   python auto_master.py
   ```
   *(Select Option 4 from the menu to run the Ultimate Demo!)*

---
*Built with ❤️ during the CodeAlpha Internship.*
