import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import string
import os

# --- New Imports for WebDriver Manager ---
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# It's highly recommended to use selenium-stealth to avoid bot detection
# Run: pip install selenium-stealth
from selenium_stealth import stealth

# --- قوائم الأسماء العشوائية ---
first_names = ["Juan", "David", "Jose", "Manuel", "Pedro", "Carlos", "Javier", "Daniel", "Luis", "Fernando"]
last_names = ["Garcia", "Rodriguez", "Gonzalez", "Fernandez", "Lopez", "Martinez", "Sanchez", "Perez", "Gomez", "Martin"]

# --- دوال إنشاء بيانات عشوائية ---
def generate_random_email():
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    return random_part + "@example.com"

def generate_strong_password(length=12):
    if length < 8: length = 8
    lower, upper, digits, special = string.ascii_lowercase, string.ascii_uppercase, string.digits, "!@#$%^&*"
    password = [random.choice(lower), random.choice(upper), random.choice(digits), random.choice(special)]
    all_chars = lower + upper + digits + special
    password += random.choices(all_chars, k=length - 4)
    random.shuffle(password)
    return "".join(password)

# --- الإعدادات ---
url = 'https://www.paypal.com/uno/signup?taskAttempted=anw_create_account_redirection&country.x=US&locale.x=en_US&failedBecause=verification_failed&resumePageId=d5e6f7a8-b9c0-4d1e-8f2a-3b4c5d6e7f8b'

# --- إعدادات المتصفح ---
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# --- استخدام مسار البروفايل الخاص بك ---
#
# IMPORTANT: YOU MUST CHANGE THIS PATH TO YOUR OWN CHROME PROFILE PATH.
# The path should point to the "User Data" folder, which contains the "Default" folder.
# Example for Windows: "C:\\Users\\YourUsername\\AppData\\Local\\Google\\Chrome\\User Data"
#
# --- مهم: يجب أن تقوم بتغيير هذا المسار إلى مسار البروفايل الخاص بك.
# المسار يجب أن يشير إلى مجلد "User Data" الذي يحتوي بداخله على مجلد "Default".
# مثال لنظام ويندوز: "C:\\Users\\YourUsername\\AppData\\Local\\Google\\Chrome\\User Data"
profile_path = "CHANGE_THIS_TO_YOUR_PROFILE_PATH" 
chrome_options.add_argument(f"user-data-dir={profile_path}")

# --- تشغيل الكود ---
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Win32", webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True)

try:
    with open('num.txt', 'r') as file:
        phone_numbers_list = file.readlines()
    print(f"✅ Found {len(phone_numbers_list)} numbers in 'num.txt' to process.")
except FileNotFoundError:
    print("❌ Error: 'num.txt' file not found. Please create it. Exiting.")
    phone_numbers_list = []
    driver.quit()

# --- الحلقة الرئيسية لمعالجة كل رقم ---
while len(phone_numbers_list) > 0:
    
    current_phone_number = phone_numbers_list[0].strip()
    
    print(f"\n--- 🔄 Starting process for number: {current_phone_number} 🔄 ---")
    
    try:
        driver.switch_to.new_window('tab')
        
        window_handles = driver.window_handles
        
        if len(window_handles) > 2:
            driver.switch_to.window(window_handles[0])
            driver.close()
            driver.switch_to.window(window_handles[-1])
            
        driver.get(url)

        random_first_name = random.choice(first_names)
        random_last_name = random.choice(last_names)
        
        FIRST_NAME_ID = "text-input-person_name_widget_givenName"
        LAST_NAME_ID = "text-input-person_name_widget_surname"
        EMAIL_ID = "text-input-e2b3c4d5-6f7a-4b8c-9d0e-1f2a3b4c5d6e"
        PASSWORD_ID = "password-input-17475f5a-3d52-4ea7-a743-7526e24bf7a3"
        COUNTRY_DROPDOWN_ID = "dropdownMenuButton_d6e7f8a9-b0c1-4d2e-8f3a-4b5c6d7e8f9a-menu"
        PHONE_NUMBER_ID = "text-input-d6e7f8a9-b0c1-4d2e-8f3a-4b5c6d7e8f9a"
        SPAIN_SELECTOR = "[data-value='ES_34']"

        first_name_input = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, FIRST_NAME_ID)))
        first_name_input.send_keys(random_first_name)
        time.sleep(random.uniform(0.5, 1.5))

        driver.find_element(By.ID, LAST_NAME_ID).send_keys(random_last_name)
        time.sleep(random.uniform(0.5, 1.5))
        
        driver.find_element(By.ID, EMAIL_ID).send_keys(generate_random_email())
        time.sleep(random.uniform(0.5, 1.5))
        
        driver.find_element(By.ID, PASSWORD_ID).send_keys(generate_strong_password())
        time.sleep(random.uniform(0.5, 1.5))
        
        driver.find_element(By.ID, COUNTRY_DROPDOWN_ID).click()
        time.sleep(random.uniform(0.5, 1.5))
        
        spain_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, SPAIN_SELECTOR)))
        spain_option.click()
        time.sleep(random.uniform(0.5, 1.5))
        
        phone_number_to_enter = current_phone_number
        if phone_number_to_enter.startswith('34'):
            phone_number_to_enter = phone_number_to_enter[2:]
        driver.find_element(By.ID, PHONE_NUMBER_ID).send_keys(phone_number_to_enter)
        time.sleep(random.uniform(1.0, 3.0))

        agree_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Agree and Create Account')]")))
        agree_button.click()
        time.sleep(random.uniform(1.0, 3.0))
        
        text_code_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-nemo='smsSelectButton']")))
        text_code_button.click()
        time.sleep(random.uniform(1.0, 3.0))

        # --- الكود الجديد: حلقة تنقر على "Send New Code" 4 مرات ---
        print("Starting 4-click loop on 'Send New Code'...")
        for i in range(4):
            try:
                resend_link = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, "Send New Code")))
                resend_link.click()
                print(f"✅ Clicked 'Send New Code' for the {i+1} time.")
                time.sleep(random.uniform(3, 5))
            except Exception as e:
                print(f"❌ Could not click 'Send New Code' on attempt {i+1}. The element may not be available.")
                break # Break the loop if the element isn't found
        
        print(f"✅ Process completed successfully for number: {current_phone_number}")

        # --- نقل الرقم إلى ملف text.txt عند الانتهاء بنجاح ---
        with open('text.txt', 'a') as text_file:
            text_file.write(current_phone_number + '\n')
        print(f"✅ Number {current_phone_number} moved to text.txt")
        
    except Exception as e:
        print(f"❌ An error occurred with number {current_phone_number}: {e}")
    finally:
        # --- تحديث ملف num.txt لإزالة الرقم الذي تم استخدامه ---
        phone_numbers_list.pop(0) # حذف الرقم الأول من القائمة
        with open('num.txt', 'w') as file:
            for num in phone_numbers_list:
                file.write(num)
        print("✅ num.txt updated. The used number has been removed.")

    print("--- Waiting a moment before starting the next number ---")
    time.sleep(5)

print("\n\n🎉 All numbers have been processed. Closing the browser.")
driver.quit()
