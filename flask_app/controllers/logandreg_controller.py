from flask import session, redirect, render_template, request, flash
from flask_app import app
from flask_app.models.logandreg_model import Users
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("home.html")

@app.route('/input_user', methods=["POST"])
def register_user():
    if request.form['action'] == "register":
        is_valid = Users.validate_new_user(request.form)
        if not is_valid:
            return redirect("/")
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
            "first_name": request.form["first_name"],
            "last_name" : request.form["last_name"],
            "email": request.form["email"],
            "password": pw_hash
        }
        user_id = Users.save(data)
        print(f"this is the user id: {user_id}")
        session["user_id"] = user_id
        return redirect(f"/user/show/{user_id}")
    
    else:
        this_user = Users.get_by_email({'email': request.form['email']})
        print('This is the user')
        print(this_user)
        if this_user:
            if len(request.form['password']) < 8:
                flash('Password must be at least 8 characters')
                return redirect('/')
            if bcrypt.check_password_hash(this_user.password,request.form['password']):
                session['user_id'] = this_user.id
                return redirect(f"/user/show/{this_user.id}")
            else:
                flash("Incorrect Password")
                return redirect("/")
        else:
            flash("No user with this email")
            return redirect('/')

@app.route("/user/show/<int:id>")
def display_one(id):
    data = {"id":id}
    return render_template("loggedin.html", user= Users.get_one(data))

# @app.route('/login', methods=['POST'])
# def login():
#     data = {"email" : request.form['email']}
#     user_in_db = Users.get_by_email(data)
#     if not user_in_db:
#         flash("Invalid Email/Password")
#         return redirect('/')
#     if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
#         flash('Invalid Email/Password')
#         return redirect('/')
#     session['user_id']= user_in_db.id
#     return redirect('/')
    


# @app.route("/display_users")
# def display_all():
#     return render_template("read.html", all_users = Users.get_all())

# @app.route("/user/edit_page/<int:id>" )
# def edituser(id):
#     data = {"id":id}
#     return render_template("edit.html", user = Users.get_one(data))

# @app.route("/user/edit", methods=['POST'])
# def edit_page():
#     updated_user = request.form["id"]
#     Users.update(request.form)
#     return redirect(f"/user/show/{updated_user}")

# @app.route("/user/delete/<int:id>")
# def goodbye(id):
#     Users.delete(id)
#     return redirect("/display_users")


    # if not Users.validate_user(request.form):
    #     session['form_data'] = request.form
    #     return redirect("/")
    # show_user = Users.save(data)
    # session.pop("form_data", None)
    # session['user_id'] = show_user
    # return redirect(f"/user/show/{show_user}")