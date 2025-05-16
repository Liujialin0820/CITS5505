import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app  # ✅ 改为 app 包的统一入口
from exts import db
from apps.front.models import FrontUser

# ✅ 创建测试用 app，不需要传参数，只手动配置
@pytest.fixture
def test_app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'WTF_CSRF_ENABLED': False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
        db.session.remove()

# ✅ 创建客户端 fixture
@pytest.fixture
def client(test_app):
    return test_app.test_client()

# ✅ 注册功能测试：使用 /signup/ POST 表单
def test_signup_success(client):
    response = client.post('/signup/', data={
        'email': 'alice@example.com',
        'username': 'Alice',
        'stu_id': '11112222',
        'password1': 'Secret123',
        'password2': 'Secret123'
    }, follow_redirects=True)

    assert response.status_code == 200

    # ✅ 查询数据库中是否注册成功
    with client.application.app_context():
        user = FrontUser.query.filter_by(email='alice@example.com').first()
        assert user is not None
        assert user.username == 'Alice'
