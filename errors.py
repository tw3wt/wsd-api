from flask import jsonify

class APIError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_general_error(e):
        response = {
            "error": "An unexpected error occurred",
            "message": str(e)
        }
        return jsonify(response), 500

    @app.errorhandler(APIError)
    def handle_api_error(e):
        response = {"error": e.message}
        return jsonify(response), e.status_code
