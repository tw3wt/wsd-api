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

    @staticmethod
    def add_user_skill(user_id, skill_name):
        """
        사용자 기술 추가
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        # 기술이 `skills` 테이블에 없는 경우 추가
        skill_query = """
            INSERT INTO skills (name) VALUES (%s)
            ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id)
        """
        cursor.execute(skill_query, (skill_name,))
        skill_id = cursor.lastrowid

        # 사용자 기술 추가
        user_skill_query = """
            INSERT INTO user_skills (user_id, skill_id)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE user_id = user_id
        """
        cursor.execute(user_skill_query, (user_id, skill_id))

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def fetch_user_skills(user_id):
        """
        사용자 기술 조회
        """
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT skills.name
            FROM user_skills
            INNER JOIN skills ON user_skills.skill_id = skills.id
            WHERE user_skills.user_id = %s
        """
        cursor.execute(query, (user_id,))
        skills = [row["name"] for row in cursor.fetchall()]

        cursor.close()
        conn.close()
        return skills

    @staticmethod
    def remove_user_skill(user_id, skill_name):
        """
        사용자 기술 삭제
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            DELETE user_skills
            FROM user_skills
            INNER JOIN skills ON user_skills.skill_id = skills.id
            WHERE user_skills.user_id = %s AND skills.name = %s
        """
        cursor.execute(query, (user_id, skill_name))

        conn.commit()
        cursor.close()
        conn.close()