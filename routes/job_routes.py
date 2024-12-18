from flask_restx import Namespace, Resource, reqparse
from controllers.job_controller import (
    get_jobs,
    get_job_details
)
from flask import request

# 쿼리 파라미터 정의
job_list_parser = reqparse.RequestParser()
job_list_parser.add_argument("page", type=int, default=1, help="Page number for pagination")
job_list_parser.add_argument("per_page", type=int, default=20, help="Number of items per page")
job_list_parser.add_argument("location", type=str, help="Filter by location")
job_list_parser.add_argument("experience", type=str, help="Filter by experience")
job_list_parser.add_argument("salary", type=int, help="Filter by minimum salary")
job_list_parser.add_argument("skills", type=str, help="Filter by skills (comma-separated)")
job_list_parser.add_argument("keyword", type=str, help="Search by keyword")
job_list_parser.add_argument("company", type=str, help="Search by company name")
job_list_parser.add_argument("position", type=str, help="Search by position")
job_list_parser.add_argument("sort_by", type=str, choices=["created_at", "views", "deadline"], default="created_at", help="Sort by criteria")

api = Namespace("Jobs", description="Job management APIs")

# 라우트 정의
@api.route("/")
class JobList(Resource):
    @api.expect(job_list_parser) 
    def get(self):
        """
        채용 공고 목록 조회
        """
        params = request.args
        return get_jobs(params)

@api.route("/:<int:job_id>")
class JobDetails(Resource):
    def get(self, job_id):
        """
        채용 공고 상세 조회
        """
        return get_job_details(job_id)
