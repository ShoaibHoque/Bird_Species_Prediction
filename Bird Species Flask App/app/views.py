from app import app
from flask import request, render_template
from keras import models
import numpy as np
from PIL import Image
import string
import random
import os

# Configure initial file upload path
app.config['INITIAL_FILE_UPLOADS'] = os.path.join(app.root_path, 'static/uploads')

# Ensure the uploads directory exists
os.makedirs(app.config['INITIAL_FILE_UPLOADS'], exist_ok=True)

# loading model
model = models.load_model("app/static/model/bird_species_model.keras")

# Route to home page
@app.route("/", methods=["GET", "POST"])
def index():

    # Execute if request is get
    if request.method == "GET":
        full_filename = 'images/white_bg.jpg'
        return render_template("index.html", full_filename=full_filename)
    
    # Execute if request is post
    if request.method == "POST":

        # Ensure the uploads directory exists
        os.makedirs(app.config['INITIAL_FILE_UPLOADS'], exist_ok=True)

        # Generating unique image name
        letters = string.ascii_lowercase
        name = ''.join(random.choice(letters) for i in range(10)) + '.png'
        full_filename = 'uploads/' + name

        # Reading, resizing, saving & preprocessing image
        image_upload = request.files['image_upload']
        image = Image.open(image_upload)
        image = image.resize((224,224))
        image.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], name))
        image_arr = np.array(image.convert('RGB'))
        image_arr.shape = (1,224,224,3)

        # Predicting output
        result = model.predict(image_arr)
        ind = np.argmax(result)
        classes = ['AMERICAN GOLDFINCH', 'BARN OWL', 'CARMINE BEE-EATER', 'DOWNY WOODPECKER', 'EMPEROR PENGUIN', 'FLAMINGO']

        return render_template('index.html', full_filename=full_filename, pred=classes[ind])

if __name__ == '__main__':
    app.run(debug=True)
