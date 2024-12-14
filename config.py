import secrets

# 32바이트 길이의 랜덤 문자열 생성
jwt_secret_key = secrets.token_hex(32)
print(jwt_secret_key)

DB_CONFIG = {
    "host": "localhost",
    "user": "MySQL",
    "password": "0000",
    "database": "job_db"
}

SECRET_KEY = jwt_secret_key

def configure_app(app):
    """
    Flask 애플리케이션에 설정을 적용합니다.
    """
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["DB_CONFIG"] = DB_CONFIG
    app.config["JWT_SECRET_KEY"] = SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600  # 1시간
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 86400  # 1일
    app.config["DEBUG"] = True
