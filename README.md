# Blookie Website Tester 🧪

Automation testing framework for Blog Websites **Playwright** + **Pytest**.

## 📁 Cấu trúc

```
blog-website-tester/
├── config/         # Cấu hình (settings, environment)
├── core/           # Base page, browser factory, logger
├── pages/          # Page Object Models
│   └── locators/   # Element locators
├── tests/          # Test cases
├── utils/          # API client, data builder
├── screenshots/    # Screenshot khi test fail
├── reports/        # HTML reports
└── logs/           # Log files
```

## ⚡ Cài đặt

```bash
# 1. Tạo virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 2. Cài dependencies
pip install -r requirements.txt

# 3. Cài Playwright browsers
playwright install chromium
```

## 🔐 Cấu hình

Tạo file `.env`:

```env
TEST_ENV=local
TEST_USER_EMAIL=testuser@example.com
TEST_USER_PASSWORD=Test@12345

EXISTING_USER_EMAIL=user@gmail.com
EXISTING_USER_PASSWORD=pass

TEST_ADMIN_EMAIL=admin@gmail.com
TEST_ADMIN_PASSWORD=pass

HEADLESS=false
SLOW_MO=700
RECORD_VIDEO=true
LOG_LEVEL=INFO
```

## 🚀 Chạy Test

```bash
# Chạy tất cả tests
pytest

# Chạy với browser hiển thị
pytest --headed

# Chạy test cụ thể
pytest tests/test_auth.py -v
pytest tests/test_posts.py -v

# Chạy tất cả admin tests
pytest -m admin -v

# Chạy admin navigation tests
pytest tests/test_admin.py::TestAdminNavigation -v

# Chạy admin dashboard tests
pytest tests/test_admin.py::TestAdminDashboard -v

# Chạy admin users management tests
pytest tests/test_admin.py::TestAdminUsersManagement -v

# Chạy admin posts management tests
pytest tests/test_admin.py::TestAdminPostsManagement -v

# Chạy admin reports management tests
pytest tests/test_admin.py::TestAdminReportsManagement -v

# Chạy class cụ thể
pytest tests/test_auth.py::TestLogin -v
pytest tests/test_posts.py::TestPostCreation -v
pytest tests/test_newsfeed.py::TestPostCardVoting -v

# Chạy theo marker
pytest -m smoke
pytest -m "ui and auth"

# Chạy với HTML report
pytest --html=reports/report.html

# Chạy parallel (nhanh hơn)
pytest -n auto
```

## 📋 Markers

| Marker | Mô tả |
|--------|-------|
| `smoke` | Quick smoke tests |
| `regression` | Full regression suite |
| `auth` | Authentication tests |
| `posts` | Blog post tests |
| `comments` | Comment system tests |
| `profile` | User profile tests |
| `search` | Search functionality |
| `admin` | Admin panel tests |
| `api` | API-only tests |

## 🛠 Tech Stack

- Python 3.10+
- Playwright
- Pytest
- Pydantic (data validation)
- Faker (test data)
- pytest-html (reports)
- Allure (optional reports)

## Video Blookie Website
[!Video Demo](https://img.youtube.com/vi/GH6hzpp0xYk/maxresdefault.jpg)](https://www.youtube.com/watch?v=GH6hzpp0xYk)