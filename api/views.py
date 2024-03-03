from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from korisnici.models import Subscription, Novcanik, UserProfile, UserSubscription
from .serializers import RegistrationSerializer, SubscriptionSerializer, NovcanikSerializer, UserProfileSerializer, UserSubscriptionSerializer
from dj_rest_auth.views import LoginView
from rest_framework.permissions import AllowAny

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        print("Request data:", request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            print("Data is valid")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("Data is invalid:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        print("Login request data:", request.data)
        print("Login response data:", response.data)
        return response


class SubscriptionListView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

class SubscriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

class NovcanikListView(generics.ListCreateAPIView):
    queryset = Novcanik.objects.all()
    serializer_class = NovcanikSerializer

class NovcanikDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Novcanik.objects.all()
    serializer_class = NovcanikSerializer

class UserProfileListView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserSubscriptionListView(generics.ListCreateAPIView):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer

class UserSubscriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
