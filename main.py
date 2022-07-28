from flask import jsonify
from flask_migrate import Migrate

from app import app, banco
from models.usuario import UserModel

Migrate(app, banco)


@app.shell_context_processor
def shell_context_processor():
    return dict(
        app=app,
        banco=banco,
        UserModel=UserModel
    )