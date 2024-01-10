from django.urls import re_path

from Inbox import views

urlpatterns = [
    # Attach the right function to the right url
    re_path(r'^update_confirm_status/$', views.update_confirm_status, name='update_confirm_status'), 
    re_path(r'^get_all_user_messages/$', views.get_all_user_messages,name='get_all_user_messages'),
    re_path(r'^update_read_status/$',views.update_read_status,name='update_read_status'),
    re_path(r'^delete_message/$',views.delete_message,name='delete_message'),
    re_path(r'^has_unread_messages/$', views.has_unread_messages,name='has_unread_messages'),
    re_path(r'^all_messages_by_post_id/$',views.all_messages_by_post_id, name='all_messages_by_post_id')

]