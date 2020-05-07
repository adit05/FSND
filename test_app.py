import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

ca_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE2UU1saTh3UWp1a2ZaWjhzbHpmdiJ9.eyJpc3MiOiJodHRwczovLzNkeS5hdXRoMC5jb20vIiwic3ViIjoiSlc3WDVOb29FYVNHQWxkaXpINEYxNFNSM2dQOEZlaW5AY2xpZW50cyIsImF1ZCI6Im1vdmllcyIsImlhdCI6MTU4ODc3Njc3NiwiZXhwIjoxNTg4ODYzMTc2LCJhenAiOiJKVzdYNU5vb0VhU0dBbGRpekg0RjE0U1IzZ1A4RmVpbiIsInNjb3BlIjoicmVhZDphY3RvcnMgcmVhZDptb3ZpZXMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWVzIl19.BIL_5W9Q90y8BMkZOtRg13i8ojgeq0_vn4UjJfdQ7vIzZ64atJVofK1B8mU6ABZjYsVvIqDdJLbLtI4P3NQKba4rRzfCoEfkrn7ZvnOdtO1xgs43o0_E7ZdCP-Bkq5xbANCfQlU___HhbZPlZ6RsOqXGVh7qZTvESusY95kVYsNayrXstoEjm4dwpJtwaC6PVVGtB80UWetzs0UYKuDaV0VTMew9L-DQqwBOv0R7bWalzhiqEDQbfphYSgdfBJQS9Oc_Ht79KqLnzTN9byDbUeAeJLXnxFi76cLbJ92zAbU6fc5D0jP3GkI8dip1dDoTHJVhs8EazYmyhVn8oOa_2w'
cd_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE2UU1saTh3UWp1a2ZaWjhzbHpmdiJ9.eyJpc3MiOiJodHRwczovLzNkeS5hdXRoMC5jb20vIiwic3ViIjoiSlc3WDVOb29FYVNHQWxkaXpINEYxNFNSM2dQOEZlaW5AY2xpZW50cyIsImF1ZCI6Im1vdmllcyIsImlhdCI6MTU4ODg2MjU4NiwiZXhwIjoxNTg4OTQ4OTg2LCJhenAiOiJKVzdYNU5vb0VhU0dBbGRpekg0RjE0U1IzZ1A4RmVpbiIsInNjb3BlIjoicmVhZDphY3RvcnMgcmVhZDptb3ZpZXMgcG9zdDphY3RvcnMgZGVsZXRlOmFjdG9ycyBwYXRjaDphY3RvcnMgcGF0Y2g6bW92aWVzIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwiZGVsZXRlOmFjdG9ycyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyJdfQ.SUM79IJa44CehFVby5ckj-9OdyqJDTKgnfnsf7YBJ1TxmHVb-gexJFDaV40ZEdZvBHFDmxEbDT6tFX2IY3LHv7D1rG5adb9kTBza-gYJ74DsbogLc-jYNCWw2deCXr5Ke8awxynYw6oNmpktk4Dky6EBCPDOm_KyuqMgqZ7hUUvAwu5YV0xfVcIMz0JiICVeDhPcL3mnCa7nab54CUxVdMR5Hl8bxnZlRNY4w5t-O8pGrjhxlPmHiKTum9F8ZEFwqIz8mtysqhTAEdp1OWY2X9NOK8pnpRdflHf7xPIFMBGdaiwZbIzn-MLKHIbfUlzKEF1SAmKFPnuQ2abmHhIjoQ'
ep_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE2UU1saTh3UWp1a2ZaWjhzbHpmdiJ9.eyJpc3MiOiJodHRwczovLzNkeS5hdXRoMC5jb20vIiwic3ViIjoiSlc3WDVOb29FYVNHQWxkaXpINEYxNFNSM2dQOEZlaW5AY2xpZW50cyIsImF1ZCI6Im1vdmllcyIsImlhdCI6MTU4ODgxMjE2MywiZXhwIjoxNTg4ODk4NTYzLCJhenAiOiJKVzdYNU5vb0VhU0dBbGRpekg0RjE0U1IzZ1A4RmVpbiIsInNjb3BlIjoicmVhZDphY3RvcnMgcmVhZDptb3ZpZXMgcG9zdDptb3ZpZXMgcG9zdDphY3RvcnMgZGVsZXRlOm1vdmllcyBkZWxldGU6YWN0b3JzIHBhdGNoOmFjdG9ycyBwYXRjaDptb3ZpZXMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWVzIiwicG9zdDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIl19.Co8Wu6qFHTPfiBoYh4F6WcUx_GZadiWKE7h4VD2OF58K_2BRmYSb9q79ntSci0gzirCk1Up14g94UOgEAZYa7eha7WV6FdaEyH7hGel2gL7_xNeXA-ztfLTzVEo4T0XFnJLwGHnhT9qPBVZ5WH4kmneh5zUSS-T9xzRZmd2wIZJhqwb4uuRnVv69cgXAJLjUlLH6S3OHqhosxbRYf4jxhGq0FzBhYwcZDJ5cF0J1N9Fs1yK0-ObT_HSsl51sL4DgjaeRRw3TjRJwetGR9i3Q-R_57PqjNw30jUZSta8IZIhupbnpTB2LQNBTHZ5uBJjm4NRzXt4nDy9uUQhYqgnKEw'

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
        # self.assertEqual(data['actor_list'], [])
        # self.assertTrue(data['number_of_actors'])

    def test_get_movies(self):
        res = self.client().get('/movies', headers={"Authorization": "Bearer {}".format(ca_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        #self.assertTrue(['movie_list'])
        #self.assertTrue(data['number_of_movies'])

    def test_ca_post_to_actors_unauthorized(self):
        res = self.client().post('/actors', headers={"Authorization": "Bearer {}".format(ca_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_ca_post_to_movies_unauthorized(self):
        res = self.client().post('/movies', headers={"Authorization": "Bearer {}".format(ca_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_cd_post_to_actors(self):
        res = self.client().post('/actors', headers={"Authorization": "Bearer {}".format(cd_token)}, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor_list'])
        self.assertTrue(data['created_id'])
        self.assertTrue(data['number_of_actors'])

    def test_cd_delete_to_actors(self):
        insert_res = self.client().post('/actors', headers={"Authorization": "Bearer {}".format(cd_token)}, json=self.new_actor)
        insert_data = json.loads(insert_res.data)
        actor_id = insert_data['created_id']

        res = self.client().delete(f'/actors/{actor_id}', headers={"Authorization": "Bearer {}".format(cd_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['number_of_actors'])

    def test_cd_post_to_movies_unauthorized(self):
        res = self.client().post('/movies', headers={"Authorization": "Bearer {}".format(cd_token)}, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
