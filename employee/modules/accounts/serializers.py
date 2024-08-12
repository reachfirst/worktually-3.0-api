from rest_framework import serializers
from employee.models import Employee, OTP
from django.contrib.auth import authenticate
from employee.models import Role


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        ref_name = "EmployeeLoginSerializer"
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        # Remove confirm_password field
        confirm_password = validated_data.pop('confirm_password', None)
        
        # Create a new employee instance with the validated data
        employee = Employee.objects.create_user(**validated_data)
        return employee

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        ref_name = "EmployeeLoginSerializer"

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password", code='authentication_failed')
        else:
            raise serializers.ValidationError("Both email and password are required", code='invalid_credentials')

        data['user'] = user
        return data

class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'email', 'first_name', 'last_name', 'phone']

    
class LogoutSerializer(serializers.Serializer):
    pass


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not Employee.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is not registered.")
        return value

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')
        if not OTP.objects.filter(email=email, otp=otp, is_verified=False).exists():
            raise serializers.ValidationError("Invalid OTP.")
        return data

class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.UUIDField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        token = data.get('token')
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if not OTP.objects.filter(email=email, reset_token=token).exists():
            raise serializers.ValidationError("Invalid or expired token.")
        return data

    def save(self):
        validated_data = self.validated_data
        otp_instance = OTP.objects.get(email=validated_data['email'], reset_token=validated_data['token'])
        employee = Employee.objects.get(email=validated_data['email'])
        employee.set_password(validated_data['new_password'])
        employee.save()
        # Invalidate the OTP and token after successful password reset
        otp_instance.delete()
        return validated_data
    

class RoleSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Role
        fields = ['id', 'name', 'created_by']





