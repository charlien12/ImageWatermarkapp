# Important imports
from app import app
from flask import request, render_template
import os
import cv2
import numpy as np
from PIL import Image

# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'

# Route to home page
@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        option = request.form['options']
        image_upload = request.files['image_upload']

        # Convert uploaded image to numpy array
        image = Image.open(image_upload)
        image_logow = np.array(image.convert('RGB'))
        h_image, w_image, _ = image_logow.shape

        if option == 'logo_watermark':
            logo_upload = request.files['logo_upload']
            logo = Image.open(logo_upload)
            logo = np.array(logo.convert('RGB'))

            # Resize logo to be larger (1/3 of image width)
            scale_percent = 33
            logo_width = int(w_image * scale_percent / 100)
            logo_height = int(logo.shape[0] * (logo_width / logo.shape[1]))
            logo_resized = cv2.resize(logo, (logo_width, logo_height))

            h_logo, w_logo, _ = logo_resized.shape

            # Center logo
            top_y = (h_image - h_logo) // 2
            left_x = (w_image - w_logo) // 2
            bottom_y = top_y + h_logo
            right_x = left_x + w_logo

            roi = image_logow[top_y:bottom_y, left_x:right_x]

            # Blend ROI and logo (slightly transparent)
            result = cv2.addWeighted(roi, 1, logo_resized, 0.7, 0)
            image_logow[top_y:bottom_y, left_x:right_x] = result

            # Save result
            img = Image.fromarray(image_logow).convert("RGB")
            img.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image.png'))
            full_filename = 'static/uploads/image.png'
            return render_template('index.html', full_filename=full_filename)

        else:
            # Text watermark
            text_mark = request.form['text_mark']

            # Font settings (bold, larger)
            font = cv2.FONT_HERSHEY_COMPLEX
            font_scale = max(1.5, w_image / 500)  # dynamically bigger for larger images
            thickness = 3

            # Get text size
            (text_width, text_height), _ = cv2.getTextSize(text_mark, font, font_scale, thickness)

            # Center text
            x = (w_image - text_width) // 2
            y = (h_image + text_height) // 2

            cv2.putText(image_logow, text=text_mark,
                        org=(x, y),
                        fontFace=font,
                        fontScale=font_scale,
                        color=(0, 0, 255),
                        thickness=thickness,
                        lineType=cv2.LINE_AA)

            # Save result
            timg = Image.fromarray(image_logow).convert("RGB")
            timg.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image1.png'))
            full_filename = 'static/uploads/image1.png'
            return render_template('index.html', full_filename=full_filename)


# Main function
if __name__ == '__main__':
    app.run(debug=True)
