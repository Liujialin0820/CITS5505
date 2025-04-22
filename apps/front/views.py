from flask import Blueprint,views,render_template,request
from .forms import SignupForm,SigninForm
from utils import restful
from .models import FrontUser
from exts import db

bp = Blueprint("front", __name__)

@bp.route("/")
def index():
    return "front index"


class SignupView(views.MethodView):
    def get(self):
        return render_template('front/front_signup.html')

    def post(self):
        print(request.form)
        form = SignupForm(request.form)
        if form.validate():
            email=form.email.data
            username=form.email.data
            password =form.password1.data
            user = FrontUser(email=email,username=username,password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())
    
bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))