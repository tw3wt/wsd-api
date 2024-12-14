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
            SELECT id, title, location, description, views
            FROM jobs
            ORDER BY views DESC
            LIMIT %s
        """
        cursor.execute(query, (limit,))
        jobs = cursor.fetchall()
        cursor.close()
        conn.close()
        return jobs
