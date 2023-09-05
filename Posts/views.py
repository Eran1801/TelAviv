from django.db.models import Q
from django.http.response import JsonResponse
from django.views.decorators.csrf import \
    csrf_exempt  # will be used to exempt the CSRF token (Angular will handle CSRF token)
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
import logging
from Posts.serializers import PostSerializerAll
from Users.models import Users
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from Posts.models import Post
import base64
import boto3
from django.core.files.base import ContentFile

# Define the logger at the module level
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

post_id = 1

def convert_base64_to_image(base64_str, filename):
    '''
    Convert base64-encoded images to actual files.
    
    Args:
        base64_str (str): Base64-encoded image string.
        filename (str): Desired filename for the output image file.
        
    Returns:
        ContentFile: The converted image data as a Django ContentFile.
    '''
    try:
        # split the base64 string into format and image data parts
        format, image_str = base64_str.split(';base64,')
        
        # extract the image file extension from the format part
        ext = format.split('/')[-1]
        
        # decode the base64-encoded image data
        image_data = base64.b64decode(image_str)
        
        # create the full image filename with extension
        image_filename = f"{filename}.{ext}"
        
        # create a ContentFile object containing the image data
        # ContentFile - a file-like object that takes just raw content, rather than an actual file.
        content_file = ContentFile(image_data, name=image_filename)
        
        # return the ContentFile object
        return content_file
    
    except Exception as e:
        logger.error(f"convert_base64_to_image: {e}")
        return None

@api_view(['POST'])
@csrf_exempt
def add_post(request):
    '''This function will be used to add a new post'''

    global post_id

    post_data = request.data

    post_user_email = post_data.get('user', {}).get('user_email')

    # Fetch the Users object based on the email
    try:
        user = Users.objects.get(user_email=post_user_email)
    except Users.DoesNotExist:
        return HttpResponseServerError('User not found')    

    post_city = post_data.get('post_city')
    post_street = post_data.get('post_street')
    post_apartment_number = post_data.get('post_apartment_number')
    post_apartment_price = post_data.get('post_apartment_price')
    
    post_rent_start = post_data.get('post_rent_start')
    post_rent_end = post_data.get('post_rent_end')

    post_description = post_data.get('post_description')

    proof_image_base64 = post_data.get('proof_image')[0]  # Extract the first item from the list
    proof_image_file = convert_base64_to_image(proof_image_base64, "proof_image")

    driving_license_base64 = post_data.get('driving_license')[0]
    driving_license_file = convert_base64_to_image(driving_license_base64, "driving_license")

    apartment_pic_1_base64 = post_data.get('apartment_pic_1')[0]
    apartment_pic_1_file = convert_base64_to_image(apartment_pic_1_base64, "apartment_pic_1")

    # apartment_pic_2_base64 = post_data.get('apartment_pic_2')[0]
    # apartment_pic_2_file = convert_base64_to_image(apartment_pic_2_base64, "apartment_pic_2")

    # apartment_pic_3_base64 = post_data.get('apartment_pic_3')[0]
    # apartment_pic_3_file = convert_base64_to_image(apartment_pic_3_base64, "apartment_pic_3")

    # apartment_pic_4_base64 = post_data.get('apartment_pic_4')[0]
    # apartment_pic_4_file = convert_base64_to_image(apartment_pic_4_base64, "apartment_pic_4")

    # creating a dict to pass to the serializer as the post
    post_data_dict = {
        'post_id': post_id,
        'post_user_id': user.user_id,
        'post_city': post_city,
        'post_street': post_street,
        'post_apartment_number': post_apartment_number,
        'post_apartment_price': post_apartment_price,
        'post_rent_start': post_rent_start,
        'post_rent_end': post_rent_end,
        'proof_image': proof_image_file,
        'driving_license': driving_license_file,
        'apartment_pic_1': apartment_pic_1_file,
        'post_description': post_description,
    }

    # ADD this to the dict 
    """
    # todo : add the rest of the images int the above dict
    'apartment_pic_2' : apartment_pic_2_file,
    'apartment_pic_3' : apartment_pic_3_file,
    'apartment_pic_4' : apartment_pic_4_file,
    """

    # apartment_pic_2_instance = post_data_dict['apartment_pic_2']
    # apartment_pic_2_filename = apartment_pic_2_instance.name

    # apartment_pic_3_instance = post_data_dict['apartment_pic_3']
    # apartment_pic_3_filename = apartment_pic_3_instance.name

    # apartment_pic_4_instance = post_data_dict['apartment_pic_4']
    # apartment_pic_4_filename = apartment_pic_4_instance.name

    post_serializer = PostSerializerAll(data=post_data_dict)
    if post_serializer.is_valid():
        try:
            post_serializer.save()  # Attempt to save to the database
            post_id += 1
            logger.info("Saved to the database")
            return JsonResponse("Post successfully saved in db", safe=False)
        except Exception as e:
            logger.error(f"add_post : {e}")
            return HttpResponseServerError("An error occurred while saving the post")
    else:
        logger.debug(post_serializer.errors)
        return HttpResponseServerError("Post validation failed")

@api_view(['GET'])
@csrf_exempt
def get_all_posts(request):
    '''This function will be used to get all the posts in the db 'Pots' table'''
    try:

        all_posts = Post.objects.all()
        all_posts_serialize = PostSerializerAll(all_posts,many=True) # many -> many objects
        return JsonResponse(all_posts_serialize.data, safe=False)

    except Exception as e:
         logger.error(f"get_all_posts : {e}")
         return HttpResponseServerError("An error occurred during get_all_posts")
    
@api_view(['GET'])
@csrf_exempt
def get_post_by_parm(request):
    '''This function will be used to get all the posts in the db 'Pots' table'''
    try:

        post_city = request.GET.get('post_city') 
        logger.info(f'post_city: {post_city} and his type is {type(post_city)}')

        post_street = request.GET.get('post_street')
        logger.info(f'post_street:  + {post_street} and his type is {type(post_street)}')

        post_apartment_number = request.GET.get('post_apartment_number')
        logger.info(f'post_apartment_number: {post_apartment_number} and his type is {type(post_apartment_number)}')
        
        if post_city == '' and post_street == 'null' and post_apartment_number == 'null': 
            return HttpResponseBadRequest("At least one field is required")

        if post_city == '':
            return HttpResponseBadRequest("City field is required")

        # Construct the queryset conditions based on available parameters
        filter_conditions = {'post_city': post_city} # post_city is definitely not null

        if post_street != 'null' and post_street != '': # needs to check this 2 conditions
            logger.info(f'filter_conditions 1: {filter_conditions}')
            filter_conditions['post_street'] = post_street
        if post_apartment_number != 'null' and post_apartment_number != '':
            logger.info(f'filter_conditions 2: {filter_conditions}')
            filter_conditions['post_apartment_number'] = post_apartment_number

        logger.info(f'filter_conditions final: {filter_conditions}')

        post_v1 = Post.objects.filter(**filter_conditions)

        if post_v1.exists():
            try:
                post_serializer = PostSerializerAll(post_v1, many=True)
                return JsonResponse(post_serializer.data, safe=False)
            except :
                return HttpResponseServerError("An error occurred while serialize the post in get_posts")
        else:
            return HttpResponseNotFound("Post not found")

    except Exception as e:
         logger.error(f"get_posts : {e}")
         return HttpResponseServerError("An error occurred get_posts")

@api_view(['GET'])
@csrf_exempt
def get_post_by_post_id(request):
    '''This function will be used to get a post by its ID'''
    try:
        post_id = request.GET.get('post_id')
        logger.info('post_id: ' + post_id)

        post = Post.objects.get(post_id=post_id) # get the post using post_id

        post_serializer = PostSerializerAll(post)
        return JsonResponse(post_serializer.data, safe=False)

    except Post.DoesNotExist:
            return HttpResponseBadRequest("Post with the given ID does not exist.")
    except Exception as e:
            return HttpResponseBadRequest(f"An error occurred get_post_by_id: {e}")

@api_view(['GET'])
@csrf_exempt
def get_post_by_user_id(request):
    '''This function will be used to get all the posts (one or more) by the user ID for the "הדירות שלי"'''
    try:
        user_id = request.GET.get('user_id')
        logger.info(f'User ID: {user_id}')

        posts = Post.objects.filter(post_user_id=user_id) # get the post using post_id
        post_serializer = PostSerializerAll(posts, many=True) # more than one post
        logger.info(f'Post serializer: {post_serializer}')

        return JsonResponse(post_serializer.data, safe=False)
    except Post.DoesNotExist:    
            return HttpResponseBadRequest("Post with the given ID does not exist.")
    except Exception as e:
            return HttpResponseBadRequest(f"An error occurred: {e}")
    
@api_view(['PUT'])
@csrf_exempt
def update_description_post(request):
    '''This function will be used to update the description of a post'''
    try:
        data = request.data

        post_id = data.get('post_id')
        post_description = data.get('post_description')
    
        post = Post.objects.get(post_id=post_id) 
        post.post_description = post_description 

        #! NEEDS TO CHANGE THE POST IS_CONFIRMED TO FALSE AGAIN AFTER THE USER UPDATE THE DESCRIPTION
        post.save() # save the updated post to the db
        return JsonResponse("Description info updated successfully", safe=False)

    except Post.DoesNotExist:
            return HttpResponseBadRequest("Post with the given ID does not exist.")
    except Exception as e:
            return HttpResponseBadRequest(f"An error occurred, update_description_post: {e}")

# def delete_s3_folder(bucket_name, folder_name):
#     try:
#         s3 = boto3.client('s3')
#         response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
#         logger.info(f'response: {response}')

#         # Iterate through the objects in the folder and delete them
#         for obj in response.get('Objects', []):
#             s3.delete_object(Bucket=bucket_name, Key=obj['Key'])

#         # Delete the folder itself
#         s3.delete_object(Bucket=bucket_name, Key=folder_name + '/')

#     except Exception as e:
#         return HttpResponseBadRequest(f"An error occurred while deleting the S3 folder: {e}")

def delete_folder(bucket, post_id):
    """
    Removes a folder (prefix) with the specified post_id from a bucket.
    
    :param bucket: The bucket that contains the folder. This is a Boto3 Bucket resource.
    :param post_id: The post_id used as the folder name to delete.
    :return: The response that contains data about which objects were deleted and any that could not be deleted.
    """
    try:
        # Construct the list of object_keys to delete, including all objects under the folder
        object_keys_to_delete = [obj.key for obj in bucket.objects.filter(Prefix=post_id)]
        
        # Check if there are objects to delete
        if object_keys_to_delete:
            try:
                response = bucket.delete_objects(Delete={'Objects': [{'Key': key} for key in object_keys_to_delete]})
            except Exception as e:
                logger.error(f"delete_folder: {e}")
                return HttpResponseBadRequest(f"An error occurred inside the if in delete_folder {e}")
             
    except Exception as e:
        logger.error(f"delete_folder: {e}")
        return HttpResponseBadRequest(f"An error occurred while delete_folder function {e}")

@api_view(['DELETE'])
@csrf_exempt
def delete_post(request):
    '''This function will be used to delete a post'''
    try:
        post_id = request.GET.get('post_id')
        post_user_id = request.GET.get('post_user_id')

        logger.info(f'post_id: {post_id}')
        logger.info(f'post_user_id: {post_user_id}') 

        # delete S3 folder corresponding to this post
        s3_bucket_name = 'rent-buzz'
        #s3_folder_name = f'rent-buzz/Posts/Users object ({post_user_id})/{post_id}/'  # adjust the path accordingly

        delete_folder(s3_bucket_name, post_id)

        post = Post.objects.get(post_id=post_id) # get the post using post_id
        post.delete() # delete the post

        return JsonResponse("Post successfully deleted", safe=False)

    except Post.DoesNotExist:
            return HttpResponseBadRequest("Post with the given ID does not exist.")
    except Exception as e:
            return HttpResponseBadRequest(f"An error occurred, delete_post: {e}")