from db import get_db_connection

class RecommendModel:
    @staticmethod
    def fetch_recommended_jobs(user_id):
        """
        사용자 정보를 기반으로 추천 공고를 가져옵니다.

        Args:
            user_id (int): 사용자 ID

        Returns:
            list: 추천 공고 리스트
        """
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 사용자 기술 스택 및 이전 지원 정보 기반 추천 쿼리
        query = """
            SELECT jobs.id, jobs.title, jobs.location, jobs.description, jobs.views
            FROM jobs
            LEFT JOIN job_skills ON jobs.id = job_skills.job_id
            LEFT JOIN skills ON job_skills.skill_id = skills.id
            WHERE skills.id IN (
                SELECT skill_id
                FROM user_skills
                WHERE user_id = %s
            )
            AND jobs.id NOT IN (
                SELECT job_id
                FROM applications
                WHERE user_id = %s
            )
            ORDER BY jobs.views DESC
            LIMIT 10
        """
        cursor.execute(query, (user_id, user_id))
        recommendations = cursor.fetchall()
        cursor.close()
        conn.close()

        return recommendations
