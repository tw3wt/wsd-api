import base64
from models.application_model import ApplicationModel

def submit_application(user_id, application_data):
    """
    지원하기
    """
    job_id = application_data.get("job_id")
    resume = application_data.get("resume")

    # 중복 지원 체크
    if ApplicationModel.check_duplicate_application(user_id, job_id):
        return {"error": "You have already applied for this job"}, 400

    # 이력서 검증 (옵션)
    if resume:
        try:
            # Base64 디코딩 테스트
            base64.b64decode(resume)
        except Exception:
            return {"error": "Invalid resume format"}, 400

    # 지원 정보 저장
    ApplicationModel.save_application(user_id, job_id, resume)
    return {"message": "Application submitted successfully"}, 201

def get_user_applications(user_id, filters):
    """
    지원 내역 조회
    """
    applications = ApplicationModel.fetch_user_applications(user_id, filters)
    return {"applications": applications}, 200

def cancel_application(user_id, application_id):
    """
    지원 취소
    """
    return ApplicationModel.cancel_user_application(user_id, application_id)
    