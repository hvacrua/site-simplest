from django.urls import path
from .views import NewClient, test_page


urlpatterns = [
    path('', NewClient.as_view()),
    path('test/', test_page),
    # path('json/', json_page)
]