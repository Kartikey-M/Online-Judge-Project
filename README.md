# Online Judge Platform

A Django-based online judge platform for competitive programming practice and contests.

## Features

- User registration and authentication
- Problem browsing and management
- Code submission and automatic judging
- Multi-language support (Python, C++, C, Java)
- Real-time verdict updates
- User statistics and leaderboards
- Responsive web interface

## Supported Languages

- Python 3
- C++ (g++)
- C (gcc)
- Java (javac/java)

## Quick Setup

### 1. Install Python
Make sure you have Python 3.8+ installed on your system.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the platform.

## Project Structure

```
online_judge/
├── manage.py
├── requirements.txt
├── online_judge/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── judge/                 # Main app with dashboard
├── problems/              # Problem management
├── submissions/           # Code execution and judging
├── accounts/              # User management
├── templates/             # HTML templates
└── static/               # CSS, JS, images
```

## Admin Panel

Access the admin panel at `http://127.0.0.1:8000/admin/` to:
- Add new problems
- Manage test cases
- View submissions
- Manage users

## Adding Problems

1. Go to the admin panel
2. Add a new Problem with:
   - Title and description
   - Time limit (seconds)
   - Memory limit (MB)
   - Difficulty level
3. Add test cases for the problem:
   - Input data
   - Expected output

## System Requirements

- Python 3.8+
- GCC compiler (for C/C++)
- Java JDK (for Java support)
- At least 1GB RAM
- 5GB disk space

## Security Notes

- Code execution is sandboxed with time and memory limits
- User code runs in isolated processes
- File system access is restricted

## Development

To contribute or modify:

1. Fork the repository
2. Create a virtual environment
3. Install dependencies
4. Make changes
5. Test thoroughly
6. Submit pull request

## Troubleshooting

### Common Issues

1. **Database errors**: Run `python manage.py migrate`
2. **Static files not loading**: Run `python manage.py collectstatic`
3. **Compiler not found**: Install GCC and Java JDK
4. **Permission errors**: Check file permissions

### Debug Mode

To enable debug mode, set `DEBUG = True` in `settings.py`. 
**Never use debug mode in production!**

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the code documentation
3. Create an issue with detailed information

## Future Enhancements

- Contest management
- Advanced statistics
- Plagiarism detection
- Docker integration
- API endpoints
- Mobile app support
