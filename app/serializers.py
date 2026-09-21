import random
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()

class SenOtpSerializers(serializers.Serializer):
    email = serializers.EmailField()

    def save(self, **kwargs):
        email = self.validated_data['email']
        
        user, created = User.objects.get_or_create(email=email, defaults={'username': email})
        
        otp = random.randint(100000, 999999)
        
        cache.set(f'user_email:{email}', otp, timeout=300)
        
        send_mail(
            subject='Salom',
            message=f'Sizning OTP codingiz: {otp}',
            from_email='asilbekaxatov40@gmail.com',
            recipient_list=[email],
            fail_silently=False,
            )
        return user


class VerifySerializers(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        entered_otp = attrs.get('otp')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError('No user found with this email address.')
            
        cached_otp = cache.get(f'user_email:{email}')
        
        if not cached_otp or str(cached_otp) != str(entered_otp):
            raise ValidationError('Invalid or expired OTP code.')
            
        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        email = self.validated_data['email']
        cache.delete(f'user_email:{email}')
        
        return self.validated_data['user']