from flask import Flask, render_template, Response, session
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
import cv2
app = Flask(__name__)
app.config['SECRET_KEY'] = 'muhammadmoin'
app.config['UPLOAD_FOLDER'] = 'static/files'


class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Process")

def process_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    if image is None:
        return None

    # For simplicity, let's convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Save the processed image to a new file
    processed_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_image.jpg')
    cv2.imwrite(processed_path, gray_image)

    return processed_path


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    session.clear()
    return render_template('indexproject.html')


@app.route('/image', methods=['GET', 'POST'])
def image():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))
        session['image_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                            secure_filename(file.filename))
    return render_template('image_processing.html', form=form)


@app.route('/processed_image')
def processed_image():
    image_path = session.get('image_path', None)
    processed_image_path = process_image(image_path)
    with open(processed_image_path, 'rb') as f:
        image_binary = f.read()
    return Response(image_binary, mimetype='image/jpeg')


if __name__ == "__main__":
    app.run(debug=True)
