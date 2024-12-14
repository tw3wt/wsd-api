import base64
import jwt
from werkzeug.security import check_password_hash, generate_password_hash
from models.user_model import UserModel
from db import get_db_connection 
from auth import generate_token, decode_token
from datetime import  timedelta

def register_user(data):
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    # 이메일 형식 검증
    if "@" not in email or "." not in email.split("@")[1]:
        return {"error": "Invalid email format"}, 400

    # 중복 회원 검사
    if UserModel.find_by_email(email):
        return {"error": "Email already registered"}, 400

    # 비밀번호 암호화 (Base64)
    hashed_password = base64.b64encode(password.encode()).decode()

    # 사용자 생성
    UserModel.create_user(email, hashed_password, name)
    return {"message": "User registered successfully"}, 201

def login_user(data):
    email = data.get("email")
    password = data.get("password")

    user = UserModel.find_by_email(email)
    if not user:
        return {"error": "Invalid email or password"}, 401

    # 비밀번호 검증 (Base64 디코딩)
    stored_password = base64.b64decode(user["password"]).decode()
    if stored_password != password:
        return {"error": "Invalid email or password"}, 401

    # JWT 토큰 발급
    access_token = generate_token(user["id"], timedelta(minutes=15))
    refresh_token = generate_token(user["id"], timedelta(days=7))

    # 로그인 이력 저장
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO login_history (user_id) VALUES (%s)", (user["id"],))
    conn.commit()
    cursor.close()
    conn.close()

    return {"access_token": access_token, "refresh_token": refresh_token}, 200

def refresh_token(refresh_token):
    try:
        user_id = decode_token(refresh_token)
        new_access_token = generate_token(user_id, timedelta(minutes=15))
        return {"access_token": new_access_token}, 200
    except Exception as e:
        return {"error": str(e)}, 401

def update_user_profile(user_id, data):
    password = data.get("password")
    name = data.get("name")

    if password:
        # 비밀번호 암호화 (Base64)
        password = base64.b64encode(password.encode()).decode()

    # 사용자 정보 수정
    UserModel.update_user(user_id, password=password, name=name)
    return {"message": "User profile updated successfully"}, 200
