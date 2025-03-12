from django.urls import path
from .views import *
from django.urls import path
from .views import members_without_images, upload_member_image
from .views import print_view, download_pdf  # Import the new view


urlpatterns = [
    path('',login_,name='login_'),
    path('user_form', UserFormView.as_view(), name='user_form'),
    path('further_questions/', FurtherQuestionsView.as_view(), name='further_questions'),
    path('child_details/<int:child_index>/', child_details_view, name='child_details'),
    path('father_details/', FatherDetailsView.as_view(), name='father_details'),
    path('mother_details/', MotherDetailsView.as_view(), name='mother_details'),
    path('survivor_details/<int:survivor_index>/', survivor_details_view, name='survivor_details'),
    path('form_success/', form_success_view, name='form_success'),
    path('spouse_details',SpouseDetailsView.as_view(),name='spouse_details'),
    path('members-without-images/', members_without_images, name='members_without_images'),
    path('upload-member-image/<int:member_id>/', upload_member_image, name='upload_member_image'),
    path('print_preview/<member_id>',print_view,name='print_preview'),
    path('search_member/',MemberFormView.as_view(),name='member_form_view'),
    path('users_search_view/<f_name>/<l_name>/<phone_num>',users_search_view,name='users_search_view'),
path('download-pdf/<int:member_id>/', download_pdf, name='download_pdf'),

]










