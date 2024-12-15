from db import get_db_connection

class BookmarkModel:
    @staticmethod
    def check_bookmark_exists(user_id, job_id):
        """
        북마크 존재 여부 확인
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM bookmarks WHERE user_id = %s AND job_id = %s",
            (user_id, job_id)
        )
        result = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return result > 0

    @staticmethod
    def add_bookmark(user_id, job_id):
        """
        북마크 추가
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO bookmarks (user_id, job_id)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id)
        """
        cursor.execute(query, (user_id, job_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def remove_bookmark(user_id, job_id):
        """
        북마크 제거
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM bookmarks WHERE user_id = %s AND job_id = %s",
            (user_id, job_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def fetch_user_bookmarks(user_id, page, page_size):
        """
        사용자별 북마크 목록 조회
        """
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT jobs.id, jobs.title, jobs.location, jobs.description, bookmarks.created_at
            FROM bookmarks
            INNER JOIN jobs ON bookmarks.job_id = jobs.id
            WHERE bookmarks.user_id = %s
            ORDER BY bookmarks.created_at DESC
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (user_id, page_size, (page - 1) * page_size))
        bookmarks = cursor.fetchall()
        cursor.close()
        conn.close()
        return bookmarks
