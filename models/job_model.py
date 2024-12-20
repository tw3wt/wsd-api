from db import get_db_connection

class JobModel:
    @staticmethod
    def fetch_jobs(page, per_page, filters, search_query, sort_by):
        """
        공고 목록 조회 (검색, 필터링, 페이지네이션, 정렬 포함)
        """
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 기본 쿼리
        query = """
            SELECT jobs.id, jobs.title, jobs.location, jobs.experience,
                   jobs.education, jobs.employment_type, jobs.deadline,
                   (SELECT COUNT(*) FROM job_views WHERE job_views.job_id = jobs.id) AS views,
                   GROUP_CONCAT(skills.name) AS skills,
                   GROUP_CONCAT(badges.name) AS badges
            FROM jobs
            LEFT JOIN job_skills ON jobs.id = job_skills.job_id
            LEFT JOIN skills ON job_skills.skill_id = skills.id
            LEFT JOIN job_badges ON jobs.id = job_badges.job_id
            LEFT JOIN badges ON job_badges.badge_id = badges.id
            WHERE 1=1
        """
        params = []

        # 필터링
        if filters["location"]:
            query += " AND location = %s"
            params.append(filters["location"])
        if filters["experience"]:
            query += " AND experience = %s"
            params.append(filters["experience"])
        if filters["salary"]:
            query += " AND salary >= %s"
            params.append(filters["salary"])
        if filters["skills"]:
            query += """
                AND id IN (
                    SELECT job_id
                    FROM job_skills
                    WHERE skill_id IN (
                        SELECT id FROM skills WHERE name = %s
                    )
                )
            """
            params.append(filters["skills"])

        # 검색
        if search_query["keyword"]:
            query += " AND (title LIKE %s OR description LIKE %s)"
            params.extend([f"%{search_query['keyword']}%", f"%{search_query['keyword']}%"])
        if search_query["company"]:
            query += " AND company_id IN (SELECT id FROM companies WHERE name LIKE %s)"
            params.append(f"%{search_query['company']}%")
        if search_query["position"]:
            query += " AND title LIKE %s"
            params.append(f"%{search_query['position']}%")

        # 정렬
        allowed_sort_columns = ["created_at", "views"]
        if sort_by not in allowed_sort_columns:
            sort_by = "created_at"
        query += f" ORDER BY {sort_by} DESC"

        # 페이지네이션
        offset = (page - 1) * per_page
        query += " LIMIT %s OFFSET %s"
        params.extend([per_page, offset])

        cursor.execute(query, params)
        jobs = cursor.fetchall()

        # 총 공고 수
        count_query = "SELECT COUNT(*) as total FROM jobs"
        cursor.execute(count_query)
        total = cursor.fetchone()["total"]

        cursor.close()
        conn.close()
        return jobs, total

    @staticmethod
    def fetch_job_details(job_id, user_id):
        """
        공고 상세 정보 가져오기
        """
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT jobs.*, 
                   GROUP_CONCAT(badges.name) AS badges,
                   (SELECT COUNT(*) FROM job_views WHERE job_views.job_id = jobs.id) AS views
            FROM jobs
            LEFT JOIN job_badges ON jobs.id = job_badges.job_id
            LEFT JOIN badges ON job_badges.badge_id = badges.id
            WHERE jobs.id = %s
            GROUP BY jobs.id
        """
        cursor.execute(query, (job_id,))
        job = cursor.fetchone()

        if job and user_id:
            # 조회 기록 추가
            view_query = """
                INSERT INTO job_views (job_id, user_id, viewed_at)
                VALUES (%s, %s, NOW())
            """
            cursor.execute(view_query, (job_id, user_id))
            conn.commit()

        cursor.close()
        conn.close()
        return job

    @staticmethod
    def increment_views(job_id):
        """
        조회수 증가
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "UPDATE jobs SET views = views + 1 WHERE id = %s"
        cursor.execute(query, (job_id,))
        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def fetch_related_jobs(job_id):
        """
        관련 공고 추천
        """
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT jobs.id, jobs.title, jobs.location, 
                   (SELECT COUNT(*) FROM job_views WHERE job_views.job_id = jobs.id) AS views
            FROM jobs
            WHERE id != %s
            ORDER BY views DESC
            LIMIT 5
        """
        cursor.execute(query, (job_id,))
        related_jobs = cursor.fetchall()

        cursor.close()
        conn.close()
        return related_jobs
