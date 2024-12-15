from db import get_db_connection

class PopularModel:
    @staticmethod
    def fetch_popular_jobs(limit=10):
        """
        Fetch jobs with the highest views from the database.

        Args:
            limit (int): Number of jobs to fetch.

        Returns:
            list: A list of popular jobs.
        """
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT j.id, j.title, j.location, COUNT(jv.id) AS views
            FROM jobs j
            LEFT JOIN job_views jv ON j.id = jv.job_id
            GROUP BY j.id
            ORDER BY views DESC
            LIMIT %s
        """
        cursor.execute(query, (limit,))
        jobs = cursor.fetchall()
        cursor.close()
        conn.close()
        return jobs
