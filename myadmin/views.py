

from rest_framework.decorators import api_view
from rest_framework.response import Response        
from rest_framework import status

from myadmin.models import Admin
from myadmin.serializers import Adminserializer

@api_view(["GET", "POST"])
def admin_list(request):

    if request.method == "GET":
        admins = Admin.objects.all()
        serializer = Adminserializer(admins, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = Adminserializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



@api_view(["PUT", "DELETE"])
def admin_detail(request, id):

    try:
        admin = Admin.objects.get(id=id)
    except Admin.DoesNotExist:
        return Response(
            {"error": "Admin not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "PUT":
        serializer = Adminserializer(admin, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    if request.method == "DELETE":
        admin.delete()
        return Response(
            {"message": "Admin deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
