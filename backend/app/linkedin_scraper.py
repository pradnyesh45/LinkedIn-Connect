from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

async def get_profile_data(username: str, password: str, profile_url: str):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # Login to LinkedIn
        driver.get("https://www.linkedin.com/login")
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "[type=submit]").click()
        
        # Navigate to profile
        driver.get(profile_url)
        
        # Get basic profile info
        profile_info = {}
        try:
            profile_info["name"] = driver.find_element(By.CSS_SELECTOR, "h1.RIbnCAsTbWzbdDScQkPGXRrQHSaITKZWQhh").text
            profile_info["headline"] = driver.find_element(By.CSS_SELECTOR, "div.text-body-medium.break-words").text
                
        except:
            pass
            
        # Get posts
        posts = []
        try:
            # Directly navigate to the posts page
            posts_url = f"{profile_url}recent-activity/all/"
            driver.get(posts_url)
            time.sleep(5)
            
            # Now get the posts
            post_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 
                    "div.feed-shared-update-v2"))
            )
            
            # Get last 5 posts
            for element in post_elements[:5]:
                try:
                    # First find the description wrapper
                    desc_wrapper = element.find_element(By.CSS_SELECTOR, 
                        "div.feed-shared-update-v2__description-wrapper")
                    
                    # Then get the content from within the wrapper
                    content = desc_wrapper.find_element(By.CSS_SELECTOR, 
                        "div.update-components-text span.break-words").text
                    
                    # Get timestamp from the actor component
                    timestamp = element.find_element(By.CSS_SELECTOR, 
                        "span.update-components-actor__sub-description").text
                    
                    posts.append({
                        "content": content,
                        "timestamp": timestamp
                    })
                except Exception as e:
                    continue
        except:
            pass
            
        return {
            "posts": posts,
            "profile_info": profile_info
        }
    
    finally:
        driver.quit()
