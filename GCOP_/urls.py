from django.urls import path
from .views import *

urlpatterns = [
    path('',login_,name='login_'),
    path('user_form', user_form_view, name='user_form'),
    path('further_questions/', further_questions_view, name='further_questions'),
    path('child_details/<int:child_index>/', child_details_view, name='child_details'),
    path('father_details/', father_details, name='father_details'),
    path('mother_details/', mother_details, name='mother_details'),
    path('survivor_details/<int:survivor_index>/', survivor_details_view, name='survivor_details'),
    path('form_success/', form_success_view, name='form_success'),
    path('spouse_details',spouse_details,name='spouse_details')
]
