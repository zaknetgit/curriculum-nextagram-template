from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from models.image import Image
from flask_login import login_user, logout_user, login_required, current_user
from instagram_web.util.helpers import upload_file_to_s3, gateway
from werkzeug import secure_filename

images_blueprint = Blueprint('images', __name__, template_folder='templates')

@images_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('images/new.html')

@images_blueprint.route("/<id>/show", methods=["GET"])
@login_required
def show(id):
    image = Image.get_or_none(Image.id == id)
    return render_template("images/show.html", image=image)

@images_blueprint.route('/<user_id>/upload', methods=['POST'])
def upload(user_id):
    user = User.get_or_none(User.id == user_id)

    if user:
        if current_user.id == int(user_id):

            if "image" not in request.files:
                flash("No file provided!")
                return redirect(url_for('images.new'))


            file = request.files["image"]


            file.filename = secure_filename(file.filename)


            image_path = upload_file_to_s3(file, user.username)

            new_image = Image(user=user, image_url=image_path)

            if new_image.save():
                flash("Successfully uploaded!","success")
                return redirect(url_for("users.show", username=user.username))
            else:
                flash("Upload failed :(  Please try again")
                return redirect(url_for('images.new'))
        else:
            flash("Cannot uplaod images for other users", "danger")
            return redirect(url_for('users.show', username = user.username))

    else:
        flash("No user found!")
        return redirect(url_for('home'))