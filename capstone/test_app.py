import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, db_drop_and_create_all, Actor, Movie, db_drop_and_create_all, database_path
from config import auth_header
from sqlalchemy import desc
from datetime import date

# Create authorization header for casting_staff and casting_director.
# casting_staff has only get:actors and get:movies permission
# casting_director has all the permissions.

casting_staff = {
    'Authorization': auth_header['casting_staff']
}
casting_director = {
    'Authorization': auth_header['casting_director']
}


#----------------------------------------------------------------------------#
# Setup of Unittest
#----------------------------------------------------------------------------#

class CastingTestCase(unittest.TestCase):
    def setUp(self):
        """
        Define test variables and initialize app.
        """
        self.app = create_app()
        self.client = self.app.test_client        
        self.database_path = database_path
        setup_db(self.app, self.database_path)
        db_drop_and_create_all()        
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)        
            self.db.create_all()
    
    def tearDown(self):
        """
        Executed after reach test
        """
        pass


#----------------------------------------------------------------------------#
# Tests for /actors POST
#----------------------------------------------------------------------------#

    def test_post_new_actor(self):       
        new_actor = {
            'name' : 'actor4',
            'age' : 40,
            'gender': 'male'
        } 

        res = self.client().post('/actors', json = new_actor, headers = casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])
    
    def test_post_new_actor_without_authorization(self):
        new_actor = {
            'name' : 'actor4',
            'age' : 40,
            'gender': 'male'
        } 

        res = self.client().post('/actors', json = new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_post_new_actor_without_actor_name(self):
        new_actor = {
            'age' : 40
        } 

        res = self.client().post('/actors', json = new_actor, headers = casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Actor''s name is required.')

#----------------------------------------------------------------------------#
# Tests for /actors GET
#----------------------------------------------------------------------------#

    def test_get_all_actors(self):        
        res = self.client().get('/actors?page=1', headers = casting_staff)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actors'])

    def test_get_all_actors_without_authorization(self):       
        res = self.client().get('/actors?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_get_all_actors_with_invalid_page_number(self):        
        res = self.client().get('/actors?page=99999', headers = casting_staff)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'No actors found in database.')

#----------------------------------------------------------------------------#
# Tests for /actors PATCH
#----------------------------------------------------------------------------#

    def test_update_actor(self):        
        actor_to_update = {
            'age' : 30
        } 
        res = self.client().patch('/actors/1', json = actor_to_update, headers = casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actor'])
        self.assertTrue(data['updated'])

    def test_update_actor_without_actor_info(self):            
            res = self.client().patch('/actors/1', headers = casting_director)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 400)
            self.assertFalse(data['success'])
            self.assertEqual(data['message'] , 'Request does not contain a valid JSON body.')

    def test_update_actor_with_invalid_actor_id(self):        
        actor_to_update = {
            'age' : 30
        } 
        res = self.client().patch('/actors/99999', json = actor_to_update, headers = casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Actor does not exist.')

#----------------------------------------------------------------------------#
# Tests for /actors DELETE
#----------------------------------------------------------------------------#

    def test_delete_actor(self):        
        res = self.client().delete('/actors/1', headers = casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['deleted'])

    def test_delete_actor_without_authorization(self):        
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_delete_actor_without_permission(self):        
        res = self.client().delete('/actors/1', headers = casting_staff)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_actor_with_invalid_actor_id(self):        
        res = self.client().delete('/actors/99999', headers = casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Actor does not exist.')

#----------------------------------------------------------------------------#
# Tests for /movies POST
#----------------------------------------------------------------------------#

    def test_post_new_movie(self):
        new_movie = {
            'title' : 'movie3',
            'release_date' : date.today()
        } 

        res = self.client().post('/movies', json = new_movie, headers = casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])

    def test_post_new_movie_without_movie_title(self):
        new_movie = {
            'release_date' : date.today()
        } 

        res = self.client().post('/movies', json = new_movie, headers = casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Movie''s title is required.')

#----------------------------------------------------------------------------#
# Tests for /movies GET
#----------------------------------------------------------------------------#

    def test_get_all_movies(self):        
        res = self.client().get('/movies?page=1', headers = casting_staff)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['movies'])

    def test_get_all_movies_without_authorization(self):       
        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_get_movies_with_invalid_page_number(self):        
        res = self.client().get('/movies?page=99999', headers = casting_staff)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'No movies found in database.')

#----------------------------------------------------------------------------#
# Tests for /movies PATCH
#----------------------------------------------------------------------------#

    def test_update_movie(self):        
        movie_to_update = {
            'release_date' : date.today()
        } 
        res = self.client().patch('/movies/1', json = movie_to_update, headers = casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['movie'])

    def test_update_movie_without_movie_info(self):        
        res = self.client().patch('/movies/1', headers = casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Request does not contain a valid JSON body.')

    def test_update_movie_with_invalid_movie_id(self):        
        movie_to_update = {
            'release_date' : date.today()
        } 
        res = self.client().patch('/movies/99999', json = movie_to_update, headers = casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Movie does not exist.')

#----------------------------------------------------------------------------#
# Tests for /movies DELETE
#----------------------------------------------------------------------------#

    def test_delete_movie(self):        
        res = self.client().delete('/movies/1', headers = casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['deleted'])
    
    def test_delete_movie_without_authorization(self):        
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_delete_movie_without_permission(self):        
        res = self.client().delete('/movies/1', headers = casting_staff)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_movie_with_invalid_movie_id(self):        
        res = self.client().delete('/movies/99999', headers = casting_director) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Movie does not exist.')


if __name__ == "__main__":
    unittest.main()