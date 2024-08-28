from .views import LabelView , LabelViewMainu
# from rest_framework.routers import DefaultRouter
from django.urls import path, include

urlpatterns = [
    path('label/', LabelView.as_view(), name='label-list-create'),
    path('label/<int:pk>/',LabelViewMainu.as_view(), name='label-list-create')
]



