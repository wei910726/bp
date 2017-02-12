from django.test import TestCase, Client
from django.contrib.auth.models import User
from poll.models import Event, Guest
from datetime import datetime

# Create your tests here.


class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id=6, name="Oneplus 3 event", status=True, limit=6000, address="shenzhen", start_time='2017-07-01 09:00:00')
        Guest.objects.create(id=4, event_id=6, realname='Jim', phone='15677998800', email='6767@89.com', sign=False)

    def test_event_model(self):
        result=Event.objects.get(name='Oneplus 3 event')
        self.assertEqual(result.address, 'shenzhen')
        self.assertTrue(result.status)

    def test_guest_model(self):
        result=Guest.objects.get(phone='15677998800')
        self.assertEqual(result.realname, 'Jim')
        self.assertFalse(result.sign)


class IndexTest(TestCase):
    def test_index(self):
        response = self.client.get('/index/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'index.html')


class LoginTest(TestCase):
    def setUp(self):
        User.objects.create_user('aa', '7056@111.com', 'abcabc6789')
        self.c = Client()

    def test_login_nouser(self):
        testdata = {'username': '', 'password': ''}
        response = self.c.post('/login_action/', data=testdata)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_wrong(self):
        testdata = {'username': 'mm', 'password': '12123333'}
        response = self.c.post('/login_action/', data=testdata)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_right(self):
        testdata = {'username': 'gab', 'password': 'pypy1234'}
        response = self.c.post('/login_action/', data=testdata)
        self.assertEqual(response.status_code, 302)


class  GuestManageTest(TestCase):
    def setUp(self):
        Event.objects.create(id=6, name="Oneplus 3 event", status=True, limit=6000, address="shenzhen", start_time='2017-07-01 09:00:00')
        Guest.objects.create(id=4, event_id=6, realname='Jim', phone='15677998800', email='6767@89.com', sign=False)
        self.c = Client()
    def test_guest(self):
        response = self.c.post('/guest_manage/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Jim', response.content)
        self.assertIn(b'', response.content)