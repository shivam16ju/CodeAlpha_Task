import os
import shutil
import re
import requests
from datetime import datetime

class AutoMaster:
    """A professional suite of automation tools for file management, data extraction, and web scraping."""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def print_header(self, title):
        print("\n" + "=" * 60)
        print(f" [***] {title.upper()} [***] ".center(60, " "))
        print("=" * 60)

    def print_success(self, msg):
        print(f"[+] SUCCESS: {msg}")

    def print_error(self, msg):
        print(f"[-] ERROR: {msg}")

    def print_info(self, msg):
        print(f"[*] INFO: {msg}")

    # ==========================================
    # TOOL 1: File Organizer (os, shutil)
    # ==========================================
    def organize_images(self, source_dir, target_dir=None):
        self.print_header("Image Organizer (JPG)")
        
        if not os.path.exists(source_dir):
            self.print_error(f"Source directory '{source_dir}' does not exist.")
            return

        if target_dir is None:
            target_dir = os.path.join(source_dir, "Organized_JPGs")

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            self.print_info(f"Created target directory: {target_dir}")

        moved_count = 0
        for filename in os.listdir(source_dir):
            # Identifying JPG files
            if filename.lower().endswith(('.jpg', '.jpeg')):
                source_path = os.path.join(source_dir, filename)
                target_path = os.path.join(target_dir, filename)
                
                # Prevent moving files if source is same as target
                if os.path.abspath(source_path) != os.path.abspath(target_path):
                    try:
                        shutil.move(source_path, target_path)
                        moved_count += 1
                        print(f"  -> Moved: {filename}")
                    except Exception as e:
                        self.print_error(f"Failed to move {filename}: {e}")

        self.print_success(f"Successfully moved {moved_count} JPG files to {target_dir}.")

    # ==========================================
    # TOOL 2: Email Extractor (re, file handling)
    # ==========================================
    def extract_emails(self, source_file, output_file=None):
        self.print_header("Email Extractor")
        
        if not os.path.exists(source_file):
            self.print_error(f"Source file '{source_file}' does not exist.")
            return

        if output_file is None:
            output_file = f"extracted_emails_{self.timestamp}.txt"

        # Regex pattern for matching standard email addresses
        email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        extracted_emails = set() # Use a set to automatically handle duplicates

        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                for line in f:
                    matches = email_pattern.findall(line)
                    extracted_emails.update(matches)
        except Exception as e:
            self.print_error(f"Failed to read source file: {e}")
            return

        if not extracted_emails:
            self.print_info("No emails found in the source file.")
            return

        try:
            # File handling - Writing results
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"--- Emails Extracted on {datetime.now()} ---\n\n")
                for email in sorted(extracted_emails):
                    f.write(email + '\n')
            self.print_success(f"Extracted {len(extracted_emails)} unique emails to {output_file}")
        except Exception as e:
            self.print_error(f"Failed to write output file: {e}")

    # ==========================================
    # TOOL 3: Webpage Title Scraper (requests, re)
    # ==========================================
    def scrape_title(self, url, output_file=None):
        self.print_header("Webpage Title Scraper")
        
        if not url.startswith('http'):
            url = 'https://' + url

        if output_file is None:
            output_file = f"scraped_titles_{self.timestamp}.txt"

        self.print_info(f"Fetching {url}...")
        
        try:
            # Using the required requests library
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            html = response.text
            
            # Use regex to extract the title tag content
            title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
            
            if title_match:
                title = title_match.group(1).strip()
                self.print_success(f"Found Title: '{title}'")
                
                # Append to file
                with open(output_file, 'a', encoding='utf-8') as f:
                    f.write(f"URL: {url}\nTitle: {title}\nDate: {datetime.now()}\n{'-'*40}\n")
                self.print_info(f"Saved result to {output_file}")
            else:
                self.print_error("No <title> tag found on the provided webpage.")
                
        except requests.RequestException as e:
            self.print_error(f"Network error while scraping webpage: {e}")
        except Exception as e:
            self.print_error(f"Failed to process webpage: {e}")

def main():
    bot = AutoMaster()
    
    while True:
        print("\n" + "=" * 60)
        print("          AUTO-MASTER PRO: TASK AUTOMATION SUITE          ")
        print("=" * 60)
        print(" Select an automation tool to run:")
        print("   1. [File] Organize JPG Files")
        print("   2. [Text] Extract Emails from Text File")
        print("   3. [Web]  Scrape Webpage Title")
        print("   4. [***]  Run ALL (The Ultimate Demo)")
        print("   5. [X]    Exit")
        print("=" * 60)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            source = input("Enter the path to the folder containing JPGs (or '.' for current dir): ").strip()
            bot.organize_images(source)
        
        elif choice == '2':
            source = input("Enter the path to the .txt file containing text: ").strip()
            bot.extract_emails(source)
            
        elif choice == '3':
            url = input("Enter the URL to scrape (e.g., python.org): ").strip()
            bot.scrape_title(url)
            
        elif choice == '4':
            print("\n--- PREPARING ULTIMATE DEMO ENVIRONMENT ---")
            demo_dir = "demo_folder"
            os.makedirs(demo_dir, exist_ok=True)
            
            # Create dummy JPGs
            with open(os.path.join(demo_dir, "test_image1.jpg"), "w") as f: f.write("dummy data")
            with open(os.path.join(demo_dir, "test_image2.jpg"), "w") as f: f.write("dummy data")
            
            # Create dummy text file with emails
            demo_txt = os.path.join(demo_dir, "sample_text.txt")
            with open(demo_txt, "w") as f: 
                f.write("Hello! You can reach HR at hr@codealpha.com or support@company.org. ")
                f.write("Also, my personal email is student123@gmail.com. Don't email fake@fake.")
                
            bot.print_success(f"Demo environment created at './{demo_dir}'")
                
            # Run all 3 automations
            bot.organize_images(demo_dir)
            bot.extract_emails(demo_txt, "demo_extracted_emails.txt")
            bot.scrape_title("https://www.python.org", "demo_scraped_titles.txt")
            
        elif choice == '5':
            print("\nExiting Auto-Master Pro. Have a great day!\n")
            break
        else:
            print("\n[!] Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
