# LinkedIn Connect

AI application to send a personalised message while sending connection request on LinkedIn.

> Note: Due to my extensive testing during development with multiple login attempts, LinkedIn now requires additional security checks (like CAPTCHA) on my personal account only. This won't affect you - your account will work normally without these security prompts.

## Video Demo

You can view the demo of the application [here](https://drive.google.com/file/d/1FNk22TzJP2ka9TzmBKQvJ1PnXqBb1QMf/view?usp=sharing).

## Local Setup (MacOS)

### Backend Setup

1. **Navigate to backend directory**

   ```bash
   cd backend
   ```

2. **Create a Python virtual environment** (optional but recommended)

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Create .env file**

   ```bash
   GOOGLE_API_KEY=your_google_palm_api_key
   ```

   Get your API key from [Google MakerSuite](https://makersuite.google.com/app/apikey)

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Backend**
   ```bash
   python3 -m uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**

   ```bash
   cd frontend
   ```

2. **Install Dependencies**

   ```bash
   npm install
   ```

3. **Run the Frontend**
   ```bash
   npm start
   ```
   The application will be available at `http://localhost:3000`

## Docker Setup (⚠️ Currently Not Working)

> Note: Docker setup is currently experiencing issues with ChromeDriver in the container environment. Please use the local setup instead.

## API Documentation

Visit `http://localhost:8000/docs` for the interactive Swagger documentation.

### Health Check

**Endpoint:** `GET /api/health`

### Generate LinkedIn Message

**Endpoint:** `POST /api/generate-message`

**Request:**

```json
{
  "username": "your-linkedin-email@example.com",
  "password": "your-linkedin-password",
  "target_profile_url": "https://www.linkedin.com/in/profile-url/"
}
```

**Response:**

```json
{
  "profile_info": {
    "name": "Shobhit Gupta",
    "headline": "Building Co-pilots to boost ROAS"
  },
  "posts": [
    {
      "content": "Good work ethics are so underrated.",
      "timestamp": "21h • Edited • \n 21 hours ago"
    },
    {
      "content": "OpenAI has started putting a tracker for AI generated images...",
      "timestamp": "4d • \n 4 days ago"
    }
    // ... more posts
  ],
  "message": "Hi Shobhit, I appreciate your insights on the importance of work ethics. As someone who values collaboration, I'd love to connect with a professional building co-pilots for improved ROAS.",
  "parameters_used": {
    "model": "gemini-pro",
    "num_posts_analyzed": 5,
    "prompt_length": 1195,
    "profile_info_included": true
  }
}
```

## Cost Analysis (30 days, 5 queries/day)

### Infrastructure Costs:

1. **Server (AWS t2.micro in Mumbai Region)**:

   - $0.0116 per hour × ₹83 = ₹0.96 per hour
   - ₹0.96 × 24 hours × 30 days = ₹700/month

2. **Chrome Instance**:

   - Memory usage: ~500MB per scrape
   - 5 queries/day = negligible additional cost on t2.micro

3. **Gemini API**:

   - ₹0.021 per 1K characters (Gemini Pro)
   - Average prompt ~1200 characters
   - 5 queries/day _ 30 days _ 1200 characters = 180K characters/month
   - Monthly cost: ~₹3.78

4. **Frontend Hosting (Vercel/Netlify)**:
   - Free tier is sufficient for this usage

### Total Monthly Cost Estimate: ₹700-800/month

- Includes server costs and overhead
- Based on AWS Asia Pacific (Mumbai) region pricing and Gemini API pricing
- Assumes basic monitoring and logging

## Credits and Resources Used

### Tools & Libraries

- FastAPI for backend API development
- React (Create React App) for frontend
- Selenium for web scraping

### AI Assistance

- Cursor IDE with Claude AI for code suggestions and debugging
- ChatGPT for code assistance and troubleshooting
