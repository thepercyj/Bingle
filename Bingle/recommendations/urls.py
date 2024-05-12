from django.urls import path
from .views import recommendations_view, generate_rec, getborrowed

urlpatterns = [
    path('', recommendations_view, name='recommendations'),  # URL for recommendations_view
    path('generate-rec/', generate_rec, name='generate_rec'),  # URL for generate_rec
    path('get-borrowed/', getborrowed, name='get_borrowed'),  # URL for getborrowed
]
