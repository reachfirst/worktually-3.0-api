from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from worktually_v3_api.custom_jwt.jwt import JobSeekerJWTAuthentication
from .models import Education
from .serializers import EducationSerializer
from job_seekers.models import JobSeeker


class AddEducationView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=EducationSerializer,
        responses={
            201: openapi.Response("Education added successfully.", EducationSerializer),
            400: "Bad Request",
        },
        operation_description="Add an education entry.",
        examples={
            "application/json": {
                "title": "Bachelor of Science",
                "degree_type": "BSc",
                "discipline": "Computer Science",
                "institute_name": "University of Example",
                "from_date": "2020-01-01",
                "to_date": "2023-12-31"
            }
        },
    )
    def post(self, request):
        job_seeker_id = request.user.id  # Get the job_seeker_id from the token

        # Merge the job_seeker_id into the request data
        data = request.data.copy()
        data['job_seeker'] = job_seeker_id

        # Pass the request object in the context
        serializer = EducationSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "message": "Education added successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UpdateEducationView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=EducationSerializer,
        responses={
            200: openapi.Response(
                "Education updated successfully.", EducationSerializer
            ),
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Update an education entry for the logged-in user.",
        examples={
            "application/json": {
                "degree_type": "BSc",
                "discipline": "Computer Science",
                "institute_name": "University of Example",
                "from_date": "2020-01-01",
                "to_date": "2023-12-31"
            }
        },
    )
    def put(self, request):
        # Get the logged-in user's job_seeker_id
        job_seeker_id = request.user.id
        
        try:
            # Fetch the latest or specific education entry for the logged-in user
            education = Education.objects.filter(job_seeker_id=job_seeker_id).latest('created_at')
        except Education.DoesNotExist:
            return Response(
                {"status": "error", "message": "No education entry found for the logged-in user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Update the education entry with the new data
        serializer = EducationSerializer(education, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "message": "Education updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DeleteEducationView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: "Education deleted successfully.", 404: "Not Found"},
        operation_description="Delete the education entry for the logged-in user.",
    )
    def delete(self, request):
        # Get the logged-in user's job_seeker_id
        job_seeker_id = request.user.id

        try:
            # Fetch the latest or specific education entry for the logged-in user
            education = Education.objects.filter(job_seeker_id=job_seeker_id).latest('created_at')
        except Education.DoesNotExist:
            return Response(
                {"status": "error", "message": "No education entry found for the logged-in user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Delete the education entry
        education.delete()
        return Response(
            {"status": "success", "message": "Education deleted successfully"},
            status=status.HTTP_200_OK,
        )

