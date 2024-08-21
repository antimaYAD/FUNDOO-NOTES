from django.shortcuts import render
from rest_framework import mixins,viewsets
from rest_framework.response import Response

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from .models import Label
from rest_framework import generics
from .serializers import LableSerialiser
from loguru import logger
# Create your views here.

class LabelView(mixins.CreateModelMixin,
                mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                mixins.UpdateModelMixin,
                generics.GenericAPIView):
    
    
    
    queryset = Label.objects.all()
    serializer_class = LableSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        try:
            if 'pk' in kwargs:
                return self.retrieve(request, *args, **kwargs)
            else:
                return self.list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error retrieving Label: {str(e)}")
            return Response({"error": "Error retrieving Label", "detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def post(self,request,*args, **kwargs):
        
        try:
            serializer = LableSerialiser(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            headers = self.get_success_headers(serializer.data)
            # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            return self.create(request,*args, **kwargs)
            
        except Exception as e:
            logger.error(f"Error creating Label: {str(e)}")
            return Response({"error": "Error creating Label", "detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
    def put(self,request,*args, **kwargs):
        
        try:
            self.update(request,*args, **kwargs)
            return Response({"message": "Label updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error updating Label: {str(e)}")
            return Response({
                'error': 'An error occurred while Updating the note.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
            
            
            
    def patch(self,request,*args, **kwargs):
        try:
            self.partial_update(request,*args, **kwargs)
            return Response({"message": "Label updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error updating Label: {str(e)}")
            return Response({"error": "Error updating Label", "detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            
        
    def delete(self, request, *args, **kwargs):
        """
        Delete a specific note by its ID.
        """
        try:
            self.destroy(request,*args, **kwargs)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error deleting note with ID {pk}: {str(e)}")
            return Response({
                'error': 'An error occurred while deleting the note.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)