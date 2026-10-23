
import base64

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Employee


@api_view(["POST"])
def employee_create(request):
    photo=request.FILES.get("photo")


    photo_baseme = None

    if photo:
        photo_baseme  = base64.b64encode(
            photo.read()
        ).decode("utf-8")


    employee = Employee.objects.create(
        name=request.data.get("name"),
        age=request.data.get("age"),
        native=request.data.get("native"),
        photo=photo_baseme
    )

    return Response({
        "message": "Base64 student created successfully",
        "id": employee.id,
        "has_photo": bool(employee.photo)
    }, status=201)


@api_view(["GET"])
def employee_get(request):
    employees = Employee.objects.all().order_by("id")

    data = []

    for employee in employees:
        data.append({
            "id": employee.id,
            "name": employee.name,
            "age": employee.age,
            "native": employee.native,
            "has_photo": bool(employee.photo)
        })

    return Response(data)


@api_view(["GET"])
def employee_photo(request, employee_id):
    employee = get_object_or_404(
        Employee,
        id=employee_id
    )

    if not employee.photo:
        return Response(
            {"message": "Photo not found"},
            status=404
        )

    image= base64.b64decode(employee.photo)

    return HttpResponse(image,content_type="image/jpeg")



@api_view(["PUT"])
def employee_update(request, employee_id):
    employee = get_object_or_404(
        Employee,
        id=employee_id
    )

    name = request.data.get("name")
    age = request.data.get("age")
    native = request.data.get("native")

    if name is None :
        return Response({
            "message": "Name are required"
        }, status=400)
    if age is None :
        return Response({
            "message":"age is required"
        },status=404)

    employee.name = name
    employee.age = age
    employee.native = native

    photo = request.FILES.get("photo")

    if photo:
        employee.photo = base64.b64encode(
            photo.read()
        ).decode("utf-8")

    employee.save()

    return Response({
        "message": "Employee updated successfully",
        "id": employee.id,
        "name": employee.name,
        "age": employee.age,
        "native": employee.native,
        "has_photo": bool(employee.photo)
    })


@api_view(["DELETE"])
def employee_delete(request, employee_id):
    employee = get_object_or_404(Employee,id=employee_id)

    employee.delete()

    return Response({
        "message": "Employee deleted successfully"
    })
