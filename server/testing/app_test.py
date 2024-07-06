import flask

from app import app
from models import User

app.secret_key = b'a\xdb\xd2\x13\x93\xc1\xe9\x97\xef2\xe3\x004U\xd1Z'

class TestApp:
    '''Flask API in app.py'''

    def test_logs_user_in(self):
        '''logs user in by username and adds user_id to session at /login.'''
        with app.test_client() as client:
            
            client.get('/clear')

            user = User.query.first()
            response = client.post('/login', json={
                'username': user.username
            })
            response_json = response.get_json()

            assert(response.content_type == 'application/json')
            assert(response.status_code == 200)
            assert(response_json['id'] == user.id)
            assert(response_json['username'] == user.username)
            assert(flask.session.get('user_id') == user.id)

    def test_logs_user_out(self):
        '''removes user_id from session at /logout.'''
        with app.test_client() as client:
            
            client.get('/clear')

            user = User.query.first()
            client.post('/login', json={
                'username': user.username
            })

            response = client.delete('/logout')
            
            assert(response.status_code == 204)
            assert(not response.data)

    