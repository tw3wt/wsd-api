from models.popular_model import PopularModel

def get_popular_jobs():
    """
    Get the list of popular jobs based on views.

    Returns:
        dict: A response containing popular jobs.
    """
    try:
        popular_jobs = PopularModel.fetch_popular_jobs(limit=10)
        return {
            "status": "success",
            "data": popular_jobs
        }, 200
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500
