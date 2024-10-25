import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
from PIL import Image
from keras.models import load_model
import cv2

# Load the pre-trained model (assuming it has been saved in .h5 format)
# model = load_model('models/tumor_otak.h5')
model = load_model('models/tumor_otak.h5', custom_objects={'InputLayer': keras.layers.InputLayer})


def preprocess_image(image_path):
    '''Preprocess the image before feeding it into the model'''
    image = Image.open(image_path).convert('RGB')  # Convert to RGB if not already
    image = image.resize((224, 224))  # Resize to 128x128, or as per the model input
    image_array = np.array(image)  # Convert image to array
    image_array = image_array / 255.0  # Normalize pixel values
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    return image_array

def predict_tumor(image_path):
    '''Predict whether the image has a tumor or not'''
    processed_image = preprocess_image(image_path)
    prediction = model.predict(processed_image)
    if prediction[0][0] > 0.5:
        return 'Tumor Detected'
    else:
        return 'No Tumor Detected'