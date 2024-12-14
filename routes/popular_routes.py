from flask_restx import Namespace, Resource
from controllers.popular_controller import get_popular_jobs

api = Namespace("Popular", description="Retrieve popular jobs based on views")

@api.route("/")
class PopularJobs(Resource):
    def get(self):
        """
        Get the list of popular jobs based on views.
        """
        return get_popular_jobs()
