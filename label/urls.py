from .views import LabelView , LabelViewMainu
# from rest_framework.routers import DefaultRouter
from django.urls import path, include

urlpatterns = [
    path('labels/', LabelView.as_view(), name='label-list-create'),
    path('labels/<int:pk>/',LabelViewMainu.as_view(), name='label-list-create')
]



