from flask_restx import Namespace, Resource
from flask import request
from controllers.urgent_jobs_controller import get_urgent_jobs

api = Namespace("Urgent", description="APIs for urgent job postings")

@api.route("/")
class UrgentJobs(Resource):
    def get(self):
        """
        마감 임박 공고 리스트 조회
        """
        limit = int(request.args.get("limit", 10))  # 기본적으로 10개의 공고 반환
        return get_urgent_jobs(limit)
