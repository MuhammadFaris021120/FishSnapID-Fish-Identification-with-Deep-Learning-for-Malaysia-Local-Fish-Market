import os
from django.core.files.storage import FileSystemStorage
import cv2
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .ai_models.yolo_detect import detect

# Function to detect fish image and return the detection status and confidence
def detect_image(image, input_image_path, username):
    print(f'detect_image...')
    
    media_root = settings.MEDIA_ROOT
    print(f'media_root: {media_root}')
    print(f'input_image_path: {input_image_path}')		

    # Detect fish in the image
    box, confidence_score = detect(image)
    if box != ():
        confidence_score = f"{confidence_score:.2f}"
        
        # Extract coordinates
        x1, y1, x2, y2 = box

        # Draw rectangle box & confidence_score on the detected image, then save it into detection_images/ path
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 10)
        cv_image = cv2.putText(image, confidence_score, (x1, y1 - 10), 1, 10, (0, 255, 0), 10)

        # Ensure the directory for detection images exists
        user_detection_images_dir = os.path.join(media_root, username, 'detection_images')
        os.makedirs(user_detection_images_dir, exist_ok=True)
		
        # Save the detected image using cv2.imwrite
        filename = os.path.basename(input_image_path)
        detection_image_path = os.path.join(user_detection_images_dir, filename)
        cv2.imwrite(detection_image_path, cv_image)
        
        context = {
            'status': 'success',
            'local_name': 'Detected_Fish',
            'confidence_score': confidence_score,
            'image_path': input_image_path,
        }
    else:
        context = {
            'status': 'failed',
            'error': 'Fish not detected',
            'image_path': input_image_path,
        }
    print(f'detect_image >> context:', context)
    return context

# View to handle fish detection
@csrf_exempt
def detect_fish(request):
    print(f'detect_fish >> request: {request}')
    
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL
    print(f'media_root: {media_root}')		
    print(f'media_url: {media_url}')		
	
    if request.method == 'POST':
        try:
            # Ensure username not None
            username = request.POST.get('username')
            if not username:
                return JsonResponse({'status': 'failed', 'error': 'Missing username parameter'}, status=400)

            # Ensure 'input_image' is in the request files
            if 'input_image' not in request.FILES:
                return JsonResponse({'status': 'failed', 'error': 'No input image provided'}, status=400)

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
            
            # Read the input image using the image path (physical)
            image_path = os.path.join(fs.location, file_path)
            image = cv2.imread(image_path)
            if image is None:
                return JsonResponse({'status': 'failed', 'error': 'Failed to read the image'})
				
			# Construct input image path and remove leading slashes	
            filename = os.path.basename(file_path)
            input_image_path = os.path.join(media_url.lstrip('/'), username, 'input_images', filename) 
            print(f'input_image_path: {input_image_path}')

            # Detect fish image
            context = detect_image(image, input_image_path, username)
            return JsonResponse(context)
        except Exception as e:
            print(e)
            context = {
                'status': 'failed',
                'error': str(e)
            }
            return JsonResponse(context)
