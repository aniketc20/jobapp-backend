from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from users.models import Application, CustomUser, Job
from rest_framework.parsers import FormParser , MultiPartParser

#Serializer to Register User
class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'name', 'password']
    def validate(self, attrs):
        if attrs['password'] == "None":
            raise serializers.ValidationError(
            {"password": "Password fields didn't match."})
        return attrs
    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name']
            )
        user.set_password(validated_data['password'])
        user.save()
        return user

# Login view
class LoginSerializer(serializers.Serializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'token']
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if user:
                try:
                    token = Token.objects.get(user_id=user.id)

                except Token.DoesNotExist:
                    token = Token.objects.create(user=user)
        else:
            msg = ('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        response = {}
        response['token'] = token.key
        response['email'] = user
        return response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'name']


class JobSerializer(serializers.ModelSerializer):
    posted_by = serializers.CharField(source='posted_by.name')
    applied_by = UserSerializer(read_only=True, many=True)
    accepted_candidate = UserSerializer(read_only=True, many=True)
    rejected_candidate = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Job
        fields = ['id', 'desc', 'posted_by', 'applied_by', 'accepted_candidate', 'rejected_candidate']
    def create(self, validated_data):
        print(validated_data)
        job = Job.objects.create(
            posted_by = self.context['request'].user,
            desc=validated_data['desc'],
            )
        job.save()
        return job


class ApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    applied_by = serializers.CharField(source='applied_by.username')
    resume = serializers.FileField()
    parser_classes = [FormParser , MultiPartParser]

    class Meta:
        model = Application
        fields = ['id', 'job', 'status', 'applied_by', 'resume']

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    def create(self, validated_data):
        try:
            application = Application.objects.create(
                    applied_by = self.context['request'].user,
                    resume = validated_data['resume']
                    )
            application.save()
            return application
        except Exception as e:
            raise serializers.ValidationError(e)

    # def validate(self, data):
    #     print(data)
    #     applied_by = data.get('applied_by')['id']
    #     #job = data.get('job')
    #     response = {}
    #     #response['job'] = job
    #     response['applied_by'] = applied_by
    #     return response
