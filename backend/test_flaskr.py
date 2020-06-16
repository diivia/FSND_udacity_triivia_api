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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_category = {
            'type': 'Sport'}

        self.new_question = {
            'question': 'Anansi Boys',
            'answer': 'Neil Gaiman',
            'category': '5',
            'difficulty': 5}


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['current_category'], None)
        self.assertTrue(len(data['categories']))

    def test_get_paginated_questions_none_existing_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))

    def test_delete_question(self):
        total_questions_before = len(Question.query.all())
        question = Question(question="Answer to the Ultimate Question of Life, the Universe, and Everything", answer="42", category='1', difficulty=1)
        question.insert()
        total_questions_after_insert = len(Question.query.all())
        res = self.client().delete(f'/questions/{question.id}')
        total_questions_after_delete = len(Question.query.all())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question_id'], question.id)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))
        self.assertTrue(total_questions_before < total_questions_after_insert)
        self.assertTrue(total_questions_after_insert > total_questions_after_delete)


    def test_add_question(self):
        total_questions_before = len(Question.query.all())
        res = self.client().post('/questions', json={'question': "Answer to the Ultimate Question of Life, the Universe, and Everything",
                                                     'answer': "42",
                                                     'category': '1',
                                                     'difficulty': 1})
        total_questions_after = len(Question.query.all())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Question successfully created!')
        self.assertTrue(total_questions_before < total_questions_after)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
