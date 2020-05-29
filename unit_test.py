import os
import unittest

#from import app, db, mail
from server import app, conn

TEST_DB = 'pythosqlite.db'


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['BASEDIR'] = "C:\\xampp\\htdocs\\blogstop"
        app.config['SQLALCHEMY_DATABASE_URI'] = os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()

        # Disable sending emails during unit testing
        #mail.init_app(app)
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

###############
#### tests ####
###############

    # Case 1: Registering
    def user(self, username, password, email):
      return self.app.post('/register', json={"username":username, "password": password, "email": email}, follow_redirects=True)

    def test_user_failed(self):
      response = self.user("new_user", "asdf", "test@gmail.com")
      self.assertEqual(response.status_code, 200)
      self.assertIn(b'{"returned":0}', response.data)  #already existing email id

    def test_user_success(self):
      response = self.user('new_user', 'new_pass', 'newguy@gmail.com') #new user, hence should be successful.
      self.assertEqual(response.status_code, 200)
      self.assertIn(b'{}', response.data)

    # case 2: Checking login
    def user_login(self, username, password):
      return self.app.post('/login', json={"username":username, "password": password}, follow_redirects=True)

    def test_login_failed(self):
      response = self.user_login("random", "random_pass") #user, pass combination doesn't exist
      self.assertEqual(response.status_code, 200)
      self.assertIn(b'{"returned":0}', response.data)

    def test_login_success(self):
      response = self.user_login('vishal', 'pwd') #user just been added after first test case hence must be successful
      self.assertEqual(response.status_code, 200)
      self.assertIn(b'{"returned":1}', response.data)

    # case 3: to check if user exists
    def check_user(self, uname):
      return self.app.get('/check', query_string=dict(username=uname))

    def test_user_exists_failed(self):
      response = self.check_user(uname = "dont_exist")
      self.assertEqual(response.status_code, 200)      
      self.assertIn(b'{"returned":0}', response.data)

    def test_user_exists_success(self):
      response = self.check_user(uname = "vishal")
      self.assertEqual(response.status_code, 200)      
      self.assertIn(b'{"returned":1}', response.data)

    # case 4: checking tag recommendation

    def get_tags(self, content):
      return self.app.get('/blogstop/recommendtags', query_string=dict(content=content))

    def test_tags_success1(self):
      mystr = "Football is a game that millions of people around the world play and love. It can be called a universal game because every small and big nation plays it. Moreover, it’s a great relaxer, stress reliever, teacher of discipline and teamwork. Apart from that, it keeps the body and mind fit and healthy. It’s a team game that makes it a more enjoyable game as it teaches people the importance of sportsmanship. Leadership, and unity."
      response = self.get_tags(content = mystr)
      self.assertEqual(response.status_code, 200)      
      self.assertIn(b'Sports;Fitness', response.data) #this is sports and fitness category hence success

    def test_tags_success2(self):
      mystr = "Political influences certainly play a major role in influencing Fashion. Many politicians become fashion symbols. Notable examples are First Lady Jacqueline Kennedy and Princess Diana. Also, political revolutions make a huge impact on the Fashion trend. For example, in 1960’s America, liberal clothing styles became popular among the younger generation. This was due to the Liberal revolution. Another significant factor which influences Fashion trend is technology. There certainly has been a rapid growth of technology in the Fashion industry. For example, wearable technology has become a popular Fashion trend. Furthermore, 3D printing technology and the internet have also made an impact on Fashion. Social influences are probably the strongest influences on the Fashion trend. Many music stars strongly influence Fashion choice. For example, wearing hoodies became famous due to rap musicians. Furthermore, movie and television actors create a big impact on Fashion. Many youngsters love to emulate the Fashion sense of their favourite celebrity"
      response = self.get_tags(content = mystr)
      self.assertEqual(response.status_code, 200)      
      self.assertIn(b'Fashion;Political', response.data) #this is not sports and fitness hence fail 

    # case 5: getting profile details
    def check_profile(self, uname):
      return self.app.get('/profile', query_string=dict(username=uname))

    def test_profile_details_success1(self):
      response = self.check_profile(uname = "vishal")
      self.assertEqual(response.status_code, 200)      
      self.assertIn( b'{"email":"v@gmail.com","likes":10,"num":4,"posts":"1;2;3;8","username":"vishal"}', response.data)

    def test_profile_details_success2(self):
      response = self.check_profile(uname = "sparsha")
      self.assertEqual(response.status_code, 200)      
      self.assertIn(b'{"email":"sp@gmail.com","likes":19,"num":2,"posts":"4;5","username":"sparsha"}', response.data)

    # case 6: checkign if update api works fine
    def test_update(self):
      response = self.app.get('/blogstop/update', query_string=dict(username="vishal", postid=67, date="29/05/2020"))
      self.assertEqual(response.status_code, 200)      
      self.assertIn( b'{}', response.data)

    # case 7: update likes

    def test_update_likes(self):
      response = self.app.get('/like_update', query_string=dict(username="testing"))
      self.assertEqual(response.status_code, 200)      
      self.assertIn( b'{}', response.data)

    # case 8 : testing sentiment analysis api for positive and negative reviews
    def test_pos_neg(self):
      response = self.app.get('/posneg', query_string=dict(username="vishal", text = "Amazing;;That was amazing;;Disappointed;;"))
      self.assertEqual(response.status_code, 200)      
      self.assertIn( b'{"neg":1,"pos":2}', response.data)

    # case 9 : 
    def get_statistics(self):
      response = self.app.get('/get_details', query_string=dict(username="vishal"))
      self.assertEqual(response.status_code, 200)
      self.assertIn(b'{}', response.data)

    

if __name__ == "__main__":
    unittest.main()
