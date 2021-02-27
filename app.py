from flask import Flask, make_response, jsonify, request
from flask.views import MethodView
from flask_pymongo import PyMongo
from bson import json_util
from flask_cors import CORS


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/Imperva'
CORS(app)

data = PyMongo(app)


class CustomerAPI(MethodView):
    def get(self, customer_id):
        if customer_id is not None:
            print(customer_id)
            res = data.db.Customers.find({'_id': int(customer_id)})
            return make_response(jsonify({'data': json_util.loads(json_util.dumps(res))}), 200)
        res = data.db.Customers.find()
        return make_response({'data': json_util.loads(json_util.dumps(res))}, 200)


app.add_url_rule("/customer/", view_func=CustomerAPI.as_view("customers"), defaults={'customer_id': None})
app.add_url_rule("/customer/<customer_id>/", view_func=CustomerAPI.as_view("customer"))


class FilmAPI(MethodView):
    def get(self, film_id):
        if film_id is not None:
            res = data.db.Films.find({'_id': int(film_id)})
            res2 = data.db.Customers.find({'Rentals': {'$elemMatch': {'filmId': int(film_id)}}})
            return make_response(jsonify({'data': json_util.loads(json_util.dumps(res)), 'customers': json_util.loads(json_util.dumps(res2))}), 200)
        res = data.db.Films.find()
        return make_response({'data': json_util.loads(json_util.dumps(res))}, 200)


app.add_url_rule("/film/", view_func=FilmAPI.as_view("films"), defaults={'film_id': None})
app.add_url_rule("/film/<film_id>/", view_func=FilmAPI.as_view("film"))

if __name__ == '__main__':
    app.run(debug=True)
