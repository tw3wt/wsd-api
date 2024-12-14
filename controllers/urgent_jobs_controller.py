from models.urgent_jobs_model import UrgentModel

def get_urgent_jobs(limit):
    """
    마감일 기준으로 마감 임박 공고를 가져옵니다.

    Args:
        limit (int): 반환할 공고의 수

    Returns:
        dict: 마감 임박 공고 리스트와 상태 코드
    """
    try:
        urgent_jobs = UrgentModel.fetch_urgent_jobs(limit)

        if not urgent_jobs:
            return {
                "status": "success",
                "message": "No urgent jobs available.",
                "data": []
            }, 200

        return {
            "status": "success",
            "message": "Urgent jobs fetched successfully.",
            "data": urgent_jobs
        }, 200
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500
