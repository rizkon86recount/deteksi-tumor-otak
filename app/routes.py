from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from app.model import predict_tumor  # Import fungsi prediksi dari model.py

app = Flask(__name__)

# Tentukan folder tempat menyimpan file yang di-upload
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads', 'user_mri_images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Pastikan folder upload ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Panggil fungsi prediksi dari model.py
        result = predict_tumor(file_path)
        
        return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
