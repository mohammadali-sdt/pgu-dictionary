from django.urls import path
from . import views

app_name = 'dictionary'

urlpatterns = [
    path('', views.home, name='home'),
    path('word/<str:word>/', views.get_word_detail, name='get_word_detail'),
    path('suggest/<str:word>/', views.get_suggestion_words, name='get_suggestion_words'),
    path('add/suggestion/', views.add_new_suggestion, name='add_new_suggestion'),
    path('suggests/actived/', views.get_actived_suggests, name='get_actived_suggests'),
    path('comment/add/<int:word_id>/', views.add_new_comment, name='add_new_comment'),
    path('comment/reply/add/<int:word_id>/<int:comment_id>', views.add_new_reply, name='add_new_reply'),
    path('comment/feedback/', views.add_feedback_comment, name='add_feedback_comment'),
    path('popup/<str:word>/', views.get_popup, name='get_popup'),
    # path('word/<str:word>/', views.get_synonym_of_word, name='get_synonym_of_word'),
    # path('suggest/<str:letter>/', views.get_suggested_words, name='get_suggested_words'),
]


