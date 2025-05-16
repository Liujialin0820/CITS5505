# encoding: utf-8
from flask import jsonify

class HttpCode(object):
    # HTTP status code constants for consistent usage
    ok = 200  # Success
    unautherror = 401  # Unauthorized (not logged in)
    paramserror = 400  # Invalid parameters
    servererror = 500  # Internal server error

def restful_result(code, message, data):
    """
    🔧 Generic response formatter
    Returns a Flask JSON response with consistent structure.
    
    :param code: HTTP status code (int)
    :param message: message to return (str)
    :param data: optional data payload (dict or None)
    :return: Flask Response (JSON)
    """
    return jsonify({
        "code": code,
        "message": message,
        "data": data or {}  # Return empty dict if data is None
    })

def success(message="", data=None):
    """
    Shortcut for a 200 OK response
    """
    return restful_result(code=HttpCode.ok, message=message, data=data)

def unauth_error(message=""):
    """
    Shortcut for a 401 Unauthorized error response
    """
    return restful_result(code=HttpCode.unautherror, message=message, data=None)

def params_error(message=""):
    """
    Shortcut for a 400 Bad Request error response
    """
    return restful_result(code=HttpCode.paramserror, message=message, data=None)

def server_error(message=""):
    """
    Shortcut for a 500 Internal Server Error response
    """
    return restful_result(
        code=HttpCode.servererror,
        message=message or 'server error',
        data=None
    )