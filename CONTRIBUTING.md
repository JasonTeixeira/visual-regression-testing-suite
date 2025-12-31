# Contributing to Visual Regression Testing Suite

Thank you for your interest in contributing! This guide will help you get started with contributing to this project.

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Chrome browser
- Git
- Percy account (free tier available at [percy.io](https://percy.io))

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/JasonTeixeira/visual-regression-testing-suite.git
   cd visual-regression-testing-suite
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Percy token**
   ```bash
   export PERCY_TOKEN=your_percy_token_here
   ```

5. **Run tests locally**
   ```bash
   # Run without Percy (functional tests only)
   pytest tests/ -v
   
   # Run with Percy (visual regression)
   npx percy exec -- pytest tests/ -m visual -v
   ```

## 📝 Making Changes

### Branching Strategy

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Urgent production fixes

### Creating a Feature Branch

```bash
git checkout -b feature/my-new-feature develop
```

### Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semi-colons, etc)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(homepage): add visual test for mobile viewport
fix(base-page): correct wait timeout for slow networks
docs(readme): update installation instructions
test(checkout): add test for payment form validation
```

## 🧪 Writing Tests

### Test Structure

Tests should follow this structure:

```python
@pytest.mark.visual
def test_descriptive_name(driver, base_url):
    """
    Clear docstring explaining what this test does and why
    """
    # Arrange - Set up test conditions
    driver.set_window_size(1920, 1080)
    page = HomePage(driver, base_url)
    
    # Act - Perform the action being tested
    page.navigate()
    page.prepare_for_visual_snapshot()
    
    # Assert - Verify the results
    percy_snapshot(driver, 'Test Name - Desktop')
    assert page.is_loaded()
```

### Best Practices for Visual Tests

1. **Hide Dynamic Content**
   - Always hide timestamps, live counters, rotating banners
   - Use the `hide_dynamic_elements()` method from page objects

2. **Wait for Page Stability**
   - Wait for images to load
   - Wait for fonts to load
   - Wait for animations to complete

3. **Use Descriptive Snapshot Names**
   ```python
   # ❌ Bad
   percy_snapshot(driver, 'test1')
   
   # ✅ Good
   percy_snapshot(driver, 'Homepage - Desktop 1920x1080 - Hero Section')
   ```

4. **Test Multiple Viewports**
   - Desktop: 1920x1080, 1366x768
   - Tablet: 1024x768, 768x1024
   - Mobile: 375x667, 414x896

5. **Use Pytest Markers**
   ```python
   @pytest.mark.visual          # Visual regression test
   @pytest.mark.smoke           # Quick smoke test
   @pytest.mark.critical        # Critical path test
   @pytest.mark.skip("Reason")  # Skip temporarily
   ```

### Adding New Page Objects

When adding new page objects:

1. Inherit from `BasePage`
2. Define locators as class attributes
3. Implement navigation and interaction methods
4. Add `prepare_for_visual_snapshot()` method
5. Document all methods with docstrings

Example:

```python
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class ProductPage(BasePage):
    """Page object for product detail page"""
    
    # Locators
    PRODUCT_IMAGE = (By.CSS_SELECTOR, ".product-image")
    ADD_TO_CART_BTN = (By.ID, "add-to-cart")
    PRICE = (By.CSS_SELECTOR, ".product-price")
    
    def __init__(self, driver, base_url="https://www.example.com"):
        super().__init__(driver)
        self.base_url = base_url
    
    def add_to_cart(self):
        """Add product to shopping cart"""
        self.click(self.ADD_TO_CART_BTN)
    
    def prepare_for_visual_snapshot(self):
        """Prepare page for visual testing"""
        self.wait_for_page_load()
        self.hide_dynamic_elements()
```

## 🔍 Code Review Process

### Before Submitting a PR

- [ ] All tests pass locally
- [ ] Code follows project style (PEP 8)
- [ ] New code has tests
- [ ] Documentation is updated
- [ ] Commit messages follow conventions
- [ ] No merge conflicts with target branch

### Submitting a Pull Request

1. **Push your branch**
   ```bash
   git push origin feature/my-new-feature
   ```

2. **Create Pull Request**
   - Use a clear, descriptive title
   - Fill out the PR template
   - Link any related issues
   - Request reviews from maintainers

3. **PR Description Should Include:**
   - What changed and why
   - Screenshots (for visual changes)
   - Testing performed
   - Any breaking changes

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] Manual testing performed

## Screenshots (if applicable)
Percy build: [link]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

## 🐛 Reporting Bugs

### Before Reporting

1. Check if the issue already exists
2. Try to reproduce with the latest code
3. Gather relevant information (OS, Python version, etc.)

### Bug Report Template

```markdown
**Describe the bug**
Clear description of what the bug is

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected behavior**
What you expected to happen

**Screenshots**
If applicable

**Environment:**
- OS: [e.g. macOS 13.0]
- Python Version: [e.g. 3.9.10]
- Browser: [e.g. Chrome 120]

**Additional context**
Any other relevant information
```

## 💡 Suggesting Enhancements

We welcome suggestions for improvements! Please:

1. Check if the enhancement was already suggested
2. Clearly describe the enhancement
3. Explain why it would be useful
4. Provide examples if possible

## 📚 Documentation

### Updating Documentation

- README.md - High-level overview and quick start
- CONTRIBUTING.md - This file
- Code comments - Explain "why", not "what"
- Docstrings - All public methods must have docstrings

### Docstring Style

```python
def method_name(self, param1, param2):
    """
    Brief description of what this method does
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ExceptionType: When this exception is raised
    """
```

## 🎨 Code Style

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use meaningful variable names
- Add comments for complex logic

### Linting

Run linters before committing:

```bash
# Format code
black pages/ tests/

# Check style
flake8 pages/ tests/

# Type checking
mypy pages/ tests/
```

## 🔒 Security

### Reporting Security Issues

**DO NOT** open a public issue for security vulnerabilities.

Instead:
1. Email security concerns to: [your-email]
2. Include "SECURITY" in the subject line
3. Provide detailed description
4. We'll respond within 48 hours

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## 🤝 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community

**Unacceptable behavior includes:**
- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

## ❓ Questions?

- **Documentation:** Check README.md first
- **Issues:** Browse existing issues
- **Discussions:** Start a discussion in the repo
- **Contact:** Reach out to maintainers

## 🙏 Thank You!

Thank you for contributing to making visual regression testing better for everyone!

---

**Remember:** Every contribution matters, no matter how small. Whether it's fixing a typo, improving documentation, or adding a major feature - we appreciate it all!
