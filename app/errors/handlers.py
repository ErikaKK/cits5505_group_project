from flask import render_template, request, jsonify, current_app, g
from app.errors import bp
from app.exceptions import ValidationError, BusinessError, TooManyRequestsError
import uuid

# create TraceID
@bp.before_app_request
def set_trace_id():
    g.trace_id = str(uuid.uuid4())

# Error Response Structure

def error_response(status_code, message, details=None):
    resp = {
        "trace_id": getattr(g, "trace_id", None),
        "message": message,
        "details": details,
    }
    return jsonify(resp), status_code

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
    return render_template('errors/403.html', trace_id=g.trace_id), 403

@bp.app_errorhandler(404)
def not_found_error(error):
    current_app.logger.info(f"Not Found: {request.path} | TraceID: {g.trace_id}")
    return render_template('errors/404.html', trace_id=g.trace_id), 404

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
    return render_template('errors/422.html', message=e, trace_id=g.trace_id), 422

@bp.app_errorhandler(500)
def internal_error(error):
    current_app.logger.error(f"Internal Server Error: {error} | TraceID: {g.trace_id}", exc_info=True)
    return render_template('errors/500.html', trace_id=g.trace_id), 500 