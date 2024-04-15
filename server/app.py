from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game, Bakery, BakedGood  # Import Bakery and BakedGood models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

@app.route('/games')
def games():
    games = []
    for game in Game.query.all():
        game_dict = game.to_dict()
        games.append(game_dict)

    response = make_response(
        games,
        200
    )

    return response

@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()

    game_dict = game.to_dict()

    response = make_response(
        game_dict,
        200
    )

    return response

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'GET':
        reviews = []
        for review in Review.query.all():
            review_dict = review.to_dict()
            reviews.append(review_dict)

        response = make_response(
            reviews,
            200
        )

        return response
    elif request.method == 'POST':
        new_review = Review(
            score=request.form.get("score"),
            comment=request.form.get("comment"),
            game_id=request.form.get("game_id"),
            user_id=request.form.get("user_id"),
        )

        db.session.add(new_review)
        db.session.commit()

        review_dict = new_review.to_dict()

        response = make_response(
            review_dict,
            201
        )

        return response

@app.route('/reviews/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def review_by_id(id):
    review = Review.query.filter(Review.id == id).first()

    if review == None:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(response_body, 404)

        return response
    else:
        if request.method == 'GET':
            review_dict = review.to_dict()

            response = make_response(
                review_dict,
                200
            )

            return response
        elif request.method == 'PATCH':
            for attr in request.form:
                setattr(review, attr, request.form.get(attr))

            db.session.add(review)
            db.session.commit()

            review_dict = review.to_dict()

            response = make_response(
                review_dict,
                200
            )

            return response
        elif request.method == 'DELETE':
            db.session.delete(review)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Review deleted."
            }

            response = make_response(
                response_body,
                200
            )

            return response

@app.route('/users')
def users():
    users = []
    for user in User.query.all():
        user_dict = user.to_dict()
        users.append(user_dict)

    response = make_response(
        users,
        200
    )

    return response

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    new_baked_good = BakedGood(
        name=request.form.get("name"),
        description=request.form.get("description"),
        bakery_id=request.form.get("bakery_id"),
        price=request.form.get("price")
    )

    db.session.add(new_baked_good)
    db.session.commit()

    baked_good_dict = new_baked_good.to_dict()

    response = make_response(
        baked_good_dict,
        201
    )

    return response

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()

    if bakery is None:
        response_body = {
            "message": "This bakery does not exist in our database. Please try again."
        }
        response = make_response(response_body, 404)
        return response
    else:
        for attr in request.form:
            setattr(bakery, attr, request.form.get(attr))

        db.session.add(bakery)
        db.session.commit()

        bakery_dict = bakery.to_dict()

        response = make_response(
            bakery_dict,
            200
        )

        return response

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.filter(BakedGood.id == id).first()

    if baked_good is None:
        response_body = {
            "message": "This baked good does not exist in our database. Please try again."
        }
        response = make_response(response_body, 404)
        return response
    else:
        db.session.delete(baked_good)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Baked good deleted."
        }

        response = make_response(
            response_body,
            200
        )

        return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
