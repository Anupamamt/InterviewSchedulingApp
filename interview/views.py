from drf_yasg import openapi
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime,timedelta

from .serializers import UserSerializer
from .models import User

class AddUser(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'role': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['Candidate', 'Interviewer', 'HR'] 
                ),
            },
        ),
        operation_description='Function to add user',
        responses={
            200: 'Success',
            400: 'Bad Request',
            404: 'Not Found',
            500:'Internal Server Error'
        },
    )

    def post(self, request, format=None):

        """
        Function to add user

        Required POST parameters:
        - name :Name of the user
        - role - Role of the user(Candidate/Interviewer/HR)

        rtype - json

        """

        try:

            if not request.data.get('name') or not request.data.get('role'):
                return Response(f'Please fill all mandatory fields', status=400)
            
            if request.data.get('role') not in ['Candidate','Interviewer','HR']:
                return Response(f'Please enter a valid role(Candidate/Interviewer/HR).', status=400)
            
            user = User.objects.create(
                name=request.data.get('name'),
                role=request.data.get('role')
            )
            return Response(f'User added successfully with id {user.id}', status=200)

        except Exception as e:
            return Response(str(e), status=500)
        

class GetUsers(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description='The search key (optional)',
            ),
        ],
    )

    def get(self, request, format=None):

        """
        Function to get all users list

        Required POST parameters:
        - name :Name of the user
        - role - Role of the user(Candidate/Interviewer/HR)

        rtype - json

        """
        
        try:

            users = []
            key_to_search = request.GET.get('search')

            if key_to_search:
                user_queryset = User.objects.filter(Q(name__icontains=key_to_search) | Q(role__icontains=key_to_search))
            else:
                user_queryset = User.objects.all()

            users_data = UserSerializer(user_queryset,many=True)

            for user_data in users_data.data:
                users.append({
                    'id':user_data.get('id'),
                    'name':user_data.get('name'),
                    'role':user_data.get('role')
                })
            return Response(users, status=200)

        except Exception as e:
            return Response(str(e), status=500)
        

class AddAvailableTime(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'from': openapi.Schema(type=openapi.TYPE_STRING,format='date-time'), 
                                    'to': openapi.Schema(type=openapi.TYPE_STRING,format='date-time'), 
                                }
                            ),

        operation_description='Function to add available time',
        responses={
            200: 'Success',
            400: 'Bad Request',
            404: 'Not Found',
            500:'Internal Server Error'
        },
    )

    def put(self, request, id):

        """
        Function to add availavle time of candidate and interviewer

        Required POST parameters:

         - slots : Details of the available time of user
            from: The string representing the available from date and time. 
                Supported format - "YYYY-MM-DD HH:MM" (e.g., "2025-01-26T04:47:36.672Z")
            to: The string representing the available from date and time. 
                Supported format - "YYYY-MM-DD HH:MM" (e.g., "2025-01-26T04:47:36.672Z")

        rtype - json

        """

        try:

            user = User.objects.get(id=id)

            slot = request.data
            if slot.get('from') and slot.get('to'):
                try:
                    _  = datetime.strptime(slot.get('from'), "%Y-%m-%dT%H:%M:%S.%fZ")
                    _  = datetime.strptime(slot.get('to'), "%Y-%m-%dT%H:%M:%S.%fZ")

                except Exception as _:
                    return Response('Invalid time format',status=400)
                
            else:
                return Response('Invalid slot format',status=400)


            user.available_time = slot
            user.save()

            return Response(f'Time slot added successfully', status=200)

        except Exception as e:
            return Response(str(e), status=500)
        

class GetAvailableTime(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='candidate_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=False,
                description='The candidate id (optional)',
            ),
            openapi.Parameter(
                name='interviewer_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=False,
                description='The interviewer id (optional)',
            ),
        ],
    )

    def get(self, request, format=None):

        """
        Function to get available time

        Required Query parameters:
        - candidate_id :Id of the candidate
        - interviewer_id - Id of the interviewer

        rtype - json

        """
        
        try:

            available_time_slots = []
            candidate = User.objects.get(id=request.GET.get('candidate_id'))
            interviewer = User.objects.get(id=request.GET.get('interviewer_id'))

            candidate_slot = candidate.available_time
            interviewer_slot = interviewer.available_time

            from_time = max(datetime.strptime(candidate_slot.get('from'), "%Y-%m-%dT%H:%M:%S.%fZ"),datetime.strptime(interviewer_slot.get('from'), "%Y-%m-%dT%H:%M:%S.%fZ"))                
            to_time = min(datetime.strptime(candidate_slot.get('to'), "%Y-%m-%dT%H:%M:%S.%fZ"),datetime.strptime(interviewer_slot.get('to'), "%Y-%m-%dT%H:%M:%S.%fZ"))                

            i = from_time

            while i < to_time and i+timedelta(hours=1) <= to_time:
                available_slot = (i,i+timedelta(hours=1))
                available_time_slots.append(available_slot)
                i = i+timedelta(hours=1)

            return Response(available_time_slots, status=200)

        except Exception as e:
            return Response(str(e), status=500)
        
