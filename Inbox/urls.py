from django.urls import re_path

from Inbox import views

urlpatterns = [
    
    re_path(r'^get_all_user_messages/$', views.get_all_user_messages,name='get_all_user_messages'),
    re_path(r'^update_read_status/$',views.update_read_status,name='update_read_status'),
    re_path(r'^delete_messages_by_post_id/$',views.delete_messages_by_post_id,name='delete_messages_by_post_id'),
    
    # What is it ? 
    re_path(r'^has_unread_messages/$', views.has_unread_messages,name='has_unread_messages'),
]