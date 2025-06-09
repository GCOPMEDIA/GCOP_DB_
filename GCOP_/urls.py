from django.urls import path
from .views import *
from django.urls import path
 # Import the new view


urlpatterns = [
    path('',login_,name='login_'),
    path('user_form', user_form_view, name='user_form'),
    path('further_questions/', further_questions_view, name='further_questions'),
    path('child_details/<int:child_index>/', child_details_view, name='child_details'),
    path('father_details/', father_details, name='father_details'),
    path('mother_details/', mother_details, name='mother_details'),
    path('survivor_details/<int:survivor_index>/', survivor_details_view, name='survivor_details'),
    path('form_success/', form_success_view, name='form_success'),
    path('spouse_details',spouse_details,name='spouse_details'),
    path('members-without-images/', members_without_images, name='members_without_images'),
    path('upload-member-image/<int:member_id>/', upload_member_image, name='upload_member_image'),
    path('print_preview/<member_id>',print_view,name='print_preview'),
path('search_member/',member_form_view,name='member_form_view'),
    path('users_search_view/<f_name>/<l_name>/<phone_num>',users_search_view,name='users_search_view'),
path('download-pdf/<int:member_id>/', download_pdf, name='download_pdf'),
    path('to-print/',to_print,name='to_print'),
    path('save_qr/', qr_code, name='qr_code'),
    path('card_details/<member_id>',card_details,name='card_details'),
    path("check-id", check_id, name="check_id"),
    path("attendance-today/",attendance,name="attendance"),
    path('attendance-today-mercy-temple/',attendance_mercy_temple,name='attendance-mercy-temple')
]













