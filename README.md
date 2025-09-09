# QA Automation Intern Assignment

This repository contains API and UI automation test cases for the QA Automation Intern role, as per the provided assignment.

## 📁 Project Structure

QA Automation Intern Assignment/                             
├── tests/                                                                  
│   ├── api_tests.py      
│   └── ui_tests.py        
├── requirements.txt       
└── README.md              


## How to Set Up & Run

### 1. Install Dependencies

Ensure you have Python 3.13.4 installed. Then, run:

```bash
pip install -r requirements.txt
```

### 2. Run API Tests

```bash
pytest tests/api_tests.py
```

> Make sure your internet is active and no VPN is blocking `https://reqres.in`.  
> This project uses the free API key:
```http
x-api-key: reqres-free-v1
```

### 3. Run UI Tests

Ensure you have ChromeDriver installed and accessible in your PATH:

```bash
python tests/ui_tests.py
```

> Headless Chrome browser is used for automation on `https://www.iamdave.ai`.


## Test Design Summary

This test suite is designed to ensure both API and UI components meet quality standards through thorough validation and automation.

- ✅ API Tests
    - Designed using `pytest` for structured and scalable testing.
    - Validate successful responses (status code 200), correct JSON data, and error handling (e.g. 404, 400).
    - Covered different HTTP methods (GET, POST).
    - Included negative test cases like missing fields and non-existent users.
    - Used Reqres public API with API key header (`x-api-key`).

- ✅ UI Tests
    - Built using `unittest` with `Selenium WebDriver` for browser automation.
    - Covered key visual elements like title, images (logo), and headings.
    - Validated navigational flow such as clicking on the "About" link.
    - Implemented visibility and interactivity checks with `WebDriverWait` for dynamic content.
    - Tests are designed to work in headless mode using Chrome for CI/CD compatibility.

Each test was designed with clarity, reliability, and reusability in mind, simulating how real users interact with APIs and UI components.

## Notes

- Selenium tests run in **headless mode** using ChromeDriver, suitable for CI environments.
- API tests are implemented using `pytest` and `requests`.
