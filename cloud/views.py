from .models import Cloudstorage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

@api_view(["POST"])
def create_cloud(request):
    photo= request.FILES.get("photo")

    cloud=Cloudstorage.objects.create(
        name=request.data.get("name"),
        age=request.data.get("age"),
        native=request.data.get("native"),
        photo=photo
    )
    return Response(
        {
            "message":"cloud created",
            "id":cloud.id,
            "photo_url":cloud.photo.url if cloud.photo else None
        }, status=status.HTTP_201_CREATED
    )

@api_view(["GET"])
def get_cloud(request):
    cloud=Cloudstorage.objects.all().order_by("id")
    data=[]

    for clouds in cloud:
        data.append({
            "id":clouds.id,
            "name":clouds.name,
            "age":clouds.age,
            "native":clouds.native,
            "photo_url":clouds.photo.url if clouds.photo else None

        })
    return Response(data,status=status.HTTP_200_OK)


@api_view(["GET"])
def get_obcloud(request,cloud_id):
    cloud = get_object_or_404(Cloudstorage, id=cloud_id)

    data = {
        "id": cloud.id,
        "name": cloud.name,
        "age": cloud.age,
        "native": cloud.native,
        "photo_url": cloud.photo.url if cloud.photo else None
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(["PUT"])
def put_cloud(request,cloud_id):
    cloud = get_object_or_404(Cloudstorage,id=cloud_id)

    cloud.name = request.data.get("name", cloud.name)
    cloud.age = request.data.get("age", cloud.age)
    cloud.native = request.data.get("native", cloud.native)

    photo = request.FILES.get("photo")
    if photo:
        cloud.photo = photo

    cloud.save()
    return Response({
        "message": "Cloud record updated successfully",
        "id": cloud.id,
        "name": cloud.name,
        "age": cloud.age,
        "native": cloud.native,
        "photo_url": cloud.photo.url if cloud.photo else None
    }, status=status.HTTP_200_OK)

@api_view(["DELETE"])
def delete_cloud(request,cloud_id):
    cloud=get_object_or_404(Cloudstorage,id=cloud_id)

    cloud.delete()

    return Response({
        "message":"deleted"
    },status=status.HTTP_200_OK)