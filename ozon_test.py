import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import os

def test_requests():
    
    OZON_URL = "https://ozon.kz/category/shiny-i-diski-8501/continental-18580188/?brand_was_predicted=true&deny_category_prediction=true&from_global=true&season=31827%2C33890&text=Continental&tirecondition=101129387"
    """Test if we can access Ozon with simple requests"""
    print("=== TESTING REQUESTS ===")
    urls = [
        "https://ozon.kz",
        "https://ozon.kz/search/?text=continental&brand=18580188",
        OZON_URL
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
   
    # Use the SAME environment variables as main project
    chrome_bin = os.getenv("CHROME_BIN", "/nix/var/nix/profiles/default/bin/chromium")
    chromedriver_bin = os.getenv("CHROMEDRIVER_BIN", "/nix/var/nix/profiles/default/bin/chromedriver")
    
    print(f"Using Chrome: {chrome_bin}")
    print(f"Using Chromedriver: {chromedriver_bin}")
    
    # Check if files exist
    if not os.path.exists(chrome_bin):
        print(f"❌ Chrome binary not found at {chrome_bin}")
        return False
    if not os.path.exists(chromedriver_bin):
        print(f"❌ Chromedriver not found at {chromedriver_bin}")
        return False
    
    opts = Options()
    opts.binary_location = chrome_bin
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--headless=new")
    opts.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Use Service with chromedriver path
    from selenium.webdriver.chrome.service import Service
    service = Service(chromedriver_bin)
    driver = webdriver.Chrome(service=service, options=opts)
    
    urls = [
        "https://ozon.kz",
        "https://ozon.kz/search/?text=continental&brand=18580188",
        OZON_URL 
    ]
    
    for url in urls:
        try:
            print(f"\nTesting: {url}")
            driver.get(url)
            time.sleep(5)
            
            print(f"Page title: {driver.title}")
            print(f"Current URL: {driver.current_url}")
            
            # Check for specific blocking indicators
            page_source = driver.page_source
            if "antibot" in page_source.lower():
                print("❌ BLOCKED: Anti-bot page detected")
                # Print first 500 chars of page source to see what's shown
                print("Page content preview:")
                print(page_source[:500])
            elif "Ozon" in page_source:
                print("✅ SUCCESS: Ozon page loaded!")
                # Print first 500 chars to see if it's the real site
                print("Page content preview:")
                print(page_source[:500])
            else:
                print("❓ UNKNOWN: Page loaded but doesn't look like Ozon")
                print("Page content preview:")
                print(page_source[:500])
            
            # Take screenshot as base64 for manual viewing
            screenshot_b64 = driver.get_screenshot_as_base64()
            print(f"📸 Screenshot (base64 - first 200 chars):")
            print(screenshot_b64[:200] + "...")
            
        except Exception as e:
            print(f"Failed: {e}")
    
    driver.quit()

def test_selenium_headful():
    """Test if we can access Ozon with headful Selenium using virtual display"""
    print("\n=== TESTING SELENIUM HEADFUL ===")
    OZON_URL = "https://ozon.kz/category/shiny-i-diski-8501/continental-18580188/?brand_was_predicted=true&deny_category_prediction=true&from_global=true&season=31827%2C33890&text=Continental&tirecondition=101129387"

    
    # Use the SAME environment variables as main project
    chrome_bin = os.getenv("CHROME_BIN", "/nix/var/nix/profiles/default/bin/chromium")
    chromedriver_bin = os.getenv("CHROMEDRIVER_BIN", "/nix/var/nix/profiles/default/bin/chromedriver")
    
    print(f"Using Chrome: {chrome_bin}")
    print(f"Using Chromedriver: {chromedriver_bin}")
    
    # Check if files exist
    if not os.path.exists(chrome_bin):
        print(f"❌ Chrome binary not found at {chrome_bin}")
        return False
    if not os.path.exists(chromedriver_bin):
        print(f"❌ Chromedriver not found at {chromedriver_bin}")
        return False
    
    # Start virtual display
    try:
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(1920, 1080))
        display.start()
        print("✅ Virtual display started")
    except Exception as e:
        print(f"❌ Virtual display failed: {e}")
        return False
    
    try:
        opts = Options()
        opts.binary_location = chrome_bin  # Use the exact Chrome binary
        
        # Headful mode - NO --headless flag
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        opts.add_argument("--window-size=1920,1080")
        
        # Use the exact chromedriver
        from selenium.webdriver.chrome.service import Service
        service = Service(chromedriver_bin)
        
        driver = webdriver.Chrome(service=service, options=opts)
        url = "https://ozon.kz/category/shiny-i-diski-8501/continental-18580188/?brand_was_predicted=true&deny_category_prediction=true&from_global=true&season=31827%2C33890&text=Continental&tirecondition=101129387"
    
        print(f"Testing: {url}")
        driver.get(url)
        time.sleep(15)  # Longer wait for headful
        
        print(f"Page title: {driver.title}")
        print(f"Current URL: {driver.current_url}")
        
        # Check for specific blocking indicators
        page_source = driver.page_source
        if "antibot" in page_source.lower():
            print("❌ BLOCKED: Anti-bot page detected")
            # Print first 500 chars of page source to see what's shown
            print("Page content preview:")
            print(page_source[:500])
        elif "Ozon" in page_source:
            print("✅ SUCCESS: Ozon page loaded!")
            # Print first 500 chars to see if it's the real site
            print("Page content preview:")
            print(page_source[:500])
        else:
            print("❓ UNKNOWN: Page loaded but doesn't look like Ozon")
            print("Page content preview:")
            print(page_source[:500])
        
        # Take screenshot as base64 for manual viewing
        screenshot_b64 = driver.get_screenshot_as_base64()
        print(f"📸 Screenshot (base64 - first 200 chars):")
        print(screenshot_b64[:200] + "...")
        driver.quit()
        display.stop()
        return True
        
    except Exception as e:
        print(f"❌ Headful failed: {e}")
        display.stop()
        return False


if __name__ == "__main__":
    print("🔍 Testing Ozon accessibility from Railway...")
    test_requests()
    test_selenium()
    test_selenium_headful()
    print("\n📊 All tests completed.")
