
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializer import UserRegistrationSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from  rest_framework_simplejwt.tokens import RefreshToken


    
class RegistrationUser(APIView):
    
    def post(self,request):
        
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # user_data= {"first_name": serializer.validated_data['first_name'],"Last_name":serializer.validated_data['last_name']}
            return Response({"Message": "User created successfully", "status": "Success","data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
       
class LoginUser(APIView):
    
    def post(self,request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
            # user = authenticate(request, email=serializer.validated_data['email'], password=serializer.validated_data['password'])
        serializer.save()
            # user_data = {"First_name":user.first_name,"Last_name":user.last_name,"email":user.email}
            
        token = RefreshToken.for_user(serializer.instance)
        return Response({"Message": "Login successful", "status": "Success","data":{'refresh':str(token),'access':str(token.access_token)}},status=status.HTTP_200_OK)
        #     return Response({'Message': 'Invalid credentials', "Status":"Error"},status=status.HTTP_401_UNAUTHORIZED)
        # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
        
        
    