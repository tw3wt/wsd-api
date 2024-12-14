from models.recommend_jobs_model import RecommendModel

def get_recommended_jobs(user_id):
    """
    사용자에게 추천할 채용 공고를 가져옵니다.

    Args:
        user_id (int): 사용자 ID

    Returns:
        dict: 추천 공고 리스트와 상태 코드
    """
    try:
        # 추천 로직 호출
        recommended_jobs = RecommendModel.fetch_recommended_jobs(user_id)

        if not recommended_jobs:
            return {
                "status": "success",
                "message": "No recommendations available.",
                "data": []
            }, 200

        return {
            "status": "success",
            "message": "Recommended jobs fetched successfully.",
            "data": recommended_jobs
        }, 200
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500
