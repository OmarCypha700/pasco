from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_question, name='upload_question'),
    path('', views.question_list, name='question_list'),
    path('download/<int:question_id>/', views.download_question, name='download_question'),
    path('view/<int:question_id>/', views.view_question, name='view_question'),
    path('download_multiple/', views.download_multiple_questions, name='download_multiple_questions'),
    path('delete/<int:question_id>', views.delete, name='delete_question')

]