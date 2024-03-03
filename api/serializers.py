from rest_framework import serializers
from django.contrib.auth.models import User
from korisnici.models import Subscription, Novcanik, UserProfile, UserSubscription
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email već postoji.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        password = data.get('password')
        password2 = data.pop('password2')  # Uklanjamo password2 iz data
        if password != password2:
            raise serializers.ValidationError({'password': 'Lozinke se ne podudaraju.'})
        return data

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'email', 'first_name', 'last_name')
        read_only_fields = ('email',)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['ime', 'prezime', 'drzava', 'email', 'broj_mobitela']

class NovcanikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Novcanik
        fields = ['balance']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['naziv', 'cijena', 'trajanje_u_danima']

class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = ['korisnik', 'pretplata', 'datum_pocetka', 'datum_isteka']
