from flask import session, redirect, render_template, request, flash
from flask_app import app
from flask_app.models import logandreg_model
from flask_app.models import post_models

@app.route('/new/post', methods=['POST'])
def create_post():
    is_valid = post_models.Posts.save_post(request.form)
    user= session['user_id']
    if not is_valid:
        return redirect (f'/user/show/{user}')
    print(request.form)
    return redirect (f'/user/show/{user}')



@app.route('/delete/post/<int:id>')
def delete_post(id):
    if 'user_id' not in session:
        return redirect('/')
    id_data= {
        'id':id
    }
    post_models.Posts.delete_posts(id_data)
    return redirect(f"/user/show/{id}")

# @app.route('/delete/post/<int:id>')
# def delete_post(id):
#     user= session['user_id']
#     post_models.Posts.delete_post(id)
#     return redirect(f'/user/show/{user}')

# @app.route('/wall')
# def from_the_window():
#     if 'id' not in session:
#         return redirect('/logout')
#     user_id = session['id']
#     return redirect(f'/wall/{user_id}')

# @app.route('/post_form', methods=['POST'])
# def submit_new_post():
#     # is_valid= Posts.verify_post(request.form)
#     # if not is_valid:
#     #     return redirect('/wall')
#     # data = {
#     #     'content': request.form['content']
#     # }
#     print(request.form)
#     Posts.save_post(request.form)
#     return redirect('/wall')
# , new_post =new_post

# @app.route("/wall/<int:id>")
# def display_one():
#     data = {"id":id}
#     results = Posts.all_user_posts(data)
#     return render_template("wall.html", user_posts= results)

# @app.route('/wall')
# def show_all_posts(id):
#     user_posts_dict={
#         "id":id
#     }
#     results = Posts.all_user_posts(user_posts_dict)
#     return render_template('wall.html', user_posts = results)

