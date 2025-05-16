import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from apps.front import create_app, db
from apps.front.models import FrontUser


# --- Fixtures: 启动测试应用 ---
@pytest.fixture
def test_app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(test_app):
    return test_app.test_client()


# --- 测试登录功能 ---
def test_student_login(client):
    # 创建用户并添加到数据库中
    user = FrontUser(username='Alice', email='alice@example.com', stu_id='11112222')
    user.password = 'Secret123'  # ✅ 注意是设置 password，不是 set_password()
    db.session.add(user)
    db.session.commit()

    # 发送登录请求
    response = client.post('/signin/', data={
        'email': 'alice@example.com',
        'password': 'Secret123'
    }, follow_redirects=True)

    # 检查返回内容
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["code"] == 200
