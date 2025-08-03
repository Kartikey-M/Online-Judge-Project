# Code Matrix

**Code Matrix** is a modern, AI-powered online judge platform built with Python and Django. It's designed for competitive programming enthusiasts to practice problem-solving, test their coding skills, and get intelligent feedback on their solutions.

## ✨ Key Features

- **User Authentication**: Secure registration and login system.
- **Problem Library**: Browse, filter, and solve a wide range of coding challenges.
- **Multi-Language Support**: Submit solutions in Python, C++, C, and Java.
- **Instant Judging**: Get real-time verdicts on your submissions (Accepted, Wrong Answer, TLE, etc.).
- **AI-Powered Assistant (New!)**:
    - **Get Hints**: Stuck on a problem? The AI can provide a helpful hint to guide you.
    - **Analyze Failures**: If your code fails, the AI can analyze your solution against failed test cases and suggest fixes.
    - **Powered by Gemini**: Utilizes Google's powerful Gemini AI for high-quality assistance.
- **Personalized Dashboard**: Track your progress, view submission history, and see performance stats.
- **Responsive UI**: A clean, modern, and mobile-friendly interface.

## 🚀 Quick Setup

### 1. Prerequisites
- Python 3.8+
- Git

### 2. Clone & Setup
```bash
# Clone the repository
git clone https://github.com/your-username/Code-Matrix.git
cd Code-Matrix

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory and add your Gemini API key:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Database Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Run the Server
```bash
python manage.py runserver
```
The platform will be available at `http://127.0.0.1:8000`.

## 🤖 AI Assistant Integration

The AI features are powered by Google's Gemini. To use them, you need a Gemini API key with access to the "Gemini 1.5 Flash" model.

- **Hint Generation**: On any problem page, click "Get AI Hint" for a nudge in the right direction.
- **Failure Analysis**: After a submission fails, you'll have an option to let the AI analyze your code and explain what went wrong.

## 📂 Project Structure

```
Code-Matrix/
├── manage.py
├── requirements.txt
├── .env                 # For API keys
├── online_judge/        # Main Django project
├── judge/               # Core app for dashboard and judging
├── problems/            # Problem management
├── submissions/         # Submission handling
├── accounts/            # User authentication
├── ai_assistant/        # Gemini AI integration
├── templates/           # HTML files
└── static/              # CSS, JS, images
```

## 🛠️ Admin Panel

Access the admin panel at `http://127.0.0.1:8000/admin/` to:
- Manage problems and test cases
- View all submissions
- Manage users

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/YourFeature`).
6. Open a pull request.

## 📜 License

This project is open source and available under the MIT License.
