import google.generativeai as genai
from .config import settings

# Configure Gemini
genai.configure(api_key=settings.GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

parameters_used = {}

async def create_message(posts, profile_info=None):
    # Prepare context from posts and profile
    posts_context = "\n".join([
        f"Post {i+1}: {post['content']}" 
        for i, post in enumerate(posts)
    ])
    
    profile_context = ""
    if profile_info:
        profile_context = f"""
        Name: {profile_info.get('name', 'Not available')}
        Headline: {profile_info.get('headline', 'Not available')}
        """
    
    prompt = f"""
    Based on the following LinkedIn profile information and recent posts, create a personalized 2-line connection request message.
    The message should be friendly, professional, and reference specific details from their profile or posts.

    Profile Information:
    {profile_context}

    Recent Posts:
    {posts_context}

    Rules:
    1. Keep it to exactly 2 lines
    2. Make it personal and specific
    3. Reference their recent activity or role
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
        if len(message) > 200:
            message = message[:197] + "..."
            
        return message
    except Exception as e:
        print(f"Error generating message: {e}")
        return "Hi! I came across your profile and would love to connect. I'm particularly interested in your recent posts about your work and experiences."

def get_parameters_used():
    return parameters_used
