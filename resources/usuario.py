from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import jwt_required


atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help='The field "login" cannot be left blank')
atributos.add_argument('senha', type=str, required=True, help='The field "senha" cannot be left blank')


class User(Resource):
    # /usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404

    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An error ocurred trying to delete hotel.'}, 500
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404


class UserRegister(Resource):
    # /cadastro
    @staticmethod
    def post():
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'message': f'The login "{dados["login"]}" already exists.'}

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'User created successfully!'}, 201 #Created


class UserLogin(Resource):

    @jwt_required
    def post(Resource):
        dados = atributos.parse_args()
        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {access_token: token_de_acesso}, 200
        return {'message': 'The user or password is incorrect.'}, 401
