from django.http.response import JsonResponse
from django.views.decorators.csrf import \
    csrf_exempt  # will be used to exempt the CSRF token (Angular will handle CSRF token)
from rest_framework.parsers import JSONParser
import logging
from Posts.serializers import PostSerializer
from Users.models import Users
from django.http import HttpResponseServerError
from Posts.models import Post


# Define the logger at the module level
logger = logging.getLogger(__name__)

@csrf_exempt
def add_post(request):
    logging.basicConfig(level=logging.DEBUG)

    if request.method == 'POST':
        user_data = JSONParser().parse(request)

        post_user_email = user_data.get('post_user_email')

        # Fetch the Users object based on the email
        try:
            user = Users.objects.get(user_email=post_user_email)
        except Users.DoesNotExist:
            return HttpResponseServerError('User not found')

        post_city = user_data.get('post_city')
        post_street = user_data.get('post_street')
        post_apartment_number = user_data.get('post_apartment_number')
        post_apartment_price = user_data.get('post_apartment_price')
        
        post_rent_start = user_data.get('post_rent_start') # extract day, month, year 
        post_rent_end = user_data.get('post_rent_end') # extract day, month, year 

        proof_image = user_data.get('proof_image')
        driving_license = user_data.get('driving_license')
        apartment_pic_1 = user_data.get('apartment_pic_1')
        apartment_pic_2 = user_data.get('apartment_pic_2')
        apartment_pic_3 = user_data.get('apartment_pic_3')
        apartment_pic_4 = user_data.get('apartment_pic_4')

        post_description = user_data.get('post_description')

        new_post = Post(

            post_user=user,
            post_city=post_city,
            post_street=post_street,
            post_apartment_number=post_apartment_number,
            post_apartment_price=post_apartment_price,
            post_rent_start=post_rent_start,
            post_rent_end=post_rent_end,
            proof_image=proof_image,
            driving_license=driving_license,
            apartment_pic_1=apartment_pic_1,
            apartment_pic_2=apartment_pic_2,
            apartment_pic_3=apartment_pic_3,
            apartment_pic_4=apartment_pic_4,
            post_description=post_description

        )

        post_serializer = PostSerializer(data=new_post)
        if post_serializer.is_valid():
            post_serializer.save() # save to db
            return JsonResponse("Post Success",safe=False)
        else:
            logger.debug(post_serializer.errors)
            return HttpResponseServerError("Post Fails")
    






        