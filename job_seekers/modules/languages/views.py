from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from worktually_v3_api.custom_jwt.jwt import JobSeekerJWTAuthentication
from .models import Language
from .serializers import LanguageSerializer

class AddLanguageView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=LanguageSerializer,
        responses={
            201: openapi.Response("Language added successfully.", LanguageSerializer),
            400: "Bad Request",
        },
        operation_description="Add a language entry.",
        examples={
            "application/json": {
                "language": "English",
                "proficiency": "Advanced",
            }
        },
    )
    def post(self, request):
        data = request.data.copy()
        data['job_seeker'] = request.user.id  # Automatically set job_seeker to the logged-in user ID
        serializer = LanguageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "message": "Language added successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateLanguageView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=LanguageSerializer,
        responses={
            200: openapi.Response("Language updated successfully.", LanguageSerializer),
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Update a language entry.",
        examples={
            "application/json": {
                "language": "English",
                "proficiency": "Advanced",
            }
        },
    )
    def put(self, request):
        # Retrieve the language entry for the logged-in user
        language = Language.objects.filter(job_seeker=request.user).first()
        if not language:
            return Response(
                {"status": "error", "message": "Language not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = LanguageSerializer(language, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "message": "Language updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteLanguageView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: "Language deleted successfully.", 404: "Not Found"},
        operation_description="Delete a language entry.",
    )
    def delete(self, request):
        # Retrieve the language entry for the logged-in user
        language = Language.objects.filter(job_seeker=request.user).first()
        if not language:
            return Response(
                {"status": "error", "message": "Language not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        language.delete()
        return Response(
            {"status": "success", "message": "Language deleted successfully"},
            status=status.HTTP_200_OK,
        )