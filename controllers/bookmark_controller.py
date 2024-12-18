from models.bookmark_model import BookmarkModel

def toggle_bookmark(user_id, bookmark_data):
    """
    북마크 추가/제거
    """
    try:
        job_id = bookmark_data.get("job_id")

        # 북마크 존재 여부 확인
        bookmark_exists = BookmarkModel.check_bookmark_exists(user_id, job_id)
        if bookmark_exists:
            # 북마크 제거
            BookmarkModel.remove_bookmark(user_id, job_id)
            return {
                "status": "success",
                "message": "Bookmark removed successfully"
            }, 200
        else:
            # 북마크 추가
            BookmarkModel.add_bookmark(user_id, job_id)
            return {
                "status": "success",
                "message": "Bookmark added successfully"
            }, 201
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500

def get_user_bookmarks(user_id, filters):
    """
    사용자별 북마크 목록 조회
    """
    try:
        page = int(filters.get("page", 1))
        page_size = int(filters.get("page_size", 20))

        bookmarks = BookmarkModel.fetch_user_bookmarks(user_id, page, page_size)
        total = len(bookmarks)  # 총 북마크 개수

        return {
            "status": "success",
            "bookmark": bookmarks,
            "total": total,
            "page": page,
            "per_page": per_page
        }, 200
    except Exception as e:
        # 오류가 발생하면 JSON 직렬화 가능한 형식으로 반환
        response = {
            "status": "error",
            "message": str(e)
        }
        return jsonify(response), 500
