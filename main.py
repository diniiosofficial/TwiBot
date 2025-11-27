#!/usr/bin/env python3
import os
import sys
import subprocess
import venv
import time
import random
import string
from datetime import datetime

# ===== VIRTUAL ENVIRONMENT SETUP =====
def setup_environment():
    """Create virtual environment and install packages"""
    print("🔧 Setting up virtual environment...")
    
    # Create venv if it doesn't exist
    if not os.path.exists("venv"):
        print("📁 Creating virtual environment...")
        venv.create("venv", with_pip=True)
    
    # Get paths
    if sys.platform.startswith('win'):
        python_path = os.path.join("venv", "Scripts", "python.exe")
        pip_path = os.path.join("venv", "Scripts", "pip.exe")
    else:
        python_path = os.path.join("venv", "bin", "python")
        pip_path = os.path.join("venv", "bin", "pip")
    
    # Install required packages
    packages = [
        "selenium", 
        "telethon", 
        "requests", 
        "beautifulsoup4", 
        "cryptography"
    ]
    
    print("📦 Installing packages in virtual environment...")
    for package in packages:
        try:
            subprocess.run([pip_path, "install", package], check=True, capture_output=True)
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"⚠️ Failed to install {package}")
    
    return python_path

# ===== MAIN BOT =====
class AutoTwitterBot:
    def __init__(self):
        self.api_id = 36522969
        self.api_hash = '8fe00a5f086cbfd9b2688b5848bd14c5'
        self.phone = '+919043785587'
        self.accounts_file = 'twitter_accounts.txt'
        
    def generate_details(self):
        """Generate random account details"""
        first_names = ['John', 'Mike', 'David', 'Chris', 'Alex', 'James', 'Robert', 'Daniel']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis']
        
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        email = f"{username}@telegmail.com"
        password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%", k=12))
        
        # Random DOB (18-25 years old)
        current_year = datetime.now().year
        birth_year = random.randint(current_year-25, current_year-18)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)
        
        return name, username, email, password, birth_day, birth_month, birth_year

    def setup_browser(self):
        """Setup Chrome browser for automation"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            
            print("🌐 Setting up browser...")
            
            # Setup Chrome options
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Auto-download and setup ChromeDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Remove automation flags
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            
            return driver
            
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return None

    def click_create_account(self, driver):
        """Click the Create Account button"""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        print("🖱️ Looking for Create Account button...")
        
        # Wait for page to load
        time.sleep(5)
        
        # Try different selectors for Create Account button
        selectors = [
            "//span[contains(text(), 'Create account')]",
            "//span[contains(text(), 'Sign up')]",
            "//a[contains(@href, 'signup')]",
            "//button[contains(text(), 'Sign up')]",
            "//div[contains(text(), 'Create account')]",
            "//button[@data-testid='signupButton']"
        ]
        
        for selector in selectors:
            try:
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                driver.execute_script("arguments[0].click();", button)
                print("✅ Clicked Create Account button!")
                return True
            except:
                continue
        
        # If no button found, try JavaScript click
        try:
            driver.execute_script("window.location.href = 'https://x.com/i/flow/signup'")
            time.sleep(3)
            return True
        except:
            print("❌ Could not find Create Account button")
            return False

    def fill_signup_form(self, driver, name, email, day, month, year, username, password):
        """Fill the entire signup form automatically"""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        print("📝 Filling signup form...")
        
        try:
            # Wait for form to load
            time.sleep(5)
            
            # Fill name field
            name_fields = driver.find_elements(By.XPATH, "//input[@name='name']")
            if not name_fields:
                name_fields = driver.find_elements(By.XPATH, "//input[@type='text']")
            
            for field in name_fields:
                try:
                    field.clear()
                    field.send_keys(name)
                    print(f"✅ Name entered: {name}")
                    break
                except:
                    continue
            
            time.sleep(2)
            
            # Fill email field
            email_fields = driver.find_elements(By.XPATH, "//input[@type='email']")
            for field in email_fields:
                try:
                    field.clear()
                    field.send_keys(email)
                    print(f"✅ Email entered: {email}")
                    break
                except:
                    continue
            
            time.sleep(2)
            
            # Handle date of birth
            self.fill_date_of_birth(driver, day, month, year)
            time.sleep(2)
            
            # Click Next button
            self.click_next_button(driver)
            time.sleep(5)
            
            # Fill username in next step
            username_fields = driver.find_elements(By.XPATH, "//input[@name='username']")
            for field in username_fields:
                try:
                    field.clear()
                    field.send_keys(username)
                    print(f"✅ Username entered: {username}")
                    break
                except:
                    continue
            
            time.sleep(2)
            self.click_next_button(driver)
            time.sleep(5)
            
            # Fill password
            password_fields = driver.find_elements(By.XPATH, "//input[@type='password']")
            for field in password_fields:
                try:
                    field.clear()
                    field.send_keys(password)
                    print("✅ Password entered")
                    break
                except:
                    continue
            
            time.sleep(2)
            
            # Final signup
            self.click_signup_button(driver)
            
            return True
            
        except Exception as e:
            print(f"❌ Form filling error: {e}")
            return False

    def fill_date_of_birth(self, driver, day, month, year):
        """Fill date of birth fields"""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import Select
        
        try:
            # Find all dropdowns
            dropdowns = driver.find_elements(By.TAG_NAME, "select")
            
            if len(dropdowns) >= 3:
                # Month
                month_select = Select(dropdowns[0])
                month_select.select_by_value(str(month))
                time.sleep(1)
                
                # Day
                day_select = Select(dropdowns[1])
                day_select.select_by_value(str(day))
                time.sleep(1)
                
                # Year
                year_select = Select(dropdowns[2])
                year_select.select_by_value(str(year))
                time.sleep(1)
                
                print(f"✅ DOB set: {day}/{month}/{year}")
            else:
                print("⚠️ Could not find DOB dropdowns")
                
        except Exception as e:
            print(f"⚠️ DOB setup failed: {e}")

    def click_next_button(self, driver):
        """Click Next button"""
        from selenium.webdriver.common.by import By
        
        next_selectors = [
            "//span[contains(text(), 'Next')]",
            "//button[contains(text(), 'Next')]",
            "//div[contains(text(), 'Next')]",
            "//button[@data-testid='nextButton']"
        ]
        
        for selector in next_selectors:
            try:
                buttons = driver.find_elements(By.XPATH, selector)
                for button in buttons:
                    try:
                        driver.execute_script("arguments[0].click();", button)
                        print("✅ Clicked Next")
                        return True
                    except:
                        continue
            except:
                continue
        return False

    def click_signup_button(self, driver):
        """Click final Signup button"""
        from selenium.webdriver.common.by import By
        
        signup_selectors = [
            "//span[contains(text(), 'Sign up')]",
            "//button[contains(text(), 'Sign up')]",
            "//button[@data-testid='signupButton']"
        ]
        
        for selector in signup_selectors:
            try:
                buttons = driver.find_elements(By.XPATH, selector)
                for button in buttons:
                    try:
                        driver.execute_script("arguments[0].click();", button)
                        print("✅ Final signup clicked!")
                        return True
                    except:
                        continue
            except:
                continue
        return False

    def save_account(self, username, email, password):
        """Save account to file"""
        try:
            with open(self.accounts_file, 'a') as f:
                f.write(f"{username} | {email} | {password} | {datetime.now()}\n")
            print("✅ Account saved to file!")
        except Exception as e:
            print(f"❌ Save error: {e}")

    def run_automation(self):
        """Main automation function"""
        print("🚀 STARTING FULLY AUTOMATIC TWITTER SIGNUP")
        print("="*50)
        
        # Generate account details
        name, username, email, password, day, month, year = self.generate_details()
        
        print(f"\n🎲 GENERATED ACCOUNT:")
        print(f"👤 Name: {name}")
        print(f"📧 Email: {email}") 
        print(f"🔑 Password: {password}")
        print(f"🆔 Username: {username}")
        print(f"🎂 DOB: {day}/{month}/{year}")
        
        # Setup browser
        driver = self.setup_browser()
        if not driver:
            return False
        
        try:
            # Open Twitter signup page
            print("🌐 Opening Twitter signup page...")
            driver.get("https://x.com/i/flow/signup")
            time.sleep(5)
            
            # Click Create Account button
            if not self.click_create_account(driver):
                return False
            
            # Fill the entire form automatically
            if not self.fill_signup_form(driver, name, email, day, month, year, username, password):
                return False
            
            print("⏳ Waiting for verification step...")
            time.sleep(10)
            
            # Save account details
            self.save_account(username, email, password)
            
            print("\n🎊 ACCOUNT CREATION INITIATED!")
            print("📧 Check @fakemailbot for verification code")
            print("💾 Account details saved to file!")
            
            input("\n⏳ Press ENTER to close browser...")
            
            return True
            
        except Exception as e:
            print(f"❌ Automation error: {e}")
            return False
        finally:
            driver.quit()

# ===== MAIN EXECUTION =====
if __name__ == "__main__":
    print("🤖 AUTO-TWITTER BOT")
    print("⭐ Kali Linux - Virtual Environment")
    print("="*50)
    
    # First install webdriver-manager using system pip (allowed in Kali)
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "webdriver-manager"], 
                      capture_output=True)
    except:
        pass
    
    # Setup virtual environment
    python_path = setup_environment()
    
    # Run the bot in the virtual environment
    if sys.platform.startswith('win'):
        subprocess.run([python_path, __file__])
    else:
        os.execv(python_path, [python_path, __file__])
    
    # If we get here, run the actual bot
    bot = AutoTwitterBot()
    
    while True:
        success = bot.run_automation()
        
        if success:
            print("\n✅ Process completed successfully!")
        else:
            print("\n❌ Process failed")
        
        choice = input("\nCreate another account? (y/n): ").lower().strip()
        if choice != 'y':
            print("👋 Thank you for using Auto-Twitter Bot!")
            break
        
        print("\n" + "="*50)
        print("🔄 STARTING NEW ACCOUNT...")
        print("="*50)
