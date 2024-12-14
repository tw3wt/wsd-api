from models.job_model import JobModel

def get_jobs(params):
    """
    공고 목록 조회 (검색, 필터링, 페이지네이션, 정렬 포함)
    """
    try:
        # 페이지네이션
        page = int(params.get("page", 1))
        per_page = int(params.get("per_page", 20))

        # 필터링
        filters = {
            "location": params.get("location"),
            "experience": params.get("experience"),
            "salary": params.get("salary"),
            "skills": params.get("skills"),
        }

        # 검색
        search_query = {
            "keyword": params.get("keyword"),
            "company": params.get("company"),
            "position": params.get("position"),
        }

        # 정렬 기준
        sort_by = params.get("sort_by", "created_at")  # 기본 정렬: 생성일

        # 모델에서 공고 조회
        jobs, total = JobModel.fetch_jobs(page, per_page, filters, search_query, sort_by)

        return {
            "status": "success",
            "data": jobs,
            "total": total,
            "page": page,
            "per_page": per_page
        }, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500


def get_job_details(job_id):
    """
    공고 상세 조회 (조회수 증가 및 관련 공고 추천 포함)
    """
    try:
        # 상세 정보 가져오기
        job_details = JobModel.fetch_job_details(job_id)
        if not job_details:
            return {"status": "error", "message": "Job not found"}, 404

        # 조회수 증가
        JobModel.increment_views(job_id)

        # 관련 공고 추천
        related_jobs = JobModel.fetch_related_jobs(job_id)

        return {
            "status": "success",
            "data": {
                "details": job_details,
                "related_jobs": related_jobs,
            }
        }, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500
