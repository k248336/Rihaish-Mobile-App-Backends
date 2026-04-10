from django.urls import path
from .views import FavoriteListView, ToggleFavoriteView

urlpatterns = [
    path('favorites', FavoriteListView.as_view(), name='favorite_list'),
    path('favorites/<int:property_id>', ToggleFavoriteView.as_view(), name='toggle_favorite'),
]
