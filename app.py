from flask import Flask
from flask_restx import Api
from config import configure_app
from logging_config import configure_logging
from errors import register_error_handlers
from routes.user_routes import api as user_ns
from routes.job_routes import api as job_ns
from routes.application_routes import api as application_ns
from routes.popular_routes import api as popular_ns
from routes.recommend_jobs_routes import api as recommend_ns
from routes.urgent_jobs_routes import api as urgent_ns

app = Flask(__name__)
configure_app(app)
configure_logging()
api = Api(
    app,
    version='1.0',
    title='Job API Documentation',
    description='A RESTful API for managing job-related services',
    doc='/docs'  # Swagger UI
)

# 네임스페이스 등록
api.add_namespace(user_ns, path="/api/users")
api.add_namespace(job_ns, path="/api/jobs")
api.add_namespace(application_ns, path="/api/applications")
api.add_namespace(popular_ns, path="/api/popular")
api.add_namespace(recommend_ns, path="/api/recommend")
api.add_namespace(urgent_ns, path="/api/urgent")

# 에러 핸들러 등록
register_error_handlers(app)

if __name__ == "__main__":
    app.run(debug=True)
