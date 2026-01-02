

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import TodoSerializer,LoginSerializer,UsersRegisterSerializer
from django.contrib.auth import authenticate
from .models import Todo
from django.contrib.auth.models import User
from .utils import generate_access_token, generate_refresh_token


@api_view(['POST']) 
@permission_classes([AllowAny]) 
def register(request): 
        user_reg_data=UsersRegisterSerializer(data=request.data) 
        if user_reg_data.is_valid(): 
                user = user_reg_data.save()
                return Response({"response":"registered successfully","user_id":user.id},status=status.HTTP_200_OK) 
        return Response(user_reg_data.errors,status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@permission_classes([AllowAny]) 
def login(request): 
        serializer=LoginSerializer(data=request.data) 
        if not serializer.is_valid(): 
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
        email=serializer.validated_data["email"] 
        password=serializer.validated_data["password"] 
        user = authenticate(request, username=email, password=password)
        if not user:
            return Response({"error":"invalid username or password"},status=status.HTTP_401_UNAUTHORIZED)
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        return Response({ 
                "message":"login successfull", 
                "access_token": access_token, 
                "refresh_token": refresh_token, 
                "username":user.first_name }) 


@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def create_todo(request): 
    t = TodoSerializer(data=request.data)
    if t.is_valid():
        t.save(user=request.user)   # ✅ now matches
        return Response({"response": t.data}, status=status.HTTP_201_CREATED)
    return Response(t.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST']) 
# @permission_classes([IsAuthenticated]) 
# def create_todo(request): 
#         t=TodoSerializer(data=request.data) 
#         if t.is_valid(): 
#                 t.save(user=request.user) 
#                 return Response({"response":t.data},status=status.HTTP_201_CREATED) 
#         return Response(t.errors,status=status.HTTP_400_BAD_REQUEST) 




@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def todoall(request): 
        todos=Todo.objects.filter(user=request.user) 
        serializer=TodoSerializer(todos,many=True) 
        return Response(serializer.data) 



@api_view(['GET']) 
@permission_classes([IsAuthenticated]) 
def todo_getone(request,todo_id): 
        try: 
                todo=Todo.objects.get(user=request.user,todo_id=todo_id) 
                serializer=TodoSerializer(todo) 
                return Response(serializer.data,status=status.HTTP_200_OK) 
        except Todo.DoesNotExist: 
 
                return Response({"reponse":"todo does not exist"}) 

        except Exception as e: 
                return Response({"message":str(e)})
                
                


@api_view(['PUT','PATCH']) 
@permission_classes([IsAuthenticated]) 
def update_todo(request,todo_id): 
        try: 
                todo=Todo.objects.get(user=request.user,todo_id=todo_id) 
                partial_update=(request.method=='PATCH') 
                serializer=TodoSerializer(todo,data=request.data,partial=partial_update) 
                if serializer.is_valid(): 
                        serializer.save() 
                        return Response(serializer.data) 
                return Response(serializer.errors) 
        except Todo.DoesNotExist: 
           return Response({"msg":"todo does not exist"},status=status.HTTP_404_NOT_FOUND) 
        
        except Exception as e: return Response({"msg":str(e)})
        
        

@api_view(['DELETE']) 
@permission_classes([IsAuthenticated]) 
def delete_todo(request,todo_id): 
        try: 
                t=Todo.objects.get(user=request.user,todo_id=todo_id) 
                t.delete() 
                return Response({"msg":"deleted"}) 
        except Todo.DoesNotExist: 
                return Response({"msg":"todo does not exist"},status=status.HTTP_404_NOT_FOUND) 
        except Exception as e: return Response({"msg":str(e)})



