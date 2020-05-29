from flask import Flask, jsonify

from recipeasy.controllers import ingredients_controller
from recipeasy.exceptions.BadRequestException import BadRequestException
from recipeasy.exceptions.NotFoundException import NotFoundException
from recipeasy.exceptions.RepositoryException import RepositoryException

import os


app = Flask(__name__)
app.register_blueprint(ingredients_controller.controller, url_prefix='/ingredients')
# TODO: recipes controller

@app.errorhandler(BadRequestException)
def handleBadRequestException(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(NotFoundException)
def handleNotFoundException(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(RepositoryException)
def handleRepositoryException(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response




if __name__ == '__main__':
    if 'AWS_ACCESS_KEY_ID' not in os.environ or 'AWS_SECRET_ACCESS_KEY' not in os.environ:
        print("Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables")
        exit(1)
    app.run()