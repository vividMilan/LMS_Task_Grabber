# LMS Task Grabber 🎓

## 🌐 Overview

It is repetitive to check for assignment due and sometimes I notice there is a assignment due before 2 - 3 days. So I built this application

## 🔧 Features

- Login to LMS
- Extracts Assignments
- Stores database in SQLite databse
- Reminds assignment due dates
- Periodically checks for assignments and any due dates are nearby

## 🛠 Tech Stack

| Technology | Purpose |
| ---------- | ------- |
| PyQt6 | Desktop application development |
| Playwright | Scraping LMS |
| SQLite | Stores assignments |
| SQLAlchemy | ORM |
| Keyring | Storing LMS credentials |
| Pytest | Testing application |

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/vividMilan/LMS_Task_Grabber.git
```

### 2. CD into project directory

```bash
cd LMS_Task_Grabber
```

### 3. Install python dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Change the environment variables

```env
LMS_USERNAME=
LMS_PASSWORD=
LMS_URL=www.campus.lms.com
```

**Please do not change LMS USERNAME and LMS PASSWORD variables**

### 4. Run the application

```bash
python -m src.main
```

## ⚠ Please keep these in mind

- The scraping script is written for my university LMS, so it not guaranteed to work on any LMS
- This is still in development, further features will be added and deployed soon
