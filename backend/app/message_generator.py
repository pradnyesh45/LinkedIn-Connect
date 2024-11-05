import google.generativeai as genai
from .config import settings

# Configure Gemini
genai.configure(api_key=settings.GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

parameters_used = {}

async def create_message(posts, profile_info=None):
    # Prepare context from posts
    posts_context = "\n".join([
        f"Post {i+1}: {post['content']}" 
        for i, post in enumerate(posts)
    ])
    
    # Prepare prompt
    prompt = f"""
    Based on the following LinkedIn posts and profile information, create a personalized 2-line connection request message.
    The message should be friendly, professional, and reference specific details from their posts.

    Posts:
    {posts_context}

    Profile Info:
    {profile_info if profile_info else 'Not available'}

    Rules:
    1. Keep it to exactly 2 lines
    2. Make it personal and specific
    3. Reference their recent activity or interests
    4. Keep it professional
    5. Don't exceed 200 characters
    """

    # Store parameters
    global parameters_used
    parameters_used = {
        "model": "gemini-pro",
        "num_posts_analyzed": len(posts),
        "prompt_length": len(prompt),
        "profile_info_included": bool(profile_info)
    }

    try:
        response = model.generate_content(prompt)
        message = response.text.strip()
        
        # Ensure it's not too long
        if len(message) > 300:
            message = message[:297] + "..."
            
        return message
    except Exception as e:
        print(f"Error generating message: {e}")
        return "Hi! I came across your profile and would love to connect. I'm particularly interested in your recent posts about your work and experiences."

def get_parameters_used():
    return parameters_used
