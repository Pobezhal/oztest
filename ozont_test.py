import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

def test_requests():
    """Test if we can access Ozon with simple requests"""
    print("=== TESTING REQUESTS ===")
    urls = [
        "https://ozon.kz",
        "https://ozon.kz/search/?text=continental&brand=18580188",
        "https://ozon.kz/category/shiny-i-diski-8501/continental-18580188/"
    ]
    
    for url in urls:
        try:
            print(f"\nTesting: {url}")
            response = requests.get(url, timeout=10)
            print(f"Status: {response.status_code}")
            print(f"Final URL: {response.url}")
            print(f"Contains 'Ozon': {'Ozon' in response.text}")
            print(f"Contains 'antibot': {'antibot' in response.text.lower()}")
            
            # Save response for analysis
            with open(f"response_{url.split('/')[-1]}.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Saved: response_{url.split('/')[-1]}.html")
            
        except Exception as e:
            print(f"Failed: {e}")

def test_selenium():
    """Test if we can access Ozon with Selenium"""
    print("\n=== TESTING SELENIUM ===")
    opts = Options()
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--headless=new")
    
    # Add user agent
    opts.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=opts)
    
    urls = [
        "https://ozon.kz",
        "https://ozon.kz/search/?text=continental&brand=18580188",
        "https://ozon.kz/category/shiny-i-diski-8501/continental-18580188/"
    ]
    
    for url in urls:
        try:
            print(f"\nTesting: {url}")
            driver.get(url)
            time.sleep(5)
            
            print(f"Page title: {driver.title}")
            print(f"Current URL: {driver.current_url}")
            print(f"Contains 'Ozon': {'Ozon' in driver.page_source}")
            print(f"Contains 'antibot': {'antibot' in driver.page_source.lower()}")
            
            # Save screenshot and page source
            driver.save_screenshot(f"selenium_{url.split('/')[-1]}.png")
            with open(f"selenium_{url.split('/')[-1]}.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print(f"Saved: selenium_{url.split('/')[-1]}.png and .html")
            
        except Exception as e:
            print(f"Failed: {e}")
    
    driver.quit()

if __name__ == "__main__":
    print("🔍 Testing Ozon accessibility from Railway...")
    test_requests()
    test_selenium()
    print("\n📊 All tests completed. Check the saved files for details.")
