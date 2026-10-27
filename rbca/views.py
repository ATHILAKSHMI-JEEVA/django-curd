
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import IsAdmin, IsManager, IsEmployee
from .models import File, TeamMember
from django.http import FileResponse
from django.shortcuts import get_object_or_404

@api_view(["GET"])
@permission_classes([IsAdmin])
def test_permission(request):
    return Response({
        "message":"permission allowed",
        "username":request.user.username,
        "role":request.user.userrole.role.name

    })

@api_view(["GET"])
@permission_classes([IsManager])
def manager_test(request):
    return Response({
        "message": "Manager access allowed!",
        "username": request.user.username,
        "role": request.user.userrole.role.name
    })

@api_view(["GET"])
@permission_classes([IsEmployee])
def employee_test(request):
    return Response({
        "message": "Employee access allowed!",
        "username": request.user.username,
        "role": request.user.userrole.role.name
    })

@api_view(["POST"])
@permission_classes([IsEmployee | IsAdmin | IsManager])
def upload_file(request):
    uploaded_file = request.FILES.get("file")

    if not uploaded_file:
        return Response(
            {"error": "Please upload a file"},
            status=400
        )

    new_file = File.objects.create(
        uploaded_by=request.user,
        name=uploaded_file.name,
        file=uploaded_file
    )

    return Response({
        "message": "File uploaded successfully",
        "id": new_file.id,
        "name": new_file.name
    }, status=201)


@api_view(["GET"])
@permission_classes([IsEmployee])
def get_my_files(request):
    files = File.objects.filter(uploaded_by=request.user)

    data = []

    for item in files:
        data.append({
            "id": item.id,
            "name": item.name,
            "file": item.file.url if item.file else None,
            "created_at": item.created_at
        })

    return Response(data)



@api_view(["GET"])
@permission_classes([IsAdmin])
def get_all_files(request):
    files = File.objects.all()

    data = []

    for item in files:
        data.append({
            "id": item.id,
            "name": item.name,
            "uploaded_by": item.uploaded_by.username,
            "file": item.file.url if item.file else None,
            "created_at": item.created_at
        })

    return Response(data)


@api_view(["GET"])
@permission_classes([IsManager])
def manager_files(request):
    team_employee_ids = TeamMember.objects.filter(
        manager=request.user
    ).values_list("employee_id", flat=True)

    files = File.objects.filter(
        uploaded_by__in=team_employee_ids
    ) | File.objects.filter(uploaded_by=request.user)

    data = []

    for item in files.distinct():
        data.append({
            "id": item.id,
            "name": item.name,
            "uploaded_by": item.uploaded_by.username,
            "file": item.file.url if item.file else None
        })

    return Response(data)




@api_view(["DELETE"])
@permission_classes([IsEmployee])
def delete_my_file(request, file_id):
    file_obj = get_object_or_404(File,id=file_id,uploaded_by=request.user)

    file_obj.delete()

    return Response({
        "message": "File deleted successfully"
    })


@api_view(["DELETE"])
@permission_classes([IsAdmin])
def admin_delete_file(request, file_id):
    file_obj = get_object_or_404(File,id=file_id)

    file_obj.delete()

    return Response({
        "message": "File deleted successfully by Admin"
    })

@api_view(["DELETE"])
@permission_classes([IsManager])
def manager_delete_file(request, file_id):
    team_employee_ids = TeamMember.objects.filter(manager=request.user).values_list("employee_id", flat=True)

    file_obj = get_object_or_404(File,id=file_id,uploaded_by__in=team_employee_ids)

    file_obj.delete()

    return Response({
        "message": "Team member file deleted successfully by Manager"
    })


@api_view(["GET"])
@permission_classes([IsAdmin])
def admin_download_file(request, file_id):
    file_obj = get_object_or_404(File, id=file_id)

    response = FileResponse(
        file_obj.file.open("rb"),
        as_attachment=True,
        filename=file_obj.name
    )

    return response