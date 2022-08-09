from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication

from users.models import Application, CustomUser, Job
from .serializers import RegisterSerializer, JobSerializer, ApplicationSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username
        })


@api_view(['POST'])
def register(request):
    data = JSONParser().parse(request)
    serializer = RegisterSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getJobs(request):
    queryset = Job.objects.exclude(posted_by=request.user)
    data = JobSerializer(queryset, many=True, context={'request': request})
    return JsonResponse(data.data, status=200, safe=False)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createJob(request):
    data = JSONParser().parse(request)
    serializer = JobSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def apply(request):
    data = request.data
    print(data)
    job = Job.objects.get(id=data['job'])
    serializer = ApplicationSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        job.applied_by.add(request.user)
        job.save()
        application = Application.objects.get(id=serializer.data['id'])
        application.job = job
        application.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)
    # return JsonResponse({"error":"cannot apply"})


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def applications(request):

    if request.method=="GET":
        queryset = Application.objects.filter(job__posted_by=request.user.id)
        data = ApplicationSerializer(queryset, many=True)
        return JsonResponse(data.data, status=200, safe=False)

    if request.method=="POST":
        data = JSONParser().parse(request)
        serializer = ApplicationSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['PUT'])
def update_application(request):
    if request.method == 'PUT':
        application = Application.objects.get(pk=request.data['applicationId'])
        serializer = ApplicationSerializer(application, data=request.data, partial=True)
  
        if serializer.is_valid():
            job = Job.objects.get(id=request.data['job'])
            serializer.save()
            applied_by = CustomUser.objects.get(username=request.data['applied_by'])
            print(applied_by.id)
            if(request.data['status']=='accepted'):
                job.accepted_candidate.add(applied_by.id)
            elif(request.data['status']=='rejected'):
                job.rejected_candidate.add(applied_by.id)
            job.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=404)
