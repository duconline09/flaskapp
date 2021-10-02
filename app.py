import datetime

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)


class Captions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text())
    date = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, title, body):
        self.title = title
        self.body = body


class CaptionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'date')


caption_schema = CaptionSchema()
captions_schema = CaptionSchema(many=True)


@app.route('/')
@app.route('/get', methods=['GET'])
def get_captions():  # put application's code here
    all_captions = Captions.query.all()
    results = captions_schema.dump(all_captions)
    return jsonify(results)


@app.route('/get/<id>', methods=['GET'])
def get_caption(id):
    caption = Captions.query.get(id)
    return caption_schema.jsonify(caption)


@app.route('/add', methods=['POST'])
def add_caption():
    title = request.json['title']
    body = request.json['body']

    captions = Captions(title, body)
    db.session.add(captions)
    db.session.commit()
    return caption_schema.jsonify(captions)


@app.route('/update/<id>', methods=['PUT'])
def update_caption(id):
    caption = Captions.query.get(id)

    title = request.json['title']
    body = request.json['body']

    caption.title = title
    caption.body = body

    db.session.commit()
    return caption_schema.jsonify(caption)


@app.route('/delete/<id>', methods=['DELETE'])
def delete_caption(id):
    caption = Captions.query.get(id)

    db.session.delete(caption)
    db.session.commit()
    return caption_schema.jsonify(caption)


if __name__ == '__main__':
    app.run(debug=True)
