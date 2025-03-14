from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import psutil

def find_chrome():
    """Find if Chrome is running."""
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if "chrome" in process.info['name'].lower():
            return True
    return False

# Ensure Chrome is running
if not find_chrome():
    print("Chrome is not running. Please open Chrome and Indeed manually before running the script.")
    exit()

# Connect to running Chrome session
options = webdriver.ChromeOptions()
options.debugger_address = "localhost:9222"  # Connect to existing Chrome
try:
    driver = webdriver.Chrome(options=options)
    print("Connected to running Chrome instance...")
except Exception as e:
    print("Failed to connect to Chrome. Make sure Chrome is running with remote debugging enabled.")
    exit()

# Find an open Indeed tab
indeed_tab_found = False
for handle in driver.window_handles:
    driver.switch_to.window(handle)
    if "indeed.com" in driver.current_url:
        indeed_tab_found = True
        print("Connected to an open Indeed tab.")
        break

if not indeed_tab_found:
    print("No Indeed tab found. Please open Indeed manually and rerun the script.")
    driver.quit()
    exit()

def search_jobs():
    """Navigates to job search page."""
    print("Navigating to Indeed job search page...")
    driver.get("https://www.indeed.com/jobs?q=helpdesk&l=remote")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='jobTitle']")))
    print("Job search results loaded.")

def apply_to_easy_apply_jobs():
    """Finds and applies to Easy Apply jobs."""
    print("Searching for Easy Apply jobs...")
    jobs = driver.find_elements(By.CSS_SELECTOR, "[data-testid='jobTitle']")
    
    if not jobs:
        print("No jobs found. Exiting.")
        return
    
    for job in jobs[:10]:  # Limit applications to 10 jobs per run
        try:
            job.click()
            time.sleep(3)
            apply_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Apply Now')]"))
            )
            apply_button.click()
            print("Applied to job successfully!")
            time.sleep(5)
        except Exception as e:
            print("Error applying to job:", e)
            continue

if __name__ == "__main__":
    search_jobs()
    apply_to_easy_apply_jobs()
    print("Job applications complete.")
