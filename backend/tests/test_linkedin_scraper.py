import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from app.linkedin_scraper import get_profile_data, scrape_posts

@pytest.mark.asyncio
async def test_profile_scraping(mocker):
    # Mock Selenium WebDriver
    mock_driver = mocker.Mock()
    mock_element = mocker.Mock()
    
    # Mock successful login
    mock_driver.find_element.return_value = mock_element
    mock_element.send_keys = mocker.Mock()
    mock_element.click = mocker.Mock()
    
    # Mock profile data
    mock_posts = [
        mocker.Mock(text="Test post 1"),
        mocker.Mock(text="Test post 2")
    ]
    mock_driver.find_elements.return_value = mock_posts
    
    # Test successful scraping
    result = await get_profile_data(
        "test@example.com",
        "password123",
        "https://linkedin.com/in/testuser"
    )
    
    assert isinstance(result, dict)
    assert "posts" in result
    assert "profile_info" in result

@pytest.mark.asyncio
async def test_login_failure(mocker):
    # Mock Selenium WebDriver with login failure
    mock_driver = mocker.Mock()
    mock_driver.find_element.side_effect = NoSuchElementException()
    
    with pytest.raises(Exception) as exc_info:
        await get_profile_data(
            "test@example.com",
            "wrong_password",
            "https://linkedin.com/in/testuser"
        )
    
    assert "Login failed" in str(exc_info.value)

@pytest.mark.asyncio
async def test_profile_not_found(mocker):
    # Mock Selenium WebDriver
    mock_driver = mocker.Mock()
    mock_driver.get.side_effect = TimeoutException()
    
    with pytest.raises(Exception) as exc_info:
        await get_profile_data(
            "test@example.com",
            "password123",
            "https://linkedin.com/in/nonexistent"
        )
    
    assert "Profile not found" in str(exc_info.value)

@pytest.mark.asyncio
async def test_scrape_posts(mocker):
    # Mock Selenium WebDriver and elements
    mock_driver = mocker.Mock()
    
    # Mock post elements
    class MockPostElement:
        def __init__(self, text, timestamp):
            self.text = text
            self.timestamp = timestamp
            
        def find_element(self, by, value):
            if "break-words" in value:
                mock_elem = mocker.Mock()
                mock_elem.text = self.text
                return mock_elem
            elif "sub-description" in value:
                mock_elem = mocker.Mock()
                mock_elem.text = self.timestamp
                return mock_elem
            
    mock_posts = [
        MockPostElement("Test post 1", "1d ago"),
        MockPostElement("Test post 2", "2d ago"),
        MockPostElement("Test post 3", "1w ago")
    ]
    
    # Mock WebDriverWait and expected_conditions
    mock_wait = mocker.patch('selenium.webdriver.support.ui.WebDriverWait')
    mock_wait.return_value.until.return_value = mock_posts
    
    # Test post scraping
    posts = await scrape_posts(mock_driver)
    
    assert len(posts) == 3
    assert posts[0]["content"] == "Test post 1"
    assert posts[0]["timestamp"] == "1d ago"

@pytest.mark.asyncio
async def test_empty_posts(mocker):
    # Mock Selenium WebDriver with no posts
    mock_driver = mocker.Mock()
    mock_driver.find_elements.return_value = []
    
    posts = await scrape_posts(mock_driver)
    
    assert isinstance(posts, list)
    assert len(posts) == 0

@pytest.mark.asyncio
async def test_invalid_url_format():
    with pytest.raises(ValueError) as exc_info:
        await get_profile_data(
            "test@example.com",
            "password123",
            "not-a-valid-url"
        )
    
    assert "Invalid LinkedIn URL" in str(exc_info.value)

@pytest.mark.asyncio
async def test_network_error(mocker):
    # Mock Selenium WebDriver with network error
    mock_driver = mocker.Mock()
    mock_driver.get.side_effect = Exception("Network error")
    
    with pytest.raises(Exception) as exc_info:
        await get_profile_data(
            "test@example.com",
            "password123",
            "https://linkedin.com/in/testuser"
        )
    
    assert "Failed to access LinkedIn" in str(exc_info.value)

@pytest.mark.asyncio
async def test_rate_limiting(mocker):
    # Mock Selenium WebDriver with rate limiting response
    mock_driver = mocker.Mock()
    mock_driver.page_source = "You've reached the limit of page requests"
    
    with pytest.raises(Exception) as exc_info:
        await get_profile_data(
            "test@example.com",
            "password123",
            "https://linkedin.com/in/testuser"
        )
    
    assert "Rate limited by LinkedIn" in str(exc_info.value) 