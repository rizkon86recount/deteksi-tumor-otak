from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from app.model import predict_tumor  # Impor fungsi prediksi dari model.py

app = Flask(__name__, template_folder='app/templates')

# Folder penyimpanan gambar
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads', 'user_mri_images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        # Simpan gambar yang diunggah
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Buat direktori jika belum ada
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        file.save(file_path)

        # Lakukan prediksi tumor
        result = predict_tumor(file_path)  # Fungsi prediksi di model.py

        # Kirim hasil prediksi dan gambar ke template result.html
        image_url = 'uploads/user_mri_images/' + filename  # Path relatif terhadap folder static
        return render_template('result.html', image_url=image_url, result=result)


if __name__ == '__main__':
    app.run(debug=True)
