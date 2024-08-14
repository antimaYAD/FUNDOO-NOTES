# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import User
# from .utils import is_valid_email,is_valid_password,is_validate_name
# from django.contrib.auth import authenticate
# from django.views.decorators.csrf import csrf_exempt
# import json
# from django.forms.models import model_to_dict


# Create your views here.

# def register_user(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#         except json.JSONDecodeError:
#             return JsonResponse({"Message": "Invalid JSON","status":"Error"}, status=400)
        
#         email = data.get('email')
#         password = data.get('password')
#         f_name = data.get('f_name')
#         l_name = data.get('l_name')
        
#         if not f_name or not l_name or not email or not password :
#             return JsonResponse({"Message": "Please fill all the fields","status":"Error"}, status=400)
        
#         name_error=is_validate_name(f_name)
#         if name_error:
#             return JsonResponse({"error":"The format of firstname is invalid"}, status=400)
        
#         name_error = is_validate_name(l_name)
#         if name_error:
#             return JsonResponse({"error":"The format of lastname is invalid"}, status=400)
        
#         email_error = is_valid_email(email)
#         if email_error:
#             return JsonResponse({"error":"Inavalid email format"}, status=400)
        
#         password_error = is_valid_password(password)
#         if password_error:
#             return JsonResponse({"error":"Invalid password formate"}, status=400)
        
#         if User.objects.filter(email=email).exists():
#             return JsonResponse({"error":"Email already exists"}, status=400)
        
#         # user = User.objects.create_user(l_name=l_name,f_name=f_name,email=email,password=password)
#         user = User.objects.create_user(
#             first_name=f_name,
#             last_name=l_name,
#             email=email,
#             password=password
#         )
        
#         user_dict = model_to_dict(user)
        
#         user_data = {"First_name":user_dict['first_name'],
#                      "Last_name":user_dict['last_name']}
    
#         return JsonResponse({'message': 'User registered successfully',"status":"Success","data":user_data}, status=201)
#     return JsonResponse({'error': 'Method not allowed'}, status=405)


# def login_user(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#         except json.JSONDecodeError:
#             return JsonResponse({"Message": "Invalid JSON","status":"Error"}, status=400)
               
#         email = data.get('email')
#         password = data.get('password')
#         # print(email,password)
#         if not email or not password:
#             return JsonResponse({"Error":"Requierd files not filled"},status=400)

        
        
#         user = authenticate(request, email=email, password=password)
        
#         if user is not None:
#             user_data = {"First_name":user.first_name,
#                          "Last_name":user.last_name,
#                          "email":user.email,
#                          }
            
#             return JsonResponse({"Message": "Login successful", "status": "Success","data":user_data}, status=200)
        
#         else:
#             return JsonResponse({'Message': 'Invalid credentials', "Status":"Error"}, status=401)
        
    
#     return JsonResponse({'error': 'Method not allowed'}, status=405)
     

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
        
        
        
        
        
        
        
    