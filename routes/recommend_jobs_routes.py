from flask_restx import Namespace, Resource, fields
from flask import request
from controllers.recommend_jobs_controller import get_recommended_jobs
from auth import jwt_required

api = Namespace("Recommend", description="Job Recommendation APIs")

user_skills_model = api.model("UserSkills", {
    "skills": fields.List(fields.String, required=True, description="List of user skills (e.g., ['Python', 'Java', 'React'])")
})

@api.route("/")
class RecommendJobs(Resource):
    @jwt_required
    def get(self):
        """
        추천 공고 리스트 조회
        """
        user_id = request.user_id  # JWT에서 추출된 사용자 ID
        return get_recommended_jobs(user_id)

@api.route("/user-skills")
class UserSkills(Resource):
    @jwt_required
    def get(self):
        """
        사용자 기술 목록 조회
        """
        user_id = request.user_id
        return get_user_skills(user_id)

    @jwt_required
    @api.expect(user_skills_model)
    def post(self):
        """
        사용자 기술 추가
        """
        user_id = request.user_id
        data = api.payload
        return add_user_skills(user_id, data)

    @jwt_required
    def delete(self):
        """
        사용자 기술 삭제
        """
        user_id = request.user_id
        skill_name = request.args.get("skill_name")
        return remove_user_skill(user_id, skill_name)
