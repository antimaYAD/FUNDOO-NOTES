from .views import LabelView 
# from rest_framework.routers import DefaultRouter
from django.urls import path, include

urlpatterns = [
    path('mixin/', LabelView.as_view(), name='label-list-create'),
    path('mixinlabel/<int:pk>/',LabelView.as_view(), name='label-retive-delete-update')
]



