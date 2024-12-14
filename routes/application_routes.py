from flask_restx import Namespace, Resource, fields
from flask import request
from controllers.application_controller import (
    submit_application,
    get_user_applications,
    cancel_application
)
from auth import jwt_required

api = Namespace("Applications", description="Job application APIs")

# 모델 정의
application_model = api.model("Application", {
    "job_id": fields.Integer(required=True, description="ID of the job being applied for"),
    "resume": fields.String(required=False, description="Resume content in base64 format (optional)")
})

filter_model = api.model("ApplicationFilters", {
    "status": fields.String(description="Filter by application status (e.g., pending, accepted, rejected)"),
    "sort_by_date": fields.String(description="Sort applications by date (asc/desc)")
})

# 라우트 정의
@api.route("/")
class Applications(Resource):
    @jwt_required
    @api.expect(application_model)
    def post(self):
        """
        지원하기
        """
        user_id = request.user_id
        data = api.payload
        return submit_application(user_id, data)

    @jwt_required
    def get(self):
        """
        지원 내역 조회
        """
        user_id = request.user_id
        filters = request.args
        return get_user_applications(user_id, filters)

@api.route("/<int:application_id>")
class ApplicationDetails(Resource):
    @jwt_required
    def delete(self, application_id):
        """
        지원 취소
        """
        user_id = request.user_id
        return cancel_application(user_id, application_id)
