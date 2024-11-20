from django.contrib.auth import authenticate
from .models import CustomUser
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist

class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'user': UserSerializer(response.data).data,
            'message': 'User successfully created.'
        })





class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username_or_email = request.data.get('username') or request.data.get('email')
        password = request.data.get('password')

        if not username_or_email or not password:
            return Response({"detail": "Username/Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if it's an email or username and try to authenticate
        try:
            if '@' in username_or_email:  # If it's an email, find the user by email
                user = CustomUser.objects.get(email=username_or_email)
            else:  # If it's a username, find the user by username
                user = CustomUser.objects.get(username=username_or_email)

            # Now authenticate the user
            user = authenticate(username=user.username, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': "User login Successfully done!",
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    }
                })
            else:
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
