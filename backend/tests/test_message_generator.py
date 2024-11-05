import pytest
from app.message_generator import create_message

@pytest.mark.asyncio
async def test_message_generation():
    posts = [
        {"content": "Test post 1", "timestamp": "1d"},
        {"content": "Test post 2", "timestamp": "2d"}
    ]
    profile_info = {"name": "Test User"}
    
    message = await create_message(posts, profile_info)
    assert isinstance(message, str)
    assert len(message) > 0 