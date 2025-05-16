# CITS5505 Group Project

## Project Title: Course Scheduler Tool

This is a web-based class management and scheduling tool built with Flask.

It allows university students to:

- Select and manage course preferences
- View automatically generated timetables
- Share personalised schedules with peers

Admins can manage courses and class time slots via a dedicated CMS.

The platform is designed for ease of use, visual clarity, and scheduling flexibility.

## 🚀 Features Overview

### 👋 Introduction / Login

- Landing page for user login or registration.
- Admin login page is separate from student login.

### 🎯 Dashboard

- Displays important instructions for students.
- Includes upcoming course events.

### 📥 Course Preference Page

- Allows students to select from existing courses or add new ones.
- Preferences are stored and later reflected in timetable view.

### 📅 Weekly Timetable

- Auto-generates a personalized calendar view of selected course slots.
- Each class block displays subject name, type, time, and location.

### 🔁 Share Schedule

- Users can share their timetable with selected users in the system.

### 🔐 Profile & Settings

- Users can update profile info and change password.

### 🛠 Admin CMS

- Admin can:
  - Add new courses.
  - Create and manage time slots.
  - View how many students are enrolled in each course.

---

## Group Memebers

| UWA ID   | Name         | ------GitHub Username------ |
| -------- | ------------ | --------------------------- |
| 24088207 | Thant Sin Oo | Thant-Sin-Oo                |
| 24143148 | Hongsui Zhu  | HongsuiZhu-11               |
| 24236328 | Jialin Liu   | Liujialin0820               |
| 24322263 | Jinho Jang   | Smithton7330                |

## How to Launch the Application

```bash

# Clone the repository
git clone https://github.com/Liujialin0820/CITS5505.git
cd CITS5505

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database 
flask db init
flask db migrate -m "comment"
flask db upgrade

# Run the Flask app
flask run


# test 
1. use front_end_selenium_test.side in firefox selenium ide
2. run test file in terminal
python -m pytest .\tests\test_student_signup.py
python -m pytest .\tests\test_student_login.py
python -m pytest .\tests\test_admin_login.py
python -m pytest .\tests\test_admin_add_course.py
python -m pytest tests/test_message_unit.py








```
