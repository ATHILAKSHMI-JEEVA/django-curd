from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Student




@api_view(["POST"])
def create_student(request):
    photo = request.FILES.get("photo")

    student =Student.objects.create(
        name=request.data.get("name"),
        age=request.data.get("age"),
        native=request.data.get("native"),
        photo=photo.read() if photo else None
    )
    return Response({
        "message": "Student created successfully",
        "id": student.id
        },     
     status=201)

@api_view(["GET"])
def get_student(request):
    students=Student.objects.all()
    data =[]
    for student in students:
        data.append({
            "id":student.id,
            "name":student.name,
            "age":student.age,
            "native":student.native,
            "photo":bool(student.photo)
        })
    return Response(data)


@api_view(["GET"])
def get_student_photo(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if not student.photo:
        return Response(
            {"message": "Photo not found"},
            status=404
        )

    return HttpResponse(
        bytes(student.photo),
        content_type="image/jpeg"
    )



from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Student


@api_view(["PUT"])
def update_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    student.name = request.data.get("name")
    student.age = request.data.get("age")
    student.native = request.data.get("native")

    photo = request.FILES.get("photo")

    if photo:
        student.photo = photo.read()

    student.save()

    return Response({
        "message": "Student updated successfully",
        "id": student.id,
        "name": student.name,
        "age": student.age,
        "native": student.native,
        "has_photo": bool(student.photo)
    })

@api_view(["DELETE"])
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    student.delete()

    return Response({
        "message": "Student deleted successfully"
    })
