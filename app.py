import serial
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///item.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

arduino_serial = serial.Serial("COM6", 9600, timeout=1)

cors = CORS(app)


class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(255), nullable=False)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"id: {self.id}, text: {self.text}"


class TextSchema(ma.Schema):
    class Meta:
        fields = ('id', 'text')


text_schema = TextSchema()
text_schemas = TextSchema(many=True)


@app.route("/sendText", methods=["POST"])
def post_me():
    data = request.get_json()
    send_text(data)
    send_text_to_db(data)
    return 'Success', 200


@app.route("/text", methods=["GET"])
def get_me():
    text = Text.query.all()
    result = text_schemas.dump(text)
    return jsonify(result)


def send_text_to_db(text):
    if text == "clear":
        return
    data_set = {"text": text}
    json_dump = json.dumps(data_set)
    data = TextSchema().loads(json_dump)
    new_item = Text(**data)
    db.session.add(new_item)
    db.session.commit()

    return text_schema.jsonify(new_item)


def send_text(command):
    arduino_serial.write(command.encode())


db.create_all()
if __name__ == '__main__':
    app.run(use_reloader=False)
