import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:huangqi861012@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.good_question = {
            'question': 'Who invented World Wide Web?',
            'answer': 'Tim Berners-Lee',
            'category': 4,
            'difficulty': 2
        }

        self.bad_question_wrong_datatype = {
            'question': 'Who invented World Wide Web?',
            'answer': 'Tim Berners-Lee',
            'category': 'science',
            'difficulty': 2
        }

        self.bad_question_missing_fields = {
            'question': "Who invented World Wide Web?",
            'answer': "Tim Berners-Lee"
        }

    def tearDown(self):
        pass

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_questions_without_arguments(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_get_questions_with_arguments(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))
        self.assertFalse(data['current_category'])

    def test_404_get_questions_with_nonexisting_page(self):
        res = self.client().get('/questions?page=9999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The requested resource is not found.")

    def test_delete_question_with_exsting_id(self):
        question = Question(
            question=self.good_question['question'],
            answer=self.good_question['answer'],
            category=self.good_question['category'],
            difficulty=self.good_question['difficulty']
        )
        question.insert()
        question_id = question.id

        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertFalse(Question.query.filter_by(id=question_id).one_or_none())

    def test_delete_question_with_nonexsting_id(self):
        res = self.client().delete('/questions/0')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The request can not be processed.")

    def test_add_valid_question(self):
        res = self.client().post('/questions', json=self.good_question)
        data = json.loads(res.data)
        question_id = int(data['created'])

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(Question.query.filter_by(id=question_id).one_or_none())

    def test_add_invalid_question_with_missing_fields(self):
        res = self.client().post('/questions', json=self.bad_question_missing_fields)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The request is not valid.")

    def test_add_invalid_question_with_wrong_datatype(self):
        res = self.client().post('/questions', json=self.bad_question_wrong_datatype)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The request can not be processed.")

    def test_search_questions_with_valid_search_term(self):
        res = self.client().post('/questions', json={'searchTerm': 'what'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertFalse(data['current_category'])

    def test_search_questions_with_empty_search_term(self):
        res = self.client().post('/questions', json={'searchTerm': ''})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The request can not be processed.")

    def test_add_invalid_question_without_search_term(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The request is not valid.")

    def test_get_questions_by_category_with_valid_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 1)

    def test_get_questions_by_category_with_invalid_category(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The requested resource is not found.")

    def test_get_questions_by_category_without_category(self):
        res = self.client().get('/categories//questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The requested resource is not found.")

    def test_play_quiz_with_valid_request_one_category(self):
        request = {
            'previous_questions': [],
            'quiz_category': {
                'id': 1,
                'type': 'science'
            }
        }
        res = self.client().post('/quizzes', json=request)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))

    def test_play_quiz_with_valid_request_all_categories(self):
        request = {
            'previous_questions': [],
            'quiz_category': {
                'id': 0,
                'type': 'click'
            }
        }
        res = self.client().post('/quizzes', json=request)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))

    def test_play_quiz_with_invalid_request(self):
        request = {
            'previous_questions': []
        }

        res = self.client().post('/quizzes', json=request)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The request is not valid.")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
