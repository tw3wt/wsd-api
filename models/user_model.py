from db import get_db_connection

class UserModel:
    @staticmethod
    def find_by_email(email):
        """이메일로 사용자 찾기"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

    @staticmethod
    def create_user(email, hashed_password, name):
        """사용자 생성"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (email, password, name) VALUES (%s, %s, %s)",
            (email, hashed_password, name)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update_user(user_id, password=None, name=None):
        """사용자 정보 수정"""
        conn = get_db_connection()
        cursor = conn.cursor()
        if password:
            cursor.execute("UPDATE users SET password = %s WHERE id = %s", (password, user_id))
        if name:
            cursor.execute("UPDATE users SET name = %s WHERE id = %s", (name, user_id))
        conn.commit()
        cursor.close()
        conn.close()
