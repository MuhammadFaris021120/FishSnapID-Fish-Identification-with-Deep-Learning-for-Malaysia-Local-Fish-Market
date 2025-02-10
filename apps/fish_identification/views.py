# Import necessary Django modules and libraries
from django.shortcuts import render
import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from apps.fish_detection.views import detect_image

# Import OpenCV for image processing
import cv2

# Import TensorFlow and Keras for model loading and prediction
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np

# Define the base directory for the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load the pre-trained MobileNetV2 model for fish identification
model_path = os.path.join(BASE_DIR, 'fish_identification', 'ai_models', 'mobilenetv2_model.h5')
print(f"Loading MobileNet-v2 model from path: {model_path}")
model = load_model(model_path)

# Define a function to preprocess the input image for the model
def preprocess_image(img):
    print('preprocess_image...')
    img_array = cv2.resize(img, (224, 224))  # Resize image to match model's expected sizing
    img_array = img_array.astype('float32')  # Ensure image data type is float32
    img_array = np.expand_dims(img_array, axis=0)  # Add a batch dimension to the image
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)  # Preprocess the image for MobileNetV2
    return img_array

# Define a function to classify the image and return the predicted fish species and confidence
def classify_image(img):
    print('classify_image...')
    processed_img = preprocess_image(img)
    predictions = model.predict(processed_img)
    labels = ['Bawal Emas', 'Cencaru', 'Daun Baru', 'Gelama', 'Jenahak', 'Kembong', 'Kerisi',
              'Merah', 'Sardin', 'Sebelah', 'Selar Kuning', 'Senangin', 'Siakap', 'Tamok', 'Tilapia Merah']
    predicted_class_index = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class_index]
    predicted_label = labels[predicted_class_index]
    return predicted_label, confidence

# Define the API endpoint to identify fish species from an uploaded image
@csrf_exempt
def identify_fish(request):
    print(f'identify_fish >> request: {request}')
	
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL
    print(f'media_root: {media_root}')
    print(f'media_url: {media_url}')	
	
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            if not username:
                return JsonResponse({'status': 'failed', 'error': 'Missing username parameter'}, status=400)

            # Ensure input_image is not None
            input_image = request.FILES.get('input_image')
            if input_image is None:
                return JsonResponse({'status': 'failed', 'error': 'Invalid input image'}, status=400)
				
            fs = FileSystemStorage()
			
            # Ensure the directory for input images exists
            user_input_images_dir = os.path.join(media_root, username, 'input_images')
            os.makedirs(user_input_images_dir, exist_ok=True)

            # Save the file using FileSystemStorage
            file_path = fs.save(os.path.join(username, 'input_images', input_image.name), input_image)
			
			# Construct input image path and remove leading slashes	
            filename = os.path.basename(file_path)
            input_image_path = os.path.join(media_url.lstrip('/'), username, 'input_images', filename) 
            print(f'input_image_path: {input_image_path}')
			
            # Calling YOLO model fish detection, if enabled
            preDetection = request.POST.get('pre_detection')
            print(f'preDetection? {preDetection}')
            if preDetection and preDetection.lower() == 'true':  # Check if preDetection is a string representing True
                # Read the uploaded image using OpenCV
                image_path = os.path.join(fs.location, file_path)
                img = cv2.imread(image_path)
                if img is None:
                    return JsonResponse({'status': 'failed', 'error': 'Failed to read the image'})
                context = detect_image(img, input_image_path, username)
                print(f'context: {context}')
                if context['status'] != 'success':
                    return JsonResponse(context)

            # Read the uploaded image using OpenCV
            image_path = os.path.join(fs.location, file_path)
            img = cv2.imread(image_path)
            if img is None:
                return JsonResponse({'status': 'failed', 'error': 'Failed to read the image'})			
			
            # Perform fish species identification using the loaded model
            local_name, confidence_score = classify_image(img)
            print(f'local_name: {local_name}, confidence_score: {confidence_score}')

            # Prepare JSON response with identified fish species and confidence score
            if local_name:
                confidence_score_str = f"{confidence_score:.2f}"
                context = {
                    'status': 'success',
                    'local_name': local_name,
                    'confidence_score': confidence_score_str,
                    'image_path': input_image_path,
                }
            else:
                context = {
                    'status': 'failed',
                    'error': 'Fish not identified',
                    'image_path': input_image_path,
                }
            return JsonResponse(context)
        except Exception as e:
            # Handle exceptions and return error response
            print(e)
            context = {
                'status': 'failed',
                'error': str(e)
            }
            return JsonResponse(context)
