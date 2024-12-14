import jwt
from flask import request, jsonify
from functools import wraps
from config import SECRET_KEY

def generate_token(user_id):
    """
    JWT 발급 함수
    """
    payload = {"user_id": user_id}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def decode_token(token):
    """
    JWT 디코딩 및 검증 함수
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")

def jwt_required(f):
    """
    인증 미들웨어: JWT 토큰 검증
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        try:
            request.user_id = decode_token(token)
        except Exception as e:
            return jsonify({"error": str(e)}), 401
        return f(*args, **kwargs)
    return decorated_function
