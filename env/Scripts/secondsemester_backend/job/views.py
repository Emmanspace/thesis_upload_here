from rest_framework import status, authentication, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseBadRequest

# for user change/update
from django.shortcuts import get_object_or_404
from bson import ObjectId
from django.contrib.auth import authenticate, login
import logging
from rest_framework.generics import GenericAPIView


# import bycrypt
from rest_framework_simplejwt.tokens import RefreshToken

# for changestream
from django.http import StreamingHttpResponse
from bson.json_util import dumps
import json
import time

# for mongodb (updated)
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from job.models import Departments
from job.serializers import DepartmentSerializer
from rest_framework.decorators import api_view


# from django.shortcuts import render 
# Create your views here.
from .models import History, Category, Notification, totalSlots, availableSlots, parkingSlots, Departments, real_time, historytab, UserProfile, User#, userEdit
from .serializers import HistorySerializers, DashboardSerializers, announcementSerializer, notificationSerializer,totalSlot_Serializer, availableSlots_Serializer, parkingSlots_Serializer, DepartmentSerializer, real_time_serializer, historyserializer, UserSerializer, UserProfileSerializer, documentSerializer#, userEditSerializer

# for user update/change
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from pymongo import MongoClient
from bson.objectid import ObjectId
import pymongo


# for authentication
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import UserLoginSerializer



class notificationView(APIView):
    def get(self, request, format=None):
        notification = Notification.objects.all()[0:5]
        serializer = notificationSerializer(notification, many=True)

        return Response(serializer.data)

class announcementView(APIView):
    def get(self, request, format=None):
        announcement = History.objects.all()
        serializer = announcementSerializer(announcement, many=True)

        return Response(serializer.data)

class NewestHistoryView(APIView):
    def get(self, request, format=None):
        histories = History.objects.all()[0:4]
        serializer = HistorySerializers(histories, many=True)

        return Response(serializer.data)
    
class DashboardView(APIView):
    def get(self, request, pk, format=None):
        try:
            dashboard = History.objects.get(pk=39)
        except History.DoesNotExist:
            return Response({'error': 'History object not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DashboardSerializers(dashboard)
        return Response(serializer.data, status=status.HTTP_200_OK)

# for parking slots (dashboard)
class totalSlots_View(APIView):
    def get(self, request, format=None):
        total = totalSlots.objects.all()
        serialized_total = totalSlot_Serializer(total, many=True)
        return Response(serialized_total.data)

class availableSlots_View(APIView):
    def get(self, request, format=None):
        available = availableSlots.objects.all()
        serialized_avail = availableSlots_Serializer(available, many=True)
        return Response(serialized_avail.data)

class parkingSlots_View(APIView):
    def get(self, request, format=None):
        parking = parkingSlots.objects.all()
        serialized_parking = parkingSlots_Serializer(parking, many=True)
        return Response(serialized_parking.data)


# for mongoDB
@csrf_exempt
def departmentApi(request,id=0):
    if request.method=='GET':
        departments = Notification.objects.all()
        departments_serializer=notificationSerializer(departments,many=True)
        return JsonResponse(departments_serializer.data,safe=False)
    elif request.method=='POST':
        department_data=JSONParser().parse(request)
        departments_serializer=notificationSerializer(data=department_data)
        if departments_serializer.is_valid():
            departments_serializer.save()
            return JsonResponse("Added Successfully",safe=False)
        return JsonResponse("Failed to Add",safe=False)
    elif request.method=='PUT':
        department_data=JSONParser().parse(request)
        department=Departments.objects.get(DepartmentId=department_data['DepartmentId'])
        departments_serializer=DepartmentSerializer(department,data=department_data)
        if departments_serializer.is_valid():
            departments_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to Update")
    elif request.method=='DELETE':
        department=Departments.objects.get(DepartmentId=id)
        department.delete()
        return JsonResponse("Deleted Successfully",safe=False)



# for historytab
# total slots
@csrf_exempt
def totalSlotsApi(request, id=0):
    if request.method=='GET':
        total = totalSlots.objects.all()
        total_serializer = totalSlot_Serializer(total, many=True)
        return JsonResponse(total_serializer.data, safe=False)
    elif request.method=='POST':
        total_data=JSONParser().parse(request)
        total_serializer=totalSlot_Serializer(data=total_data)
        if total_serializer.is_valid():
            total_serializer.save()
            return JsonResponse("Total slot updated successfully.", safe=False)
        return JsonResponse("Total Slot update Failed.", safe=False)
   

# for available slots
@csrf_exempt
def availableApi(request, id=0):
    if request.method=='GET':
        avail = availableSlots.objects.all()
        avail_serializer = availableSlots_Serializer(avail, many=True)
        return JsonResponse(avail_serializer.data, safe=False)
    elif request.method=='POST':
        avail_data=JSONParser().parse(request)
        avail_serializer=availableSlots_Serializer(data=avail_data)
        if avail_serializer.is_valid():
            avail_serializer.save()
            return JsonResponse("Available slot updated successfully.", safe=False)
        return JsonResponse("Available Slot update Failed.", safe=False)

# for parking slots 
@csrf_exempt
def parkingApi(request, id=0):
    if request.method=='GET':
        parking = parkingSlots.objects.all()
        parking_serializer = parkingSlots_Serializer(parking, many=True)
        return JsonResponse(parking_serializer.data, safe=False)
    elif request.method=='POST':
        parking_data=JSONParser().parse(request)
        parking_serializer=parkingSlots_Serializer(data=parking_data)
        if parking_serializer.is_valid():
            parking_serializer.save()
            return JsonResponse("Available slot updated successfully.", safe=False)
        return JsonResponse("Available Slot update Failed.", safe=False)
# end of for history tab

# real_time 
@csrf_exempt
def realTimeApi(request, id=0):
    if request.method=='GET':
        real_time = real_time.objects.all()
        time_serializer = real_time_serializer(real_time, many=True)
        return JsonResponse(time_serializer.data, safe=False)
    elif request.method=='POST':
        real_time_data=JSONParser().parse(request)
        time_serializer=real_time_serializer(data=real_time_data)
        if time_serializer.is_valid():
            time_serializer.save()
            return JsonResponse("Real time addition is successful", safe=False)
        return JsonResponse("real time addition Failed.", safe=False)
   

# for history tab
@csrf_exempt
def historyApi(request, id=0):
    if request.method=='GET':
        histories = historytab.objects.all()
        history_serializer = historyserializer(histories, many=True)
        return JsonResponse(history_serializer.data, safe=False)
    elif request.method=='POST':
        histories_data=JSONParser().parse(request)
        history_serializer=historyserializer(data=histories_data)
        if history_serializer.is_valid():
            history_serializer.save()
            return JsonResponse("history addition is successful", safe=False)
        return JsonResponse("history addition Failed.", safe=False)

#SSE
@csrf_exempt
def sse(request):
    def count_documents():
        client = MongoClient('mongodb+srv://villagraemmanuel:secondsemesterthesis@secondsemester-mongodb.7mf5tnr.mongodb.net/?retryWrites=true&w=majority&appName=secondsemester-mongoDB')  # Replace with your MongoDB connection string
        db = client['thesis_db2']  # Replace 'mydatabase' with your database name
        collection = db['job_totalslots']  # Replace 'mycollection' with your collection name
        count = collection.count_documents({})
        return count

    def event_stream():
        client = MongoClient('mongodb+srv://villagraemmanuel:secondsemesterthesis@secondsemester-mongodb.7mf5tnr.mongodb.net/?retryWrites=true&w=majority&appName=secondsemester-mongoDB')
        db = client['thesis_db2']
        my_collection = db['job_real_time']

        pipeline = [{'$match': {'operationType': {'$in': ['insert', 'update', 'delete']}}}]
        with my_collection.watch(pipeline) as stream:
            # for counting the documents in a collection
            initial_count = my_collection.count_documents({})
            yield f"event: {json.dumps({'operation': 'initial_count', 'count': initial_count})}\n\n"

            # orig
            for change in stream:
                data = json.dumps(change)
                yield f"event: {data}\n\n"
                time.sleep(1)  # Optional delay between events

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['Connection'] = 'keep-alive'
    del response['Connection']
    response.close()
    return response

# for counting the documents
@csrf_exempt
def count_documents(request):
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb+srv://villagraemmanuel:secondsemesterthesis@secondsemester-mongodb.7mf5tnr.mongodb.net/?retryWrites=true&w=majority&appName=secondsemester-mongoDB')  # Replace with your MongoDB connection string
        db = client['thesis_db2']  # Replace 'mydatabase' with your database name
        collection = db['job_real_time']  # Replace 'mycollection' with your collection name
        # Count the total number of documents in the collection
        total_count = collection.count_documents({})
        # Close MongoDB connection
        client.close()
        # Return the total count as JSON response
        return JsonResponse({'total_count': total_count})
    
    except Exception as e:
        # Handle exceptions, such as connection errors or collection not found
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def decrement_documents(request):
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb+srv://villagraemmanuel:secondsemesterthesis@secondsemester-mongodb.7mf5tnr.mongodb.net/?retryWrites=true&w=majority&appName=secondsemester-mongoDB')  # Replace with your MongoDB connection string
        db = client['thesis_db2']  # Replace 'mydatabase' with your database name
        collection = db['job_real_time']  # Replace 'mycollection' with your collection name
        
        # Count the total number of documents in the collection
        total_count = collection.count_documents({})
        if total_count >0:
            collection.update_many({}, {'$inc': {'total_count': -1}})
        
        updated_count = collection.count_documents({})
        # Close MongoDB connection
        client.close()
        
        # Return the total count as JSON response
        return JsonResponse({'total_count': updated_count})
    
    except Exception as e:
        # Handle exceptions, such as connection errors or collection not found
        return JsonResponse({'error': str(e)}, status=500)

# for fetching mongodb collection into frontend table (history tab)
@csrf_exempt
def get_documents(request):
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb+srv://villagraemmanuel:secondsemesterthesis@secondsemester-mongodb.7mf5tnr.mongodb.net/?retryWrites=true&w=majority&appName=secondsemester-mongoDB')  # Replace with your MongoDB connection string
        db = client['thesis_db2']  # Replace 'mydatabase' with your database name
        collection = db['PlateLogs']  # Replace 'mycollection' with your collection name

        limit = int(request.GET.get('limit',7 ))
        documents = list(collection.find().limit(limit))
        client.close()

        return JsonResponse(documents, safe=False)
    
    except Exception as e:
        # Handle exceptions, such as connection errors or collection not found
        return JsonResponse({'error': str(e)}, status=500)
    

# @csrf_exempt
# def user_profile(request, user_id=None):
#     if request.method == 'GET':
#         # If user_id is None, fetch profile of currently logged-in user
#         if user_id is None:
#             if request.user.is_authenticated:
#                 user_id = request.user.id
#             else:
#                 return JsonResponse({'error': 'User is not authenticated'}, status=401)
        
#         # Connect to MongoDB and fetch user profile
#         client = MongoClient('mongodb+srv://villagraemmanuel:secondsemesterthesis@secondsemester-mongodb.7mf5tnr.mongodb.net/?retryWrites=true&w=majority&appName=secondsemester-mongoDB')
#         db = client['thesis_db2']
#         collection = db['auth_user']  # Replace with your collection name
        
#         user_profile = collection.find_one({'_id': ObjectId(user_id)})
        
#         if user_profile:
#             return JsonResponse(user_profile, safe=False)
#         else:
#             return JsonResponse({'error': 'User profile not found'}, status=404)

#     elif request.method == 'PUT':
#         # Only allow updating profile of currently logged-in user
#         if user_id is None or user_id == str(request.user.id):
#             return update_user_profile(request, user_id)
#         else:
#             return JsonResponse({'error': 'Unauthorized'}, status=403)
#     else:
#         return JsonResponse({'error': 'Invalid HTTP Method'}, status=405)

# @login_required
# def update_user_profile(request, user_id):
#     try:
#         data = json.loads(request.body)
#     except json.JSONDecodeError as e:
#         return JsonResponse({'error': 'Invalid JSON format'}, status=400)

#     # Connect to MongoDB and update user profile
#     client = MongoClient('mongodb+srv://villagraemmanuel:secondsemesterthesis@secondsemester-mongodb.7mf5tnr.mongodb.net/?retryWrites=true&w=majority&appName=secondsemester-mongoDB')
#     db = client['thesis_db2']
#     collection = db['auth_user']  # Replace with your collection name
    
#     result = collection.update_one({'_id': ObjectId(user_id)}, {'$set': data})
    
#     if result.modified_count > 0:
#         return JsonResponse({'message': 'User profile updated successfully'})
#     else:
#         return JsonResponse({'error': 'User profile not found'}, status=404)
#end of user update/change

# for authentication
class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
# end of authentication

# auth2
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
# end of auth2

# profile update
# client = MongoClient('mongodb+srv://villagraemmanuel:secondsemesterthesis@secondsemester-mongodb.7mf5tnr.mongodb.net/?retryWrites=true&w=majority&appName=secondsemester-mongoDB')
# db = client['thesis_db2']
# collection = db['auth_user']  # Replace with your collection name

# class UserProfileDetail(APIView):
#     def get(self, request):
#         user_id = str(request.user.id)
#         user_profile = collection.find_one({'_id': ObjectId(user_id)})

#         if user_profile:
#             return JsonResponse(user_profile, status=200)
#         else:
#             return JsonResponse({'error': 'User Profile not found'}, status=404)
    
#     def put(self, request):
#         user_id = str(request.user.id)
#         data = json.loads(request.body)
#         updated_profile = collection.find_one_and_update(
#             {'_id': ObjectId(user_id)},
#             {'$set':data},
#             return_document =True
#         )

#         if updated_profile:
#             return JsonResponse(updated_profile, status=200)
#         else:
#             return JsonResponse({'error': 'User Profile not found'}, status=404)
# # end of profile update

# comparison

@csrf_exempt
def get_documents(request):
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb+srv://villagraemmanuel:secondsemesterthesis@secondsemester-mongodb.7mf5tnr.mongodb.net/?retryWrites=true&w=majority&appName=secondsemester-mongoDB')  # Replace with your MongoDB connection string
        db = client['thesis_db2']  # Replace 'mydatabase' with your database name
        collection = db['PlateLogs']  # Replace 'mycollection' with your collection name

        limit = int(request.GET.get('limit',7 ))
        documents = list(collection.find().limit(limit))
        client.close()

        return JsonResponse(documents, safe=False)
    
    except Exception as e:
        # Handle exceptions, such as connection errors or collection not found
        return JsonResponse({'error': str(e)}, status=500)
    
# end of comparison
# logger = logging.getLogger(__name__)
# class UserProfileDetail(APIView): #originally APIView
#     def __init__(self):
#         super().__init__()
#         self.client = MongoClient('mongodb+srv://villagraemmanuel:secondsemesterthesis@secondsemester-mongodb.7mf5tnr.mongodb.net/?retryWrites=true&w=majority&appName=secondsemester-mongoDB')
#         self.db = self.client['thesis_db2']
#         self.collection = self.db['auth_user']
    
    # def get(self, request, *args, **kwargs):
    #     id = request.query_params["id"]
    #     print(id)

    #     profile = self.get_queryset()
    #     serializer = UserProfileSerializer(profile, many=True)
    #     return Response (serializer.data)

    # this is the orignial
    # def get(self, request):
    #     try:
    #         user = request.user
    #         user_profile = get_object_or_404(User, pk=user.id)
    #         # user_id = str(request.user.id)
    #         user_id = user.pk

    #         if user_id:
    #             object_id = ObjectId(str(user_id))
    #             # mongo_user_profile = self.collection.find_one({'_id': object_id})
    #             mongo_user_profile = self.collection.find_one({'_id': object_id})

    #         else:
    #             return JsonResponse({'error0': 'user id not found'}, status=404)
            
    #         if mongo_user_profile is None:
    #             # user_profile['_id'] = str(user_profile['_id']) #added
    #             self.logger.error('User profile is not found in mongodb for ID: %s', user_id)
    #             return JsonResponse({'error1': 'User Profile not found'}, status=404)
    #             # return JsonResponse(user_profile, status=200)

    #         combined_profile = {
    #             'id': user_profile.id,
    #             'username': user_profile.username,
    #             'first_name' : mongo_user_profile['first_name'],
    #             'last_name':  mongo_user_profile['last_name'],
    #             'email': mongo_user_profile['email']
    #         }
    #         return JsonResponse(combined_profile, status=200)
    #     except Exception as e:
    #         return JsonResponse({'error2': str(e)}, status=400)  # Handle invalid user ID
    # # end of the originial
   
    # def put(self, request):
    #     try:
    #         # user_id = request.user.id
    #         # user_id = '6623b2d478cc1b15298e2f7d'
    #         # object_id = ObjectId(user_id)

    #         # data = json.loads(request.body)
    #         user = request.user
    #         user_id = user.pk
    #         user_id_str = str(user_id)
    #         object_id = ObjectId(user_id_str)
            
    #         if not request.data.get('first_name') or not request.data.get('last_name') or not request.data.get('email'):
    #             return JsonResponse({'error3': 'missing required fields in request body'}, status=400)
    #         data = json.loads(request.body)

    #         # self.collection.update_one({'_id': object_id}, {set:{
    #         self.collection.update_one({'_id': object_id}, {set:{
    #             'first_name': data['first_name'],
    #             'last_name': data['last_name'],
    #             'email': data['email'],
    #         }})
    #     # try:
    #     #     # user_id = ObjectId(str(user_id))

    #     #     self.collection.update_one({'id': object_id}, {'$set':{
    #     #     'first_name': data['first_name'],
    #     #     'last_name': data['last_name'],
    #     #     'email': data['email'],
    #     #     'password': data['password']
    #     #     }})
           
    #         return JsonResponse({'message': 'Profile Updated successfully'}, status=200)
    #     except Exception as e:
    #         return JsonResponse({'error4': str(e)}, status=400)


# 2:26 am
client = MongoClient('mongodb+srv://villagraemmanuel:secondsemesterthesis@secondsemester-mongodb.7mf5tnr.mongodb.net/?retryWrites=true&w=majority&appName=secondsemester-mongoDB')
db = client['thesis_db5']
collection = db['auth_user']

# PUT
# @csrf_exempt
class UpdateDocumentView(GenericAPIView):
    serializer_class = documentSerializer
    
    def put(self, request, pk):
        try:
            
            document_id = ObjectId(pk)
            document = collection.find_one({"_id": document_id})

            if not document:
                return Response({'error1': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.get_serializer(document, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            collection.update_one({"_id": document_id}, {"$set": serializer.validated_data})

            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# GET
@csrf_exempt
@api_view(['GET'])
def get (self, id):
        try:
            client = MongoClient('mongodb+srv://villagraemmanuel:secondsemesterthesis@secondsemester-mongodb.7mf5tnr.mongodb.net/?retryWrites=true&w=majority&appName=secondsemester-mongoDB')
            db = client['thesis_db2']
            collection = db['auth_user']
            # Look up document by "id" field

            document = collection.find_one({"id": id})

            if not document:
                return Response({'error1': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

            # Extract "id" field (handle potential missing field)
            document_id = document.get('id')
            if document_id is None:
                return Response({'error2': 'Document does not have an "id" field'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(document)

            serialized_data = {
                'id': document.get('id'),
                'username': document.get('username')
            }
            return Response(serialized_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error3': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#end of 2:26 am
# this is for getting all the documents
@csrf_exempt
@api_view(['GET'])

def get_user(request):
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb+srv://villagraemmanuel:secondsemesterthesis@secondsemester-mongodb.7mf5tnr.mongodb.net/?retryWrites=true&w=majority&appName=secondsemester-mongoDB')  # Replace with your MongoDB connection string
        db = client['thesis_db2']  # Replace 'mydatabase' with your database name
        collection = db['auth_user']  # Replace 'mycollection' with your collection name

        limit = int(request.GET.get('limit',7 ))
        documents = list(collection.find().limit(limit))
        for doc in documents:
            doc['_id'] = str(doc['_id'])
        client.close()

        return JsonResponse(documents, safe=False)
    
    except Exception as e:
        # Handle exceptions, such as connection errors or collection not found
        return JsonResponse({'error': str(e)}, status=500)


# 4-23

# @api_view(['GET', 'POST', 'DELETE'])
# def user_list(request):
#     if request.method == 'GET':
#         tutorials = userEdit.objects.all()
        
#         title = request.GET.get('title', None)
#         if title is not None:
#             tutorials = tutorials.filter(title__icontains=title)
        
#         tutorials_serializer = userEditSerializer(tutorials, many=True)
#         return JsonResponse(tutorials_serializer.data, safe=False)
#         # 'safe=False' for objects serialization
 
#     elif request.method == 'POST':
#         tutorial_data = JSONParser().parse(request)
#         tutorial_serializer = userEditSerializer(data=tutorial_data)
#         if tutorial_serializer.is_valid():
#             tutorial_serializer.save()
#             return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
#         return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         count = userEdit.objects.all().delete()
#         return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
# @api_view(['GET', 'PUT', 'DELETE'])
# def user_detail(request, pk):
#     try: 
#         tutorial = userEdit.objects.get(pk=pk) 
#     except userEdit.DoesNotExist: 
#         return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
#     if request.method == 'GET': 
#         tutorial_serializer = userEditSerializer(tutorial) 
#         return JsonResponse(tutorial_serializer.data) 
 
#     elif request.method == 'PUT': 
#         tutorial_data = JSONParser().parse(request) 
#         tutorial_serializer = userEditSerializer(tutorial, data=tutorial_data) 
#         if tutorial_serializer.is_valid(): 
#             tutorial_serializer.save() 
#             return JsonResponse(tutorial_serializer.data) 
#         return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
#     elif request.method == 'DELETE': 
#         tutorial.delete() 
#         return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
# @api_view(['GET'])
# def user_list_published(request):
#     tutorials = userEdit.objects.filter(published=True)
        
#     if request.method == 'GET': 
#         tutorials_serializer = userEditSerializer(tutorials, many=True)
#         return JsonResponse(tutorials_serializer.data, safe=False)
# 4-23

def register_user(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            plate = request.POST.get('plate', None)  # Handle optional plate field

            user = User.objects.create_user(username, '', password, first_name,'', last_name,'', email, '', plate,'')  # Update with your user model
            # user = User.objects.create_user(username, '', password)  # Update with your user model
            user.first_name = first_name
            user.last_name = last_name
            user.plate = plate
            user.save()

            return JsonResponse({'message': 'Registration successful!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
