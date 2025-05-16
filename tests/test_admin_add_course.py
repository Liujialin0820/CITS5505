import pytest
from app import create_app
from exts import db
from config import Config
from apps.common.models import CourseModel
from apps.cms.models import CMSUser

# ✅ Pytest fixture to initialize the app and test client
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True              # Enable testing mode
    app.config['WTF_CSRF_ENABLED'] = False    # Disable CSRF protection for tests

    with app.app_context():
        db.create_all()  # Create all database tables

        # ✅ Insert a mock admin user for login simulation
        if not db.session.get(CMSUser, 1):
            admin = CMSUser(id=1, username="admin", email="admin@test.com", password="testpass")
            db.session.add(admin)
            db.session.commit()

    with app.test_client() as client:
        # ✅ Simulate logged-in admin session
        with client.session_transaction() as sess:
            sess[Config.CMS_USER_ID] = 1
        yield client

# ✅ Unit test to verify that an admin can add a course
def test_add_course(client):
    course_data = {
        'name': 'Software Engineering'
    }

    # Send a POST request to add a course
    response = client.post('/cms/acourse/', data=course_data, follow_redirects=True)
    assert response.status_code == 200

    # ✅ Verify that the course has been saved to the database
    with client.application.app_context():
        course = CourseModel.query.filter_by(name='Software Engineering').first()
        assert course is not None
