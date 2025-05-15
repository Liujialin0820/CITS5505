from flask import Blueprint, jsonify
from .models import CourseModel  # 根据你的项目路径调整导入方式

bp = Blueprint("common", __name__, url_prefix="/common")

@bp.route("/")
def index():
    return "common index"

@bp.route("/courses-with-times")
def get_courses_with_times():
    data = CourseModel.get_all_courses_with_times()
    return jsonify(data)
