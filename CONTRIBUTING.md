# Contributing to Student Performance Analytics Dashboard

Thank you for considering contributing to this project! Here are some guidelines to help you get started.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/student-analytics-app.git
   cd student-analytics-app
   ```

3. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Set up the development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 📝 How to Contribute

### Reporting Bugs
- Use the GitHub issue tracker
- Describe the bug in detail
- Include steps to reproduce
- Mention your environment (OS, Python version, browser)

### Suggesting Features
- Open an issue with the tag "enhancement"
- Explain the feature and its benefits
- Provide examples if possible

### Code Contributions

#### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and small

#### Testing
Before submitting:
1. Test your changes thoroughly
2. Ensure the app runs without errors
3. Test with different data sets
4. Check browser compatibility (Chrome, Firefox, Safari)

#### Commit Messages
- Use clear, descriptive commit messages
- Format: `type: subject` (e.g., `feat: add export to CSV`)
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`

## 🔍 Areas for Contribution

### High Priority
- [ ] Add more ML models (SVM, Neural Networks)
- [ ] Implement user authentication
- [ ] Add database support (SQLite/PostgreSQL)
- [ ] Create unit tests
- [ ] Add data validation on upload

### Medium Priority
- [ ] Dark mode theme
- [ ] More chart types (radar, heatmap)
- [ ] Export to more formats (JSON, XML)
- [ ] Internationalization (i18n)
- [ ] Mobile responsive improvements

### Low Priority
- [ ] Additional statistical tests
- [ ] Custom color themes
- [ ] Animation improvements
- [ ] Performance optimizations

## 📚 Documentation
- Update README.md if you add features
- Add docstrings to new functions
- Update API documentation
- Include inline comments for complex code

## 🧪 Pull Request Process

1. **Update documentation** as needed
2. **Test thoroughly** on your local machine
3. **Create a pull request** with:
   - Clear title and description
   - Reference any related issues
   - Screenshots if UI changes
   - List of changes made

4. **Code review**: Maintainers will review your PR
5. **Address feedback** if requested
6. **Merge**: Once approved, your PR will be merged

## 📋 Development Setup Tips

### Running in Development Mode
```bash
export FLASK_ENV=development  # On Windows: set FLASK_ENV=development
python app.py
```

### Testing with Sample Data
The app includes a sample data generator. Use the "Load Sample Data" button in the UI or:
```python
from app import get_sample_data
df = get_sample_data()
```

### Debugging
- Use Flask's debug mode for auto-reload
- Check browser console for JS errors
- Use Python debugger (pdb) for backend issues

## 🤝 Community Guidelines

- Be respectful and constructive
- Help others learn and grow
- Give credit where it's due
- Have fun and be creative!

## 📧 Questions?

If you have questions, feel free to:
- Open an issue for discussion
- Reach out to maintainers
- Join our community discussions

Thank you for contributing! 🎉
