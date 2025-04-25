from flask import (
    Blueprint,
    views,
    render_template,
    request,
    session,
    redirect,
    url_for,
    g,
    jsonify,
)
from .forms import (
    LoginForm,
    RegisterForm,
    ResetpwdForm,
    AddBoardForm,
    UpdateBoardForm,
)
from .models import CMSUser
from exts import db
from .decorators import login_required
from config import Config
from utils import restful
from apps.common.models import BoardModel

bp = Blueprint("cms", __name__, url_prefix="/cms")


@bp.route("/logout/")
@login_required
def logout():
    del session[Config.CMS_USER_ID]
    return redirect(url_for("cms.login"))


class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template("cms/login.html", message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[Config.CMS_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return redirect(url_for("cms.index"))
            else:
                return self.get(message="email or password error")
        else:
            message = form.errors.popitem()[0] + ": " + form.errors.popitem()[1][0]
            return self.get(message=message)


class RegisterView(views.MethodView):
    def get(self, message=None):
        return render_template("cms/register.html", message=message)

    def post(self):
        form = RegisterForm(request.form)
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            security_code = form.security_code.data

            if security_code != Config.SECRET_KEY:
                message = "Security code error. Please contact the administrator."
                return self.get(message=message)

            # check if already registered
            existing_user = CMSUser.query.filter_by(email=email).first()
            if existing_user:
                return self.get(message="Email already registered")

            # create new user
            user = CMSUser(username=username, password=password, email=email)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("cms.login"))
        else:
            field, errors = form.errors.popitem()
            message = f"{field}: {errors[0]}"
            return self.get(message=message)


class ResetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template("cms/cms_resetpwd.html")

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error("wrong password!")
        else:
            return restful.params_error(form.get_error())


@bp.route("/")
@login_required
def index():
    return render_template("cms/cms_index.html")


@bp.route("/profile/")
@login_required
def profile():
    return render_template("cms/cms_profile.html")


@bp.route("/boards/")
@login_required
def boards():
    board_models = BoardModel.query.all()
    context = {"boards": board_models}
    return render_template("cms/cms_boards.html", **context)


@bp.route("/aboard/", methods=["POST"])
@login_required
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route("/uboard/", methods=["POST"])
@login_required
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message="没有这个板块！")
    else:
        return restful.params_error(message=form.get_error())


@bp.route("/dboard/", methods=["POST"])
@login_required
def dboard():
    board_id = request.form.get("board_id")
    if not board_id:
        return restful.params_error("请传入板块id！")

    board = BoardModel.query.get(board_id)
    if not board:
        return restful.params_error(message="没有这个板块！")

    db.session.delete(board)
    db.session.commit()
    return restful.success()


bp.add_url_rule("/login/", view_func=LoginView.as_view("login"))
bp.add_url_rule("/register/", view_func=RegisterView.as_view("register"))
bp.add_url_rule("/resetpwd/", view_func=ResetPwdView.as_view("resetpwd"))
