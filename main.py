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

# Initialize Telegram client
client = TelegramClient('session_name', api_id, api_hash)

file_name = "twitter_accounts.txt"

if not os.path.exists(file_name):
    with open(file_name, "w") as f:
        f.write("S.No | Username | Email | Password | Date Created\n")

def get_next_username(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%"
    return ''.join(random.choices(chars, k=length))

def generate_name():
    first_names = ['John', 'Mike', 'David', 'Chris', 'Alex', 'James', 'Robert', 'Daniel']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis']
    return f"{random.choice(first_names)} {random.choice(last_names)}"

async def register_email_with_bot(email):
    try:
        bot = await client.get_entity('fakemailbot')
        await client.send_message(bot, "/start")
        await asyncio.sleep(2)
        await client.send_message(bot, "/set")
        await asyncio.sleep(2)
        await client.send_message(bot, email)
        print(f"✅ Email {email} registered with @fakemailbot")
        await asyncio.sleep(3)
        return True
    except Exception as e:
        print(f"❌ Email registration failed: {e}")
        return False

async def save_credentials(email, username, password):
    try:
        with open(file_name, "r") as f:
            lines = f.readlines()
        
        serial_no = len(lines)  # Header counts as line 1
        date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(file_name, "a") as f:
            f.write(f"{serial_no} | {username} | {email} | {password} | {date_created}\n")

        print(f"\n✅ Credentials saved:")
        print(f"📧 Email: {email}")
        print(f"👤 Username: {username}")
        print(f"🔑 Password: {password}")
        print(f"💾 Saved to: {file_name}\n")
        return True
    except Exception as e:
        print(f"❌ Error saving credentials: {e}")
        return False

def setup_browser():
    """Setup Chrome browser with options"""
    try:
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Try different Chrome driver approaches
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except:
            # Fallback to system Chrome
            driver = webdriver.Chrome(options=chrome_options)
        
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    except Exception as e:
        print(f"❌ Browser setup failed: {e}")
        return None

def click_create_account(driver):
    """Click create account button with multiple fallbacks"""
    wait = WebDriverWait(driver, 15)
    
    # Try multiple selectors
    selectors = [
        "//span[contains(text(), 'Create account')]",
        "//span[contains(text(), 'Sign up')]",
        "//a[contains(@href, 'signup')]",
        "//button[contains(text(), 'Sign up')]",
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

def fill_signup_form(driver, name, email, username, password):
    """Fill the complete signup form"""
    wait = WebDriverWait(driver, 15)
    
    try:
        # Wait for form to load
        time.sleep(3)
        
        # Fill name
        name_fields = driver.find_elements(By.XPATH, "//input[@name='name']")
        if name_fields:
            name_fields[0].send_keys(name)
            print(f"✅ Name entered: {name}")
        
        time.sleep(1)
        
        # Fill email
        email_fields = driver.find_elements(By.XPATH, "//input[@type='email']")
        if email_fields:
            email_fields[0].send_keys(email)
            print(f"✅ Email entered: {email}")
        
        time.sleep(1)
        
        # Fill date of birth
        fill_dob(driver)
        time.sleep(1)
        
        # Click Next
        click_next_button(driver)
        time.sleep(3)
        
        # Fill username on next page
        username_fields = driver.find_elements(By.XPATH, "//input[@name='username']")
        if username_fields:
            username_fields[0].clear()
            username_fields[0].send_keys(username)
            print(f"✅ Username entered: {username}")
        
        time.sleep(1)
        click_next_button(driver)
        time.sleep(3)
        
        # Fill password
        password_fields = driver.find_elements(By.XPATH, "//input[@type='password']")
        if password_fields:
            password_fields[0].send_keys(password)
            print("✅ Password entered")
        
        time.sleep(1)
        
        # Final signup
        click_signup_button(driver)
        
        return True
        
    except Exception as e:
        print(f"❌ Form filling error: {e}")
        return False

def fill_dob(driver):
    """Fill date of birth"""
    try:
        # Generate random DOB (18-25 years old)
        current_year = datetime.now().year
        birth_year = random.randint(current_year-25, current_year-18)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)
        
        # Try different DOB field selectors
        month_selectors = ["SELECTOR_1", "Month", "month"]
        day_selectors = ["SELECTOR_2", "Day", "day"] 
        year_selectors = ["SELECTOR_3", "Year", "year"]
        
        # Fill month
        for selector in month_selectors:
            try:
                month_dropdown = driver.find_element(By.ID, selector)
                Select(month_dropdown).select_by_value(str(birth_month))
                break
            except:
                continue
        
        # Fill day
        for selector in day_selectors:
            try:
                day_dropdown = driver.find_element(By.ID, selector)
                Select(day_dropdown).select_by_value(str(birth_day))
                break
            except:
                continue
        
        # Fill year
        for selector in year_selectors:
            try:
                year_dropdown = driver.find_element(By.ID, selector)
                Select(year_dropdown).select_by_value(str(birth_year))
                break
            except:
                continue
        
        print(f"✅ DOB set: {birth_day}/{birth_month}/{birth_year}")
        
    except Exception as e:
        print(f"⚠️ DOB selection failed: {e}")

def click_next_button(driver):
    """Click Next button"""
    next_selectors = [
        "//span[contains(text(), 'Next')]",
        "//button[contains(text(), 'Next')]",
        "//div[contains(text(), 'Next')]"
    ]
    
    for selector in next_selectors:
        try:
            buttons = driver.find_elements(By.XPATH, selector)
            for button in buttons:
                try:
                    button.click()
                    print("✅ Clicked Next")
                    return True
                except:
                    continue
        except:
            continue
    return False

def click_signup_button(driver):
    """Click final Signup button"""
    signup_selectors = [
        "//span[contains(text(), 'Sign up')]",
        "//button[contains(text(), 'Sign up')]",
        "//div[contains(text(), 'Sign up')]"
    ]
    
    for selector in signup_selectors:
        try:
            buttons = driver.find_elements(By.XPATH, selector)
            for button in buttons:
                try:
                    button.click()
                    print("✅ Final signup clicked!")
                    return True
                except:
                    continue
        except:
            continue
    return False

async def automate_twitter_signup(name, email, username, password):
    """Complete automated Twitter signup"""
    print("🌐 Launching browser...")
    driver = setup_browser()
    
    if not driver:
        return False
    
    try:
        # Open Twitter signup
        driver.get("https://x.com/i/flow/signup")
        print("✅ Opened Twitter signup page")
        time.sleep(5)
        
        # Click create account
        if not click_create_account(driver):
            return False
        
        # Fill complete form
        if not fill_signup_form(driver, name, email, username, password):
            return False
        
        print("⏳ Waiting for verification step...")
        print("📧 Check @fakemailbot for verification code")
        
        # Wait for manual verification
        input("⏳ Press ENTER after you've completed verification...")
        
        return True
        
    except Exception as e:
        print(f"❌ Automation error: {e}")
        return False
    finally:
        driver.quit()
        print("🌐 Browser closed")

async def main():
    # Generate account details
    name = generate_name()
    username = get_next_username()
    email = f"{username}@telegmail.com"
    password = generate_password()
    
    print(f"\n🚀 STARTING ACCOUNT CREATION")
    print(f"👤 Name: {name}")
    print(f"📧 Email: {email}")
    print(f"🆔 Username: {username}")
    print(f"🔑 Password: {password}")
    
    # Register email with bot
    if not await register_email_with_bot(email):
        return
    
    # Save credentials
    await save_credentials(email, username, password)
    
    # Automated Twitter signup
    success = await automate_twitter_signup(name, email, username, password)
    
    if success:
        print("🎊 ACCOUNT CREATION PROCESS COMPLETED!")
    else:
        print("❌ Account creation failed")

if __name__ == '__main__':
    # Run the bot
    asyncio.run(main())
