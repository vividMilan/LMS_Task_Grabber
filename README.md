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

1. Download the latest release under releases

2. Configure Username, Password and LMS URL under settings

## ⚠ Please keep these in mind

- The scraping script is written for my university LMS, so it not guaranteed to work on any LMS
- This is still in development, further features will be added and deployed soon
