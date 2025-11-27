#!/usr/bin/env python3
from telethon.sync import TelegramClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random
import string
import os
import asyncio
from datetime import datetime

# Telegram credentials
api_id = 36522969
api_hash = '8fe00a5f086cbfd9b2688b5848bd14c5'
phone_number = '+919043785587'

file_name = "twitter_accounts.txt"

class TwitterBot:
    def __init__(self):
        self.client = None
        self.setup_files()
    
    def setup_files(self):
        if not os.path.exists(file_name):
            with open(file_name, "w") as f:
                f.write("S.No | Username | Email | Password | Date Created\n")
    
    async def connect_telegram(self):
        """Connect to Telegram properly"""
        try:
            self.client = TelegramClient('session_name', api_id, api_hash)
            await self.client.start(phone=phone_number)
            print("✅ Connected to Telegram successfully!")
            return True
        except Exception as e:
            print(f"❌ Telegram connection failed: {e}")
            return False
    
    def get_next_username(self, length=8):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    def generate_password(self, length=12):
        chars = string.ascii_letters + string.digits + "!@#$%"
        return ''.join(random.choices(chars, k=length))
    
    def generate_name(self):
        first_names = ['John', 'Mike', 'David', 'Chris', 'Alex', 'James', 'Robert', 'Daniel']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis']
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    async def register_email_with_bot(self, email):
        """Register email with fakemailbot"""
        try:
            # Check if client is connected
            if not self.client or not self.client.is_connected():
                print("❌ Telegram client not connected")
                return False
            
            bot = await self.client.get_entity('fakemailbot')
            
            # Send commands to bot
            await self.client.send_message(bot, "/start")
            await asyncio.sleep(2)
            
            await self.client.send_message(bot, "/set")
            await asyncio.sleep(2)
            
            await self.client.send_message(bot, email)
            print(f"✅ Email {email} registered with @fakemailbot")
            await asyncio.sleep(3)
            
            return True
        except Exception as e:
            print(f"❌ Email registration failed: {e}")
            return False
    
    async def save_credentials(self, email, username, password):
        try:
            with open(file_name, "r") as f:
                lines = f.readlines()
            
            serial_no = len(lines)
            date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(file_name, "a") as f:
                f.write(f"{serial_no} | {username} | {email} | {password} | {date_created}\n")

            print(f"\n✅ Credentials saved:")
            print(f"📧 Email: {email}")
            print(f"👤 Username: {username}")
            print(f"🔑 Password: {password}")
            return True
        except Exception as e:
            print(f"❌ Error saving credentials: {e}")
            return False
    
    def setup_browser(self):
        """Setup Chrome browser with options"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Try to use system Chrome
            driver = webdriver.Chrome(options=chrome_options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return None
    
    def click_create_account(self, driver):
        """Click create account button"""
        wait = WebDriverWait(driver, 15)
        
        selectors = [
            "//span[contains(text(), 'Create account')]",
            "//span[contains(text(), 'Sign up')]",
            "//a[contains(@href, 'signup')]",
        ]
        
        for selector in selectors:
            try:
                button = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                button.click()
                print("✅ Clicked Create Account button")
                return True
            except:
                continue
        
        print("❌ Could not find Create Account button")
        return False
    
    def fill_signup_form(self, driver, name, email, username, password):
        """Fill the complete signup form"""
        try:
            # Wait for form to load
            time.sleep(3)
            
            # Fill name
            name_field = driver.find_element(By.NAME, "name")
            name_field.send_keys(name)
            print(f"✅ Name entered: {name}")
            time.sleep(1)
            
            # Fill email
            email_field = driver.find_element(By.NAME, "email")
            email_field.send_keys(email)
            print(f"✅ Email entered: {email}")
            time.sleep(1)
            
            # Fill date of birth
            self.fill_dob(driver)
            time.sleep(1)
            
            # Click Next
            self.click_next_button(driver)
            time.sleep(3)
            
            # Fill username on next page
            username_field = driver.find_element(By.NAME, "username")
            username_field.clear()
            username_field.send_keys(username)
            print(f"✅ Username entered: {username}")
            time.sleep(1)
            
            self.click_next_button(driver)
            time.sleep(3)
            
            # Fill password
            password_field = driver.find_element(By.XPATH, "//input[@type='password']")
            password_field.send_keys(password)
            print("✅ Password entered")
            time.sleep(1)
            
            # Final signup
            self.click_signup_button(driver)
            
            return True
            
        except Exception as e:
            print(f"❌ Form filling error: {e}")
            return False
    
    def fill_dob(self, driver):
        """Fill date of birth"""
        try:
            # Generate random DOB (18-25 years old)
            current_year = datetime.now().year
            birth_year = random.randint(current_year-25, current_year-18)
            birth_month = random.randint(1, 12)
            birth_day = random.randint(1, 28)
            
            # Fill month
            month_dropdown = driver.find_element(By.ID, "SELECTOR_1")
            Select(month_dropdown).select_by_value(str(birth_month))
            
            # Fill day
            day_dropdown = driver.find_element(By.ID, "SELECTOR_2")
            Select(day_dropdown).select_by_value(str(birth_day))
            
            # Fill year
            year_dropdown = driver.find_element(By.ID, "SELECTOR_3")
            Select(year_dropdown).select_by_value(str(birth_year))
            
            print(f"✅ DOB set: {birth_day}/{birth_month}/{birth_year}")
            
        except Exception as e:
            print(f"⚠️ DOB selection failed: {e}")
    
    def click_next_button(self, driver):
        """Click Next button"""
        try:
            next_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]")
            next_button.click()
            print("✅ Clicked Next")
            return True
        except:
            return False
    
    def click_signup_button(self, driver):
        """Click final Signup button"""
        try:
            signup_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Sign up')]")
            signup_button.click()
            print("✅ Final signup clicked!")
            return True
        except:
            return False
    
    async def automate_twitter_signup(self, name, email, username, password):
        """Complete automated Twitter signup"""
        print("🌐 Launching browser...")
        driver = self.setup_browser()
        
        if not driver:
            return False
        
        try:
            # Open Twitter signup
            driver.get("https://x.com/i/flow/signup")
            print("✅ Opened Twitter signup page")
            time.sleep(5)
            
            # Click create account
            if not self.click_create_account(driver):
                return False
            
            # Fill complete form
            if not self.fill_signup_form(driver, name, email, username, password):
                return False
            
            print("⏳ Waiting for verification step...")
            print("📧 Check @fakemailbot for verification code")
            
            # Keep browser open for verification
            input("⏳ Press ENTER after you've completed verification...")
            
            return True
            
        except Exception as e:
            print(f"❌ Automation error: {e}")
            return False
        finally:
            driver.quit()
            print("🌐 Browser closed")
    
    async def run(self):
        """Main function to run the bot"""
        print("🚀 STARTING TWITTER BOT")
        print("="*50)
        
        # Connect to Telegram first
        if not await self.connect_telegram():
            return
        
        # Generate account details
        name = self.generate_name()
        username = self.get_next_username()
        email = f"{username}@telegmail.com"
        password = self.generate_password()
        
        print(f"\n🎲 GENERATED ACCOUNT DETAILS:")
        print(f"👤 Name: {name}")
        print(f"📧 Email: {email}")
        print(f"🆔 Username: {username}")
        print(f"🔑 Password: {password}")
        
        # Register email with bot
        if not await self.register_email_with_bot(email):
            await self.client.disconnect()
            return
        
        # Save credentials
        await self.save_credentials(email, username, password)
        
        # Automated Twitter signup
        success = await self.automate_twitter_signup(name, email, username, password)
        
        if success:
            print("🎊 ACCOUNT CREATION PROCESS COMPLETED!")
        else:
            print("❌ Account creation failed")
        
        # Disconnect Telegram
        await self.client.disconnect()
        print("🔒 Telegram disconnected")

# Run the bot
async def main():
    bot = TwitterBot()
    await bot.run()

if __name__ == '__main__':
    asyncio.run(main())
