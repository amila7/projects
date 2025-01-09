from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from  drfapp.serializers import StudentSerializer  # Fixed typo in serializer name
from drfapp.serializers import StudentSerializer


class StudentView(APIView):  # More descriptive class name
    permission_classes = [IsAuthenticated]  # Add authentication requirement
    
    def get(self, request, pk=None, *args, **kwargs):
        """
        Retrieve a student or list of students.
        If pk is provided, return specific student, otherwise return all students.
        """
        if pk:
            student = get_object_or_404(Student, pk=pk)
            serializer = StudentSerializer(student)
        else:
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """Create a new student."""
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Student created successfully',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)