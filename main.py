#!/usr/bin/env python3
import os
import sys
import subprocess
import importlib
import time
import random
import string
from datetime import datetime

# ===== AUTO-INSTALLATION =====
def install_requirements():
    """Automatically install all required packages"""
    required_packages = {
        'selenium': 'selenium',
        'telethon': 'telethon', 
        'requests': 'requests',
        'beautifulsoup4': 'beautifulsoup4',
        'cryptography': 'cryptography'
    }
    
    print("🔧 Installing required packages...")
    
    for package, pip_name in required_packages.items():
        try:
            importlib.import_module(package)
            print(f"✅ {package} already installed")
        except ImportError:
            print(f"📦 Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
    
    # Install Chrome and ChromeDriver on Linux
    if sys.platform.startswith('linux'):
        print("🌐 Setting up Chrome browser...")
        try:
            # Install Chrome
            subprocess.run(['wget', 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'], 
                         capture_output=True)
            subprocess.run(['sudo', 'apt', 'install', './google-chrome-stable_current_amd64.deb', '-y'], 
                         capture_output=True)
            
            # Install ChromeDriver
            subprocess.run(['wget', 'https://storage.googleapis.com/chrome-for-testing-public/120.0.6099.109/linux64/chromedriver-linux64.zip'], 
                         capture_output=True)
            subprocess.run(['unzip', 'chromedriver-linux64.zip'], capture_output=True)
            subprocess.run(['sudo', 'mv', 'chromedriver-linux64/chromedriver', '/usr/local/bin/'], 
                         capture_output=True)
            subprocess.run(['sudo', 'chmod', '+x', '/usr/local/bin/chromedriver'], 
                         capture_output=True)
            print("✅ Chrome setup completed")
        except:
            print("⚠️ Chrome setup may need manual intervention")

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
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        print("🌐 Launching browser...")
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
        except Exception as e:
            print(f"❌ Browser error: {e}")
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
            "//div[contains(text(), 'Create account')]"
        ]
        
        for selector in selectors:
            try:
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                button.click()
                print("✅ Clicked Create Account button!")
                return True
            except:
                continue
        
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
            time.sleep(3)
            
            # Fill name field
            name_selectors = ["//input[@name='name']", "//input[@placeholder='Name']", "//input[contains(@class, 'name')]"]
            for selector in name_selectors:
                try:
                    name_field = driver.find_element(By.XPATH, selector)
                    name_field.clear()
                    name_field.send_keys(name)
                    print(f"✅ Name entered: {name}")
                    break
                except:
                    continue
            
            time.sleep(1)
            
            # Fill email field
            email_selectors = ["//input[@name='email']", "//input[@type='email']", "//input[contains(@placeholder, 'email')]"]
            for selector in email_selectors:
                try:
                    email_field = driver.find_element(By.XPATH, selector)
                    email_field.clear()
                    email_field.send_keys(email)
                    print(f"✅ Email entered: {email}")
                    break
                except:
                    continue
            
            time.sleep(1)
            
            # Handle date of birth
            self.fill_date_of_birth(driver, day, month, year)
            time.sleep(1)
            
            # Click Next button
            next_selectors = ["//span[contains(text(), 'Next')]", "//button[contains(text(), 'Next')]", "//div[contains(text(), 'Next')]"]
            for selector in next_selectors:
                try:
                    next_btn = driver.find_element(By.XPATH, selector)
                    next_btn.click()
                    print("✅ Clicked Next")
                    break
                except:
                    continue
            
            time.sleep(3)
            
            # Fill username
            username_selectors = ["//input[@name='username']", "//input[contains(@placeholder, 'username')]"]
            for selector in username_selectors:
                try:
                    username_field = driver.find_element(By.XPATH, selector)
                    username_field.clear()
                    username_field.send_keys(username)
                    print(f"✅ Username entered: {username}")
                    break
                except:
                    continue
            
            time.sleep(1)
            
            # Click Next after username
            for selector in next_selectors:
                try:
                    next_btn = driver.find_element(By.XPATH, selector)
                    next_btn.click()
                    print("✅ Clicked Next after username")
                    break
                except:
                    continue
            
            time.sleep(3)
            
            # Fill password
            password_selectors = ["//input[@type='password']", "//input[@name='password']"]
            for selector in password_selectors:
                try:
                    password_field = driver.find_element(By.XPATH, selector)
                    password_field.clear()
                    password_field.send_keys(password)
                    print("✅ Password entered")
                    break
                except:
                    continue
            
            time.sleep(1)
            
            # Final signup
            signup_selectors = ["//span[contains(text(), 'Sign up')]", "//button[contains(text(), 'Sign up')]"]
            for selector in signup_selectors:
                try:
                    signup_btn = driver.find_element(By.XPATH, selector)
                    signup_btn.click()
                    print("✅ Final signup clicked!")
                    return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"❌ Form filling error: {e}")
            return False

    def fill_date_of_birth(self, driver, day, month, year):
        """Fill date of birth fields"""
        from selenium.webdriver.common.by import By
        
        try:
            # Month dropdown
            month_selectors = ["//select[@id='SELECTOR_1']", "//select[contains(@name, 'month')]"]
            for selector in month_selectors:
                try:
                    month_dropdown = driver.find_element(By.XPATH, selector)
                    month_dropdown.click()
                    time.sleep(1)
                    month_option = driver.find_element(By.XPATH, f"//option[@value='{month}']")
                    month_option.click()
                    break
                except:
                    continue
            
            time.sleep(1)
            
            # Day dropdown
            day_selectors = ["//select[@id='SELECTOR_2']", "//select[contains(@name, 'day')]"]
            for selector in day_selectors:
                try:
                    day_dropdown = driver.find_element(By.XPATH, selector)
                    day_dropdown.click()
                    time.sleep(1)
                    day_option = driver.find_element(By.XPATH, f"//option[@value='{day}']")
                    day_option.click()
                    break
                except:
                    continue
            
            time.sleep(1)
            
            # Year dropdown
            year_selectors = ["//select[@id='SELECTOR_3']", "//select[contains(@name, 'year')]"]
            for selector in year_selectors:
                try:
                    year_dropdown = driver.find_element(By.XPATH, selector)
                    year_dropdown.click()
                    time.sleep(1)
                    year_option = driver.find_element(By.XPATH, f"//option[@value='{year}']")
                    year_option.click()
                    break
                except:
                    continue
            
            print(f"✅ DOB set: {day}/{month}/{year}")
            
        except Exception as e:
            print(f"⚠️ DOB setup failed: {e}")

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
    print("⭐ Automatic installation & execution")
    print("="*50)
    
    # Auto-install requirements
    install_requirements()
    
    # Run the bot
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
