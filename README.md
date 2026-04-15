# E-commerce UI Test Automation
A simple project containing end-to-end UI tests for a demo e-commerce web application using Playwright and Pytest.

The project focuses on practicing automated web testing, working with locators, and handling dynamic elements on the page.
Tested application: https://automationexercise.com

## Technologies
- Python
- Playwright
- Pytest
---
## Features
- User registration (positive scenario)
- User login (positive scenario)
- Add and remove product from cart (positive scenario)
- Basic purchase flow (checkout + payment)
- Basic handling dynamic elements (cookies, popups)
  
---
## Testing
This project includes automated UI tests using Playwright and Pytest:
- Positive test scenarios (valid user actions)
- User flow testing (login, cart, basic checkout steps)
- UI validation using assertions (element visibility, text content)
- Reusable helper functions for common actions (login, add to cart)
  
---
## Setup and Instalation
### 1. Clone a repository
```bash
git clone https://github.com/PavlinaCp/ecommerce-playwright-tests.git
cd ecommerce-playwright-tests
```
### 2. Install dependencies
```bash
pip. install -r requierements.txt
```
### 3. Install Playwright browsers
```bash
playwright install
```
### 4. Run tests
```bash
pytest
```
---
## Configuration
- Test execution is configured using `pytest.ini`
- Default browser is set to Chromium
- Test are executed with verbose output for better readability
- Custom test file naming is configured (python.py)
