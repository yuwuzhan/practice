import unittest
from app import create_app, db
from app.models import User, Role
from flask import url_for
import re

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue('我的朋友' in response.get_data(as_text=True))

    def test_register_and_login(self):
        #注册新用户
        response = self.client.post(url_for('auth.register'), data={
            'email': 'wwwaaa@example.com',
            'username': '余武展',
            'password': 'weewadsad',
            'password2': 'weewadsad'})
        self.assertTrue(response.status_code == 302)

        #使用新用户登陆
        response = self.client.post(url_for('auth.login'), data={
            'email': 'wwwaaa@example.com',
            'password': 'weewadsad'
        },follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue(re.search('你好,\s+余武展!', data))
        self.assertTrue('你还没确认您的请求' in data)

        #发送确认令牌
        user = User.query.filter_by(email='wwwaaa@example.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token),
                                   follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('您已确认您的请求~' in data)

        #退出
        response = self.client.get(url_for('auth.logout'),
                                   follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have been logged out' in data)

