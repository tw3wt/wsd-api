from db import get_db_connection

class ApplicationModel:
    @staticmethod
    def check_duplicate_application(user_id, job_id):
        """
        중복 지원 여부 확인
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM applications WHERE user_id = %s AND job_id = %s",
            (user_id, job_id)
        )
        result = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return result > 0

    @staticmethod
    def save_application(user_id, job_id, resume):
        """
        지원 정보 저장
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO applications (user_id, job_id, resume) VALUES (%s, %s, %s)",
            (user_id, job_id, resume)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def fetch_user_applications(user_id, filters):
        """
        사용자별 지원 목록 조회
        """
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 기본 SQL 쿼리
        query = "SELECT * FROM applications WHERE user_id = %s"
        values = [user_id]

        # 상태 필터 추가
        if "status" in filters:
            query += " AND status = %s"
            values.append(filters["status"])

        # 날짜 정렬 추가
        if "sort_by_date" in filters and filters["sort_by_date"].lower() == "desc":
            query += " ORDER BY applied_at DESC"
        else:
            query += " ORDER BY applied_at ASC"

        cursor.execute(query, tuple(values))
        applications = cursor.fetchall()
        cursor.close()
        conn.close()
        return applications

    @staticmethod
    def cancel_user_application(user_id, application_id):
        """
        지원 취소
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        # 상태 확인
        cursor.execute(
            "SELECT status FROM applications WHERE id = %s AND user_id = %s",
            (application_id, user_id)
        )
        result = cursor.fetchone()
        if not result:
            cursor.close()
            conn.close()
            return {"error": "Application not found"}, 404

        if result[0] != "pending":
            cursor.close()
            conn.close()
            return {"error": "Only pending applications can be canceled"}, 400

        # 상태 업데이트
        cursor.execute(
            "UPDATE applications SET status = 'canceled' WHERE id = %s AND user_id = %s",
            (application_id, user_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Application canceled successfully"}, 200
