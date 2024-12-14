from flask_restx import Namespace, Resource
from flask import request
from controllers.recommend_jobs_controller import get_recommended_jobs
from auth import jwt_required

api = Namespace("Recommend", description="Job Recommendation APIs")

@api.route("/")
class RecommendJobs(Resource):
    @jwt_required
    def get(self):
        """
        추천 공고 리스트 조회
        """
        user_id = request.user_id  # JWT에서 추출된 사용자 ID
        return get_recommended_jobs(user_id)
