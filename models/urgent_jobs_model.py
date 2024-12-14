from db import get_db_connection

class UrgentModel:
    @staticmethod
    def fetch_urgent_jobs(limit=10):
        """
        마감일 기준으로 임박한 공고를 가져옵니다.

        Args:
            limit (int): 반환할 공고 수

        Returns:
            list: 마감 임박 공고 리스트
        """
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 마감일이 가까운 공고를 가져오는 SQL 쿼리
        query = """
            SELECT id, title, location, description, deadline
            FROM jobs
            WHERE deadline IS NOT NULL
            ORDER BY deadline ASC
            LIMIT %s
        """
        cursor.execute(query, (limit,))
        urgent_jobs = cursor.fetchall()
        cursor.close()
        conn.close()

        return urgent_jobs
