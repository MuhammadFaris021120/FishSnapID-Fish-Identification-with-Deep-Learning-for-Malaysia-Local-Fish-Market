# /apps/db/views.py

import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, Fish, FishCollection
import json

@csrf_exempt
def query_fish_recent_capture(request):
    """
    Retrieve the most recent fish collection for a given user.

    Parameters:
    - request: HTTP GET request containing the username.

    Returns:
    - JSON response containing the latest fish collection details or an error message.
    """
    print(f'query_fish_recent_capture >> request: {request}')
    if request.method == 'GET':
        username = request.GET.get('username')

        if not username:
            return HttpResponseBadRequest('Missing username parameter')

        try:
            # Get the user by username
            user = get_object_or_404(UserProfile, username=username)

            # Query the latest FishCollection record for the user
            latest_collection = FishCollection.objects.filter(user=user).order_by('-created_datetime').first()

            if not latest_collection:
                return JsonResponse({'message': 'No records found'}, status=404)

            # Prepare the result
            result = {
                'fish_collection_id': latest_collection.id,
                'fish_id': latest_collection.fish.id,
                'local_name': latest_collection.fish.local_name,
                'english_name': latest_collection.fish.english_name,
                'scientific_name': latest_collection.fish.scientific_name,
                'fish_desc': latest_collection.fish.fish_desc,
                'safety_desc': latest_collection.fish.safety_desc,
                'captured_location': latest_collection.captured_location,
                'image_path': latest_collection.image_path,
                'collection_created_datetime': latest_collection.created_datetime,
                'confidence_score': latest_collection.confidence_score,
            }

            return JsonResponse(result)
        except Exception as e:
            return HttpResponseBadRequest(f'Error: {str(e)}')

    return HttpResponseBadRequest('Invalid request method')

@csrf_exempt
def query_fish_for_search(request):
    """
    Search for fish collections by local name and return unique results sorted by local name.

    Parameters:
    - request: HTTP GET request containing the username and an optional local_name.

    Returns:
    - JSON response containing unique fish collection details filtered and sorted by local name, or an error message.
    """
    print(f'query_fish_for_search >> request: {request}')
    if request.method == 'GET':
        username = request.GET.get('username')
        local_name = request.GET.get('local_name', '')

        if not username:
            return HttpResponseBadRequest('Missing username parameter')

        try:
            # Get the user by username
            user = get_object_or_404(UserProfile, username=username)

            # Query FishCollection by user and filter by local_name using icontains for wildcard search
            fish_collections = FishCollection.objects.filter(user=user, fish__local_name__icontains=local_name)

            # Sort by local_name and filter unique records
            sorted_collections = sorted(fish_collections, key=lambda x: x.fish.local_name)
            unique_collections = []
            seen_local_names = set()
            for collection in sorted_collections:
                if collection.fish.local_name not in seen_local_names:
                    unique_collections.append(collection)
                    seen_local_names.add(collection.fish.local_name)

            # Prepare the result
            result = []
            for collection in unique_collections:
                result.append({
                    'id': collection.id,
                    'name': collection.fish.local_name,
                })

            return JsonResponse(result, safe=False)
        except Exception as e:
            return HttpResponseBadRequest(f'Error: {str(e)}')

    return HttpResponseBadRequest('Invalid request method')

@csrf_exempt
def query_fish_collection(request):
    """
    Retrieve fish collections filtered by local name for a given user.

    Parameters:
    - request: HTTP GET request containing the username and an optional local_name.

    Returns:
    - JSON response containing fish collection details filtered by local name, or an error message.
    """
    print(f'query_fish_collection >> request: {request}')
    if request.method == 'GET':
        username = request.GET.get('username')
        local_name = request.GET.get('local_name', '')

        if not username:
            return HttpResponseBadRequest('Missing username parameter')

        try:
            # Get the user by username
            user = get_object_or_404(UserProfile, username=username)

            # Query FishCollection by user and filter by local_name using icontains for wildcard search
            fish_collections = FishCollection.objects.filter(user=user, fish__local_name__icontains=local_name)

            # Prepare the result
            result = []
            for collection in fish_collections:
                result.append({
                    'fish_collection_id': collection.id,
                    'fish_id': collection.fish.id,
                    'local_name': collection.fish.local_name,
                    'english_name': collection.fish.english_name,
                    'scientific_name': collection.fish.scientific_name,
                    'fish_desc': collection.fish.fish_desc,
                    'safety_desc': collection.fish.safety_desc,
                    'captured_location': collection.captured_location,
                    'image_path': collection.image_path,
                    'collection_created_datetime': collection.created_datetime,
                    'confidence_score': collection.confidence_score,
                })

            return JsonResponse(result, safe=False)
        except Exception as e:
            return HttpResponseBadRequest(f'Error: {str(e)}')

    return HttpResponseBadRequest('Invalid request method')

@csrf_exempt
def query_fish_by_local_name(request):
    """
    Retrieve fish details by local name.

    Parameters:
    - request: HTTP GET request containing the local_name.

    Returns:
    - JSON response containing fish details or an error message.
    """
    print(f'query_fish_by_local_name >> request: {request}')
    if request.method == 'GET':
        local_name = request.GET.get('local_name')

        if not local_name:
            return HttpResponseBadRequest('Missing local_name parameter')

        try:
            # Get the first Fish object by local_name (case-insensitive)
            fish = Fish.objects.filter(local_name__iexact=local_name).first()

            if not fish:
                return JsonResponse({'error': 'No fish found with the provided local_name'}, status=404)

            # Prepare the result
            result = {
                'status': 'success',
                'fish_id': fish.id,
                'local_name': fish.local_name,
                'english_name': fish.english_name,
                'scientific_name': fish.scientific_name,
                'fish_desc': fish.fish_desc,
                'safety_desc': fish.safety_desc,
                'created_datetime': fish.created_datetime,
            }

            return JsonResponse(result)
        except Exception as e:
            return HttpResponseBadRequest(f'Error: {str(e)}')

    return HttpResponseBadRequest('Invalid request method')

@csrf_exempt
def create_fish_collection(request):
    """
    Create a new fish collection record for a user.

    Parameters:
    - request: HTTP POST request containing username, local_name, captured_location, image_path, and confidence_score.

    Returns:
    - JSON response indicating success or failure of the creation process.
    """
    print(f'create_fish_collection >> request: {request}')
    if request.method == 'POST':
        try:
            # Get inputs from form-data
            username = request.POST.get('username')
            local_name = request.POST.get('local_name')
            captured_location = request.POST.get('captured_location')
            image_path = request.POST.get('image_path')
            confidence_score = request.POST.get('confidence_score')

            if not username or not local_name or not image_path or not confidence_score:
                return JsonResponse({'status': 'failed', 'error': 'Missing required fields'}, status=400)

            # Convert confidence_score to float
            try:
                confidence_score = float(confidence_score)
            except ValueError:
                return JsonResponse({'status': 'failed', 'error': 'Invalid confidence_score'}, status=400)

            # Get the user by username
            user = get_object_or_404(UserProfile, username=username)
            # Get the fish by local_name
            fish = get_object_or_404(Fish, local_name=local_name)

            # Create and save the FishCollection record
            fish_collection = FishCollection(
                user=user,
                fish=fish,
                captured_location=captured_location,
                image_path=image_path,
                confidence_score=confidence_score,
            )
            fish_collection.save()

            return JsonResponse({'status': 'success', 'message': 'FishCollection record created successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'failed', 'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'failed', 'error': str(e)}, status=400)

    return JsonResponse({'status': 'failed', 'error': 'Invalid request method'}, status=400)

@csrf_exempt
def delete_fish_collection(request):
    """
    Delete a fish collection record based on fish_collection.id parameter.

    Parameters:
    - request: HTTP DELETE request containing the fish_collection_id.

    Returns:
    - JSON response indicating success or failure of the deletion process.
    """
    print(f'delete_fish_collection >> request: {request}')
    if request.method == 'DELETE':
        try:
            # Parse the request body to get fish_collection_id
            fish_collection_id = request.GET.get('fish_collection_id')

            if not fish_collection_id:
                return HttpResponseBadRequest('Missing fish_collection_id parameter')

            # Get the FishCollection object
            fish_collection = get_object_or_404(FishCollection, id=fish_collection_id)

            # Get the image path to delete the image file
            image_path = fish_collection.image_path

            # Delete the FishCollection record
            fish_collection.delete()

            # Delete the image file if it exists
            image_full_path = os.path.join(settings.BASE_DIR, image_path)
            print(f'delete_fish_collection >> image_full_path: {image_full_path}')
            if os.path.exists(image_full_path):
                try:
                    os.remove(image_full_path)
                except OSError as e:
                    return JsonResponse({'status': 'failed', 'error': f'Error deleting image file: {str(e)}'}, status=500)
					
            # Delete the image file if it exists in /detection_images folder
            detection_full_path = image_full_path.replace('input_images', 'detection_images')
            print(f'delete_fish_collection >> detection_full_path: {detection_full_path}')
            if os.path.exists(detection_full_path):
                try:
                    os.remove(detection_full_path)
                except OSError as e:
                    return JsonResponse({'status': 'failed', 'error': f'Error deleting detection image file: {str(e)}'}, status=500)

            return JsonResponse({'status': 'success', 'message': 'FishCollection record deleted successfully'})
        except FishCollection.DoesNotExist:
            return JsonResponse({'status': 'failed', 'error': 'FishCollection record does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'failed', 'error': str(e)}, status=500)

    return HttpResponseBadRequest('Invalid request method')

@csrf_exempt
def update_fish_collection(request):
    """
    Update the captured_location field for a fish collection record.

    Parameters:
    - request: HTTP POST request containing the fish_collection_id and the new captured_location.

    Returns:
    - JSON response indicating success or failure of the update process.
    """
    print(f'update_fish_collection >> request: {request}')
    if request.method == 'POST':
        try:
            # Get inputs from form-data
            fish_collection_id = request.POST.get('fish_collection_id')
            new_captured_location = request.POST.get('captured_location')
            print(f'update_fish_collection >> fish_collection_id: {fish_collection_id}, new_captured_location: {new_captured_location}')

            if not fish_collection_id:
                return JsonResponse({'status': 'failed', 'error': 'Missing fish_collection_id field'}, status=400)

            if not new_captured_location:
                return JsonResponse({'status': 'failed', 'error': 'Missing new_captured_location field'}, status=400)

            # Get the FishCollection object
            fish_collection = get_object_or_404(FishCollection, id=fish_collection_id)

            # Update the captured_location field
            fish_collection.captured_location = new_captured_location
            fish_collection.save()

            return JsonResponse({'status': 'success', 'message': 'FishCollection record updated successfully'})
        except FishCollection.DoesNotExist:
            return JsonResponse({'status': 'failed', 'error': 'FishCollection record does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'failed', 'error': str(e)}, status=500)

    return JsonResponse({'status': 'failed', 'error': 'Invalid request method'}, status=400)
	
	
@csrf_exempt
def create_user_profile(request):
    """
    Create a new UserProfile record if it does not exist.

    Parameters:
    - request: HTTP POST request containing username, password, fullname, and email in form data.

    Returns:
    - JSON response indicating success or failure of the creation process.
    """
    if request.method == 'POST':
        try:
            # Get inputs from form-data
            username = request.POST.get('username')
            password = request.POST.get('password')
            fullname = request.POST.get('fullname')
            email = request.POST.get('email')

            if not username:
                return JsonResponse({'status': 'failed', 'error': 'Missing username field'}, status=400)

            # Check if user profile already exists
            if UserProfile.objects.filter(username=username).exists():
                # return JsonResponse({'status': 'failed', 'error': 'User profile already exists'}, status=400)
                return JsonResponse({'status': 'success', 'message': 'User profile already exists'})

            # Create and save the UserProfile record
            user_profile = UserProfile(
                username=username,
                password=password,
                fullname=fullname,
                email=email,
            )
            user_profile.save()

            return JsonResponse({'status': 'success', 'message': 'UserProfile record created successfully'})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'error': str(e)}, status=400)

    return JsonResponse({'status': 'failed', 'error': 'Invalid request method'}, status=400)
	
@csrf_exempt
def delete_fish_image(request):
    """
    Delete a fish image based on image_path parameter.

    Parameters:
    - request: HTTP DELETE request containing the image_path.

    Returns:
    - JSON response indicating success or failure of the deletion process.
    """
    print(f'delete_fish_image >> request: {request}')
    if request.method == 'DELETE':
        try:
            # Parse the request body to get image_path
            image_path = request.GET.get('image_path')

            if not image_path:
                return HttpResponseBadRequest('Missing image_path parameter')

            # Delete the image file if it exists in /input_images folder
            image_full_path = os.path.join(settings.BASE_DIR, image_path)
            print(f'delete_fish_image >> image_full_path: {image_full_path}')
            if os.path.exists(image_full_path):
                try:
                    os.remove(image_full_path)
                except OSError as e:
                    return JsonResponse({'status': 'failed', 'error': f'Error deleting image file: {str(e)}'}, status=500)
					
            # Delete the image file if it exists in /detection_images folder
            detection_full_path = image_full_path.replace('input_images', 'detection_images')
            print(f'delete_fish_image >> detection_full_path: {detection_full_path}')
            if os.path.exists(detection_full_path):
                try:
                    os.remove(detection_full_path)
                except OSError as e:
                    return JsonResponse({'status': 'failed', 'error': f'Error deleting detection image file: {str(e)}'}, status=500)

            return JsonResponse({'status': 'success', 'message': 'Fish image deleted successfully'})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'error': str(e)}, status=500)

    return HttpResponseBadRequest('Invalid request method')	
	
