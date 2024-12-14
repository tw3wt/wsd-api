from flask_restx import Namespace, Resource, fields
from flask import request
from controllers.bookmark_controller import (
    toggle_bookmark,
    get_user_bookmarks
)
from auth import jwt_required

api = Namespace("Bookmarks", description="Bookmark management APIs")

# 모델 정의
bookmark_model = api.model("BookmarkToggle", {
    "job_id": fields.Integer(required=True, description="ID of the job to bookmark or remove bookmark")
})

# 라우트 정의
@api.route("/")
class Bookmarks(Resource):
    @jwt_required
    @api.expect(bookmark_model)
    def post(self):
        """
        북마크 추가/제거
        """
        user_id = request.user_id
        data = api.payload
        return toggle_bookmark(user_id, data)

    @jwt_required
    def get(self):
        """
        북마크 목록 조회
        """
        user_id = request.user_id
        filters = request.args
        return get_user_bookmarks(user_id, filters)
