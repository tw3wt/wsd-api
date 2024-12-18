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


def add_user_skills(user_id, skill_data):
    """
    사용자 기술 추가
    """
    try:
        skills = skill_data.get("skills", [])
        if not skills:
            return {"status": "error", "message": "No skills provided"}, 400

        for skill in skills:
            UserSkillModel.add_user_skill(user_id, skill)

        return {"status": "success", "message": "Skills added successfully"}, 201
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

def get_user_skills(user_id):
    """
    사용자 기술 조회
    """
    try:
        skills = UserSkillModel.fetch_user_skills(user_id)
        return {"status": "success", "data": skills}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

def remove_user_skill(user_id, skill_name):
    """
    사용자 기술 삭제
    """
    try:
        if not skill_name:
            return {"status": "error", "message": "Skill name is required"}, 400

        UserSkillModel.remove_user_skill(user_id, skill_name)
        return {"status": "success", "message": "Skill removed successfully"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500
