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

|  UWA ID    |      Name       |------GitHub Username------|
|------------|-----------------|---------------------------|
|  24088207  |  Thant Sin Oo   |Thant-Sin-Oo|
|  24143148  |  Hongsui Zhu    |HongsuiZhu-11|
|  24236328  |  Jialin Liu     |Liujialin0820|
|  24322263  |  Jinho Jang     |Smithton7330|


## How to Launch the Application

```bash
# Clone the repository
git clone https://github.com/your-repo-url.git
cd your-repo-folder

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
flask run


## How to Run the Tests
This project includes a suite of automated tests to ensure key functionalities—such as user login, course preference handling, and admin features—work as expected.

To run the tests:

1. Activate your virtual environment:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows

    Run all test cases located in the tests/ directory:

python -m unittest discover -s tests

    If your project uses pytest, you can also run:

pytest

Make sure all dependencies are installed before running tests:

pip install -r requirements.txt







