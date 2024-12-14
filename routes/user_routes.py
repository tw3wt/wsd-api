from flask_restx import Namespace, Resource, fields
from controllers.user_controller import (
    register_user, login_user, refresh_token, update_user_profile
)
from auth import jwt_required
from flask import request

api = Namespace("Auth", description="User authentication and management APIs")

# 모델 정의
register_model = api.model("Register", {
    "email": fields.String(required=True, description="User email"),
    "password": fields.String(required=True, description="User password"),
    "name": fields.String(required=True, description="User name")
})

login_model = api.model("Login", {
    "email": fields.String(required=True, description="User email"),
    "password": fields.String(required=True, description="User password")
})

profile_update_model = api.model("ProfileUpdate", {
    "password": fields.String(description="New password (optional)"),
    "name": fields.String(description="New name (optional)")
})

# 라우트
@api.route("/register")
class Register(Resource):
    @api.expect(register_model)
    def post(self):
        """회원 가입"""
        data = api.payload
        return register_user(data)

@api.route("/login")
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """로그인"""
        data = api.payload
        return login_user(data)

@api.route("/refresh")
class RefreshToken(Resource):
    def post(self):
        """토큰 갱신"""
        ref_token = api.payload.get("refresh_token")
        return refresh_token(ref_token)

@api.route("/profile")
class Profile(Resource):
    @jwt_required
    @api.expect(profile_update_model)
    def put(self):
        """회원 정보 수정"""
        user_id = request.user_id
        data = api.payload
        return update_user_profile(user_id, data)