# 🚀 Code Matrix - AI-Powered Online Judge Platform

[![Production Ready](https://img.shields.io/badge/Production-Ready-brightgreen)](#)
[![Django](https://img.shields.io/badge/Django-4.2.23-blue)](#)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](#)
[![AI Powered](https://img.shields.io/badge/AI-Gemini%202.0-orange)](#)
[![Live Demo](https://img.shields.io/badge/Live-Demo-success)](https://code-matrix-0ya4.onrender.com)

**Code Matrix** is a modern, AI-powered online judge platform that helps programmers practice competitive programming with intelligent assistance. Get instant hints, code analysis, and debugging help powered by Google's Gemini 2.0 Flash AI.

## 🌟 Features

### 🧠 AI-Powered Learning
- **Smart Hints**: Get algorithmic guidance without spoiling the solution
- **Code Analysis**: Understand why your solution failed
- **Debugging Help**: AI analyzes runtime errors and suggests fixes
- **Performance Tips**: Optimization suggestions for time limit exceeded cases

### 💻 Multi-Language Support
- **Python** - Full support with instant execution
- **C++** - Complete compilation and testing
- **C** - Traditional C programming support  
- **Java** - Object-oriented problem solving

### 🎯 Problem Management
- **15+ Active Problems** with varying difficulty levels
- **Comprehensive Test Cases** for thorough validation
- **Sample Test Cases** visible to users for understanding
- **Difficulty Levels**: Easy, Medium, Hard categorization

### 🔧 Development Features
- **Online Compiler**: Test code without submitting
- **Real-time Execution**: See results instantly
- **Progress Tracking**: Monitor your improvement
- **Clean UI/UX**: Responsive Bootstrap design

## 🚀 Quick Start

### Live Demo
Visit the live platform: **[code-matrix-0ya4.onrender.com](https://code-matrix-0ya4.onrender.com)**

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/Kartikey-M/Online-Judge-Project.git
cd Online-Judge-Project
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Environment Setup**
Create a `.env` file:
```env
DJANGO_SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key
DATABASE_URL=sqlite:///db.sqlite3
DEBUG=True
```

4. **Database Setup**
```bash
python manage.py migrate
python manage.py createsuperuser
```

5. **Run Development Server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to see Code Matrix in action!

## 🏗️ Architecture

Code Matrix follows a clean, modular architecture:

```
📁 Code Matrix
├── 🎯 judge/          # Core application (home, dashboard, compiler)
├── 📚 problems/       # Problem management system
├── 📝 submissions/    # Code submission and evaluation
├── 👤 accounts/       # User authentication and profiles
├── 🤖 ai_assistant/   # Gemini AI integration
├── 🎨 templates/      # Bootstrap-powered UI
└── ⚙️ static/         # CSS, JS, and assets
```

### Key Components
- **Django 4.2.23**: Robust web framework
- **PostgreSQL**: Production database
- **Google Gemini 2.0 Flash**: AI assistance
- **Bootstrap 5**: Modern, responsive UI
- **WhiteNoise**: Static file serving
- **Render.com**: Cloud deployment

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Production readiness check
python production_check.py

# Full system test (optional)
python system_test.py
```

**Current Status**: ✅ 7/7 production checks passed

## 🤖 AI Assistant

The AI assistant is powered by Google's Gemini 2.0 Flash and provides:

### 💡 Intelligent Hints
```python
# User struggling with "Two Sum" problem
AI Response: "Consider using a hash map to store numbers you've seen. 
As you iterate through the array, check if the complement 
(target - current number) exists in your hash map."
```

### 🔍 Code Analysis
```python
# For Wrong Answer verdicts
AI Response: "Your logic looks correct, but check edge cases. 
What happens when the array has duplicate numbers? 
Consider if your solution handles negative numbers properly."
```

### 🐛 Debugging Support
```python
# For Runtime Errors
AI Response: "The IndexError suggests you're accessing an array 
index that doesn't exist. Check your loop bounds and ensure 
you're not going beyond array length-1."
```

## 📊 Statistics

**Current Platform Status:**
- 🎯 **15 Active Problems** across all difficulty levels
- 📝 **9 Total Submissions** from users
- 👥 **3 Registered Users** and growing
- 🤖 **AI Assistant** integrated and operational
- 🔧 **Multi-language** execution engine working

## 🔒 Security

Code Matrix implements enterprise-level security:

- **Environment Variables**: All secrets externalized
- **CSRF Protection**: All forms secured
- **Input Sanitization**: User code safely executed
- **Sandboxed Execution**: Isolated code running
- **Time Limits**: Prevents infinite loops
- **Memory Limits**: Resource usage control

## 🚀 Deployment

### Production Environment
- **Platform**: Render.com with automatic deployments
- **Database**: PostgreSQL with connection pooling
- **Static Files**: WhiteNoise for efficient serving
- **SSL**: Automatic HTTPS with certificates
- **Environment**: Secure variable management

### Deploy Your Own
1. Fork this repository
2. Connect to Render.com
3. Set environment variables:
   - `DJANGO_SECRET_KEY`
   - `GEMINI_API_KEY`
   - `DATABASE_URL` (provided by Render)
4. Deploy automatically!

## 📚 Documentation

- **[High-Level Design](ARCHITECTURE.md)**: Complete system architecture
- **API Documentation**: Available in code comments
- **User Guide**: Built-in help sections
- **Admin Guide**: Django admin interface

## 🛠️ Development

### Adding New Problems
1. Access the Django admin panel
2. Create new Problem with description
3. Add test cases (sample and hidden)
4. Set difficulty and constraints
5. Activate the problem

### Extending AI Features
The AI assistant can be extended with new analysis types:
```python
# In ai_assistant/gemini_service.py
def analyze_memory_limit_exceeded(self, problem_title, user_code, language):
    # Add new AI analysis method
    pass
```

### Adding New Languages
1. Extend `judge/views.py` with new executor method
2. Add language option to forms
3. Update UI language selection
4. Test compilation and execution

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code style
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed
- Ensure all checks pass

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google AI**: For the powerful Gemini 2.0 Flash model
- **Django Team**: For the excellent web framework
- **Bootstrap**: For the beautiful UI components
- **Render.com**: For reliable hosting platform
- **Open Source Community**: For inspiration and support

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Kartikey-M/Online-Judge-Project/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Kartikey-M/Online-Judge-Project/discussions)
- **Email**: Open an issue for contact information

---

<div align="center">

**Built with ❤️ for the coding community**

[🌟 Star this repo](https://github.com/Kartikey-M/Online-Judge-Project/stargazers) if you find it helpful!

**[Try Code Matrix Now](https://code-matrix-0ya4.onrender.com)** 🚀

</div>
