from models.bookmark_model import BookmarkModel

def toggle_bookmark(user_id, bookmark_data):
    """
    북마크 추가/제거
    """
    job_id = bookmark_data.get("job_id")

    # 북마크 존재 여부 확인
    bookmark_exists = BookmarkModel.check_bookmark_exists(user_id, job_id)
    if bookmark_exists:
        # 북마크 제거
        BookmarkModel.remove_bookmark(user_id, job_id)
        return {"message": "Bookmark removed successfully"}, 200
    else:
        # 북마크 추가
        BookmarkModel.add_bookmark(user_id, job_id)
        return {"message": "Bookmark added successfully"}, 201

def get_user_bookmarks(user_id, filters):
    """
    사용자별 북마크 목록 조회
    """
    page = int(filters.get("page", 1))
    page_size = int(filters.get("page_size", 20))

    bookmarks = BookmarkModel.fetch_user_bookmarks(user_id, page, page_size)
    return {"bookmarks": bookmarks, "page": page, "page_size": page_size}, 200
