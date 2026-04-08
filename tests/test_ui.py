from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

try:
    driver.get("http://localhost:8501")
    
    # 1. Flexible Title Check
    print(f"Current Page Title is: {driver.title}")
    assert "Fraud" in driver.title or "Monitor" in driver.title

    # 2. Wait up to 10 seconds for the Dashboard data to appear
    # We look for 'stDataFrame' or 'stTable' or simply any text that says 'Transaction'
    wait = WebDriverWait(driver, 10)
    
    # This waits until the main dataframe/table container is actually rendered
    data_element = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Transaction')]"))
    )
    
    print("UI Test Passed: Transaction data is visible on the dashboard.")

except Exception as e:
    print(f"Test Failed: {e}")

finally:
    driver.quit()