import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
from werkzeug.exceptions import BadRequest
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    selection = questions[start:end]
    formatted_questions = [question.format() for question in selection]
    return formatted_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        # set up allowed headers and methods
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, DELETE, OPTIONS')
        return response

    @app.route('/categories')
    def get_all_categories():
        # handle get all categories
        categories = Category.query.order_by(Category.type).all()
        formatted_categories = {category.id: category.type for category in categories}
        response = {
            'success': True,
            'categories': formatted_categories
        }
        return jsonify(response)

    @app.route('/questions')
    def get_all_questions():
        # handle get all questions
        questions = Question.query.order_by(Question.id).all()
        formatted_questions = paginate_questions(request, questions)
        categories = Category.query.order_by(Category.type).all()
        formatted_categories = {category.id: category.type for category in categories}
        if len(formatted_questions) == 0:
            abort(404)
        else:
            response = {
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(questions),
                'categories': formatted_categories,
                'current_category': None
            }
        return jsonify(response)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        # handle delete question by id
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()
            if question is None:
                abort(422)
            else:
                question.delete()
                response = {
                    'success': True,
                    'deleted': question_id
                }
        except:
            abort(422)
        return jsonify(response)

    @app.route('/questions', methods=['POST'])
    def add_question():
        # handle add questions and search questions by title
        body = request.get_json()
        if 'question' in body and 'answer' in body and 'difficulty' in body and 'category' in body:
            try:
                question = body.get('question')
                answer = body.get('answer')
                difficulty = body.get('difficulty')
                category_id = body.get('category')

                new_question = Question(
                    question=question,
                    answer=answer,
                    difficulty=difficulty,
                    category=category_id
                )
                new_question.insert()
                response = {
                    'success': True,
                    'created': new_question.id
                }
            except:
                abort(422)
        elif 'searchTerm' in body:
            try:
                title = body.get('searchTerm')
                if title is None or title == '':
                    abort(422)
                questions = Question.query.filter(Question.question.ilike('%{}%'.format(title))).all()
                formatted_questions = [question.format() for question in questions]
                response = {
                    'success': True,
                    'questions': formatted_questions,
                    'total_questions': len(formatted_questions),
                    'current_category': None
                }
            except:
                abort(422)
        else:
            abort(400)
        return jsonify(response)

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        # handle get questions based on category
        try:
            category = Category.query.filter_by(id=category_id).one_or_none()
            if category is None:
                abort(404)
            else:
                questions = Question.query.filter_by(category=category_id).all()
                formatted_questions = [question.format() for question in questions]
                response = {
                    'success': True,
                    'questions': formatted_questions,
                    'total_questions': len(formatted_questions),
                    'current_category': category_id
                }
        except:
            abort(404)
        return jsonify(response)

    @app.route('/quizzes', methods=['POST'])
    def play():
        # handle get a new random question for the selected category/categories
        try:
            body = request.get_json()
            if 'quiz_category' not in body or 'previous_questions' not in body:
                abort(400)
            else:
                previous_questions = body.get('previous_questions')
                category = body.get('quiz_category')
            if 'id' not in category:
                abort(400)
            category_id = int(category.get('id'))
            if category_id == 0:
                questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter_by(category=category_id).filter(
                    Question.id.notin_(previous_questions)).all()

            if len(questions) == 0:
                new_question = None
            else:
                new_question = random.choice(questions).format()

            response = {
                'success': True,
                'question': new_question
            }
        except BadRequest:
            abort(400)
        except:
            abort(422)
        return jsonify(response)

    @app.errorhandler(400)
    def bad_request(error):
        # handle 404 error
        response = {
            'success': False,
            'error': 400,
            'message': "The request is not valid."
        }
        return jsonify(response), 400

    @app.errorhandler(404)
    def not_found(error):
        # handle 404 error
        response = {
            'success': False,
            'error': 404,
            'message': "The requested resource is not found."
        }
        return jsonify(response), 404

    @app.errorhandler(422)
    def not_processed(error):
        # handle 404 error
        response = {
            'success': False,
            'error': 422,
            'message': "The request can not be processed."
        }
        return jsonify(response), 422

    return app
