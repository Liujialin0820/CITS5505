from flask import Blueprint, jsonify  # Import Flask's Blueprint system and JSON response helper
from .models import CourseModel  # Import CourseModel from current package (adjust if needed for actual structure)

# Create a blueprint named 'common', with URL prefix '/common'
bp = Blueprint("common", __name__, url_prefix="/common")

@bp.route("/")
def index():
    # Simple test or placeholder route for /common/
    return "common index"

@bp.route("/courses-with-times")
def get_courses_with_times():
    # Returns all courses with their associated timeslots in JSON format
    data = CourseModel.get_all_courses_with_times()  # Calls a class method that likely returns list of dicts
    return jsonify(data)  # Convert Python data to JSON HTTP response

