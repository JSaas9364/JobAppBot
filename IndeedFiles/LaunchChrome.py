from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import webbrowser

# Open a new Indeed tab (this assumes Chrome is already running)
INDEED_URL = "https://www.indeed.com/jobs?q=helpdesk&l=remote"
webbrowser.open_new_tab(INDEED_URL)

# Start Selenium session
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# Wait for Indeed tab to open and attach to it
indeed_tab_found = False
for handle in driver.window_handles:
    driver.switch_to.window(handle)
    if "indeed.com" in driver.current_url:
        indeed_tab_found = True
        print("Connected to the new Indeed tab.")
        break

if not indeed_tab_found:
    print("No Indeed tab found. Please open Indeed manually and rerun the script.")
    driver.quit()
    exit()

def search_jobs():
    """Search for Helpdesk Remote jobs."""
    print("Navigating to Indeed job search page...")
    driver.get(INDEED_URL)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='jobTitle']")))
    print("Job search results loaded.")

def apply_to_easy_apply_jobs():
    """Find and apply to Easy Apply jobs."""
    print("Searching for Easy Apply jobs...")
    jobs = driver.find_elements(By.CSS_SELECTOR, "[data-testid='jobTitle']")
    
    if not jobs:
        print("No Easy Apply jobs found. Exiting.")
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
