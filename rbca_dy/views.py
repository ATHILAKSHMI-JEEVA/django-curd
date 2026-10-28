
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import File
from .permission import has_permission,get_accessible_files,can_access_file

from .models import Role, UserRole, Permission, RolePermission


@api_view(["POST"])
def create_role(request):
    name = request.data.get("name")

    if not name:
        return Response({"error": "Role name required"}, status=400)

    role, created = Role.objects.get_or_create(name=name)

    return Response({
        "id": role.id,
        "name": role.name,
        "message": "Role created" if created else "Role already exists"
    })


@api_view(["POST"])
def create_permission(request):
    name = request.data.get("name")

    if not name:
        return Response({"error": "Permission name required"}, status=400)

    permission, created = Permission.objects.get_or_create(name=name)

    return Response({
        "id": permission.id,
        "name": permission.name,
        "message": "Permission created" if created else "Permission already exists"
    })


@api_view(["POST"])
def assign_permission(request):
    role_id = request.data.get("role_id")
    permission_ids = request.data.get("permission_ids", [])

    if not role_id:
        return Response({"error": "role_id required"}, status=400)

    if not  permission_ids:
        return Response({"error": "permission id required"}, status=400)

    role = get_object_or_404(Role, id=role_id)

    assigned = []

    for permission_id in permission_ids:
        permission = get_object_or_404(Permission, id=permission_id)

        RolePermission.objects.get_or_create(
            role=role,
            permission=permission
        )

        assigned.append(permission.name)

    return Response({
        "message": "Permissions assigned successfully",
        "role": role.name,
        "permissions": assigned
    })


@api_view(["POST"])
def create_user(request):
    name = request.data.get("name")
    username = request.data.get("username")
    password = request.data.get("password")

    if not name or not username or not password:
        return Response(
            {"error": "name, username and password required"},
            status=400
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"},
            status=400
        )

    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=name
    )

    return Response({
        "message": "User created successfully",
        "user_id": user.id,
        "username": user.username,
        "name": user.first_name
    }, status=201)



@api_view(["POST"])
def assign_role(request):
    user_id = request.data.get("user_id")
    role_id = request.data.get("role_id")
    team = request.data.get("team", "")

    if not user_id or not role_id:
        return Response(
            {"error": "user_id and role_id required"},
            status=400
        )

    user = get_object_or_404(User, id=user_id)
    role = get_object_or_404(Role, id=role_id)

    user_role, created = UserRole.objects.update_or_create(
        user=user,
        defaults={"role": role, "team": team}
    )

    return Response({
        "message": "Role assigned successfully",
        "user": user.username,
        "role": role.name,
        "team": user_role.team
    })

@api_view(["POST"])
def upload_file(request):
    user_id = request.data.get("user_id")
    name = request.data.get("name")
    uploaded_file = request.FILES.get("file")
    team = request.data.get("team", "")

    if not user_id or not name or not uploaded_file:
        return Response(
            {"error": "user_id, name and file required"},
            status=400
        )

    try:
        user_role = UserRole.objects.get(user_id=user_id)
    except UserRole.DoesNotExist:
        return Response(
            {"error": "User role not assigned"},
            status=404
        )

    allowed = (
        has_permission(user_role, "file.upload.all")
        or has_permission(user_role, "file.upload.own")
        or (
            team == user_role.team
            and has_permission(user_role, "file.upload.team")
        )
    )

    if not allowed:
        return Response(
            {"error": "You do not have permission to upload files"},
            status=403
        )

    file_obj = File.objects.create(
        name=name,
        file=uploaded_file,
        owner=user_role.user,
        team=team
    )

    return Response({
        "message": "File uploaded successfully",
        "file_id": file_obj.id,
        "name": file_obj.name,
        "owner": user_role.user.username,
        "team": file_obj.team
    }, status=201)

@api_view(["GET"])
def get_permissions(request):
    permissions = Permission.objects.all()

    data = []
    for permission in permissions:
        data.append({
            "id": permission.id,
            "name": permission.name
        })

    return Response(data)


@api_view(["GET"])
def view_files(request):
    user_id = request.query_params.get("user_id")

    if not user_id:
        return Response(
            {"error": "user_id is required"},
            status=400
        )

    user_role = get_object_or_404(UserRole, user_id=user_id)

    files = get_accessible_files(user_role, action="view")

    data = []

    for file_obj in files:
        data.append({
            "id": file_obj.id,
            "name": file_obj.name,
            "owner": file_obj.owner.username if file_obj.owner else None,
            "team": file_obj.team,
            "file_url": file_obj.file.url
        })

    return Response(data)

@api_view(["PUT"])
def update_file(request, file_id):
    user_id = request.data.get("user_id")

    if not user_id:
        return Response(
            {"error": "user_id is required"},
            status=400
        )

    user_role = get_object_or_404(
        UserRole,
        user_id=user_id
    )

    file_obj = get_object_or_404(File, id=file_id)

    if not can_access_file(user_role, file_obj, "update"):
        return Response(
            {"error": "You do not have permission to update this file"},
            status=403
        )

    name = request.data.get("name")

    if name:
        file_obj.name = name

    uploaded_file = request.FILES.get("file")

    if uploaded_file:
        file_obj.file = uploaded_file

    file_obj.save()

    return Response({
        "message": "File updated successfully",
        "id": file_obj.id,
        "name": file_obj.name
    })

@api_view(["DELETE"])
def delete_file(request, file_id):
    user_id = request.query_params.get("user_id")

    if not user_id:
        return Response(
            {"error": "user_id is required"},
            status=400
        )

    user_role = get_object_or_404(
        UserRole,
        user_id=user_id
    )

    file_obj = get_object_or_404(File, id=file_id)

    if not can_access_file(user_role, file_obj, "delete"):
        return Response(
            {"error": "You do not have permission to delete this file"},
            status=403
        )

    file_obj.delete()

    return Response({
        "message": "File deleted successfully"
    })