from flask import render_template, request, jsonify, current_app, g
from flask_login import current_user
from app.errors import bp
from app.exceptions import ValidationError, BusinessError, TooManyRequestsError
import uuid


# create TraceID
@bp.before_app_request
def set_trace_id():
    g.trace_id = str(uuid.uuid4())


# Error Response Structure
def error_response(status_code, message, details=""):
    error_data = {
        "status_code": status_code,
        "trace_id": getattr(g, "trace_id", None),
        "message": message,
        "details": details,
    }
    # Check if request wants JSON
    if request.is_json or request.headers.get("Accept") == "application/json":
        return jsonify(error_data), status_code

    # Otherwise return HTML
    return (
        render_template(
            "errors/error.html", **error_data, login=current_user.is_authenticated
        ),
        status_code,
    )


@bp.app_errorhandler(ValidationError)
def handle_validation_error(e):
    current_app.logger.warning(f"ValidationError: {e} | TraceID: {g.trace_id}")
    return error_response(400, str(e))


@bp.app_errorhandler(BusinessError)
def handle_business_error(e):
    current_app.logger.warning(f"BusinessError: {e} | TraceID: {g.trace_id}")
    return error_response(409, str(e))


@bp.app_errorhandler(TooManyRequestsError)
def handle_too_many_requests(e):
    current_app.logger.warning(f"TooManyRequests: {e} | TraceID: {g.trace_id}")
    return error_response(429, str(e))


@bp.app_errorhandler(401)
def unauthorized_error(e):
    current_app.logger.warning(f"Unauthorized: {e} | TraceID: {g.trace_id}")
    return error_response(401, "Unauthorized")


@bp.app_errorhandler(403)
def forbidden_error(error):
    current_app.logger.warning(f"Forbidden: {error} | TraceID: {g.trace_id}")
    return error_response(403, "Sorry, you do not have permission to access this page.")


@bp.app_errorhandler(404)
def not_found_error(error):
    current_app.logger.info(f"Not Found: {request.path} | TraceID: {g.trace_id}")
    return error_response(404, "Sorry, the page you are looking for was not found.")


@bp.app_errorhandler(409)
def conflict_error(e):
    current_app.logger.warning(f"Conflict: {e} | TraceID: {g.trace_id}")
    return error_response(409, "Conflict")


@bp.app_errorhandler(429)
def too_many_requests_error(e):
    current_app.logger.warning(f"Too Many Requests: {e} | TraceID: {g.trace_id}")
    return error_response(429, "Too Many Requests")


@bp.app_errorhandler(422)
def handle_422(e):
    current_app.logger.warning(f"Unprocessable Entity: {e} | TraceID: {g.trace_id}")
    return error_response(422, "Unprocessable Entity:" + str(e))


@bp.app_errorhandler(500)
def internal_error(error):
    current_app.logger.error(
        f"Internal Server Error: {error} | TraceID: {g.trace_id}", exc_info=True
    )
    return error_response(500, "Sorry, something went wrong on the server.")
