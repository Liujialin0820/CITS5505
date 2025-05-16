import pytest
from app import create_app
from exts import db
from apps.cms.models import CMSUser

# ✅ Create a Flask test client for unit testing
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True  # Enable testing mode
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing

    with app.app_context():
        db.create_all()  # Create all tables in a clean test DB

        # ✅ Pre-insert a known admin user into the database if not already present
        if not CMSUser.query.filter_by(email='admin2@test.com').first():
            user = CMSUser(
                username='admin2',
                email='admin2@test.com',
                password='testpass'  # Note: assumes CMSUser hashes this internally
            )
            db.session.add(user)
            db.session.commit()

    # ✅ Provide a test client instance
    with app.test_client() as client:
        yield client

# ✅ Test case for successful admin login
def test_admin_login(client):
    login_data = {
        'email': 'admin2@test.com',
        'password': 'testpass',
        'remember': 1
    }

    # ✅ Send POST request to login route
    response = client.post('/cms/login/', data=login_data, follow_redirects=True)

    # ✅ Ensure HTTP 200 OK response
    assert response.status_code == 200

    # ✅ Verify login was successful by checking the response content
    assert b'Logout' in response.data or b'Dashboard' in response.data
