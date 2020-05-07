import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

ca_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE2UU1saTh3UWp1a2ZaWjhzbHpmdiJ9.eyJpc3MiOiJodHRwczovLzNkeS5hdXRoMC5jb20vIiwic3ViIjoiSlc3WDVOb29FYVNHQWxkaXpINEYxNFNSM2dQOEZlaW5AY2xpZW50cyIsImF1ZCI6Im1vdmllcyIsImlhdCI6MTU4ODc3Njc3NiwiZXhwIjoxNTg4ODYzMTc2LCJhenAiOiJKVzdYNU5vb0VhU0dBbGRpekg0RjE0U1IzZ1A4RmVpbiIsInNjb3BlIjoicmVhZDphY3RvcnMgcmVhZDptb3ZpZXMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWVzIl19.BIL_5W9Q90y8BMkZOtRg13i8ojgeq0_vn4UjJfdQ7vIzZ64atJVofK1B8mU6ABZjYsVvIqDdJLbLtI4P3NQKba4rRzfCoEfkrn7ZvnOdtO1xgs43o0_E7ZdCP-Bkq5xbANCfQlU___HhbZPlZ6RsOqXGVh7qZTvESusY95kVYsNayrXstoEjm4dwpJtwaC6PVVGtB80UWetzs0UYKuDaV0VTMew9L-DQqwBOv0R7bWalzhiqEDQbfphYSgdfBJQS9Oc_Ht79KqLnzTN9byDbUeAeJLXnxFi76cLbJ92zAbU6fc5D0jP3GkI8dip1dDoTHJVhs8EazYmyhVn8oOa_2w'


class ActorsMoviesTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "actors_movies_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_actor = {
            'name': 'Jim Carey',
            'age': '58',
            'gender': 'male'
        }

        self.new_movie = {
            'title': 'The Matrix',
            'release_date': 'March 31, 1999'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors(self):
        res = self.client().get('/actors', headers={"Authorization": "Bearer {}".format(ca_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        #self.assertEqual(data['actor_list'], [])
        #self.assertTrue(data['number_of_actors'])

    def test_get_movies(self):
        res = self.client().get('/movies', headers={"Authorization": "Bearer {}".format(ca_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        #self.assertTrue(['movie_list'])
        #self.assertTrue(data['number_of_movies'])

    def ca_post_to_actors(self):
        res = self.client().post('/actors', headers={"Authorization": "Bearer {}".format(ca_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
