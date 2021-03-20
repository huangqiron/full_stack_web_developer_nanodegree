import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# db_drop_and_create_all()

## ROUTES
@app.route('/drinks')
def get_drinks():
    '''
    It will get drinks without authorization.
    '''
    try:
        drinks = Drink.query.all()
        return jsonify({
            'success': True,
            'drinks': [drink.short() for drink in drinks]
        })
    except:
        abort(404)


@app.route("/drinks-detail")
@requires_auth('get:drinks-detail')
def get_drink_detail(jwt):
    '''
    It will get details of drinks. 
    It can be accessed only for registered users.
    '''
    try:
        drinks = Drink.query.all()
        return jsonify({
            'success': True,
            'drinks': [drink.long() for drink in drinks]
        })
    except:
        abort(404)


@app.route("/drinks", methods=['POST'])
@requires_auth('post:drinks')
def add_drink(jwt):
    '''
    It will add a new drink.
    It can be accessed only for managers.
    '''
    body = request.get_json()
    if not ('title' in body and 'recipe' in body):
        abort(422)
    title = body.get('title')
    recipe = body.get('recipe')
    try:
        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': [drink.long()],
        })
    except:
        abort(422)


@app.route("/drinks/<id>", methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, id):
    '''
    It will update the details of drinks.
    It can be accessed only for managers
    '''
    drink = Drink.query.get(id)
    if drink:
        try:
            body = request.get_json()
            title = body.get('title')
            recipe = body.get('recipe')
            if title:
                drink.title = title
            if recipe:
                drink.title = recipe
            drink.update()
            return jsonify({
                'success': True,
                'drinks': [drink.long()]
            })
        except:
            abort(422)
    else:
        abort(404)



@app.route("/drinks/<id>", methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    '''
    It will remove a drink from database.
    It can be accessed only for managers.
    '''
    drink = Drink.query.get(id)
    if drink:
        try:
            drink.delete()
            return jsonify({
                'success': True,
                'delete': id
            })
        except:
            abort(422)
    else:
        abort(404)
        


# Error Handling
@app.errorhandler(422)
def unprocessable(error):
    '''
    It handles unprocessable requests.
    '''
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    '''
    It handles errors that requested resource is not found.
    '''
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    '''
    It handles errors that the user has no authorization for requested operations.
    '''
    return jsonify({
        "success": False,
        "error": ex.status_code,
        'message': ex.error
    }), 401
