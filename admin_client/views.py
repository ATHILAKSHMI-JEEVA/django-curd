from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.core.paginator import Paginator
from .models import Role,Permision,RolePermision,CustomUser, TaskHistory,TaskStatus,Task
from .utils import  generate_tokens,verify_token,get_user_from_token,generate_access_token,has_permission

@api_view(["POST"])
def create_role(request):
    name = request.data.get("name")

    if not name:
        return Response({"error": "Role name required"}, status=400)

    role, created = Role.objects.get_or_create(role_name=name)

    return Response({
        "id": role.id,
        "name": role.role_name,
        "message": "Role created" if created else "Role already exists"
    })

@api_view(["POST"])
def create_permision(request):
    name=request.data.get("name")
    if not name:
        return Response({
            "error":"permision name required"
        },status=400)
    permision,created=Permision.objects.get_or_create(permision_name=name)
    return Response({
        "id":permision.id,
        "name":permision.permision_name,
        "message":"permision created" if created else "permission already exists"
    })

@api_view(["POST"])
def assign_permision(request):
    role_id=request.data.get("role_id")
    permision_id=request.data.get("permision_id")

    if not role_id or not permision_id:
        return Response({
            "error":"role id and permision id required"
        },status=400)
    try:
        role = Role.objects.get(id=role_id)
    except Role.DoesNotExist:
        return Response(
            {"error": "Role not found"},
            status=404
        )

    try:
        permision = Permision.objects.get(id=permision_id)
    except Permision.DoesNotExist:
        return Response(
            {"error": "Permission not found"},
            status=404
        )

    assign,created=RolePermision.objects.get_or_create(role=role,permision=permision)
    return Response({
        "id":assign.id,
        "role":assign.role.role_name,
        "permision":assign.permision.permision_name,
        "message":"permision assigned" if created else "permision already assigned",
    })

@api_view(["GET"])
def get_role_permision(request,role_id):
    try:
        role=Role.objects.get(id=role_id)
    except Role.DoesNotExist:
        return Response({
            "error":"role not found"
        },status=404)
    permisions=RolePermision.objects.filter(role=role)
    data=[]
    for permision in permisions:
        data.append({
            "id":permision.id,
            "permision_name":permision.permision.permision_name
        })
    return Response({
        "role_id":role.id,
        "role_name":role.role_name,
        "permisions":data
    })

@api_view(["POST"])
def register_admin(request):

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    role_id = request.data.get("role_id")

    if not username or not email or not password or not role_id:
        return Response({"error": "All fields required"}, status=400)

    if CustomUser.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    if CustomUser.objects.filter(email=email).exists():
        return Response({"error": "Email already exists"}, status=400)

    try:
        role = Role.objects.get(id=role_id)
    except Role.DoesNotExist:
        return Response({"error": "Role not found"}, status=404)

    admin = CustomUser(
        username=username,
        email=email,
        role=role,
        is_active=True
    )

    admin.set_password(password)
    admin.save()

    return Response({
        "message": "Admin created successfully",
        "id": admin.id,
        "username": admin.username,
        "email": admin.email,
        "role": admin.role.role_name
    }, status=201)

@api_view(["POST"])
def login_user(request):

    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"error": "Username and password required"},
            status=400
        )

    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return Response(
            {"error": "Invalid username or password"},
            status=401
        )

    if not user.is_active:
        return Response(
            {"error": "Account is inactive"},
            status=403
        )

    if not user.check_password(password):
        return Response(
            {"error": "Invalid username or password"},
            status=401
        )

    tokens = generate_tokens(user)

    return Response({
        "message": "Login successful",
        "user_id": user.id,
        "username": user.username,
        "role": user.role.role_name,
        "access_token": tokens["access"],
        "refresh_token": tokens["refresh"]
    }, status=200)


@api_view(["POST"])
def refresh_access_token(request):

    refresh_token = request.data.get("refresh_token")

    if not refresh_token:
        return Response(
            {"error": "Refresh token required"},
            status=400
        )

    payload = verify_token(refresh_token, "refresh")

    if not payload:
        return Response(
            {"error": "Invalid or expired refresh token"},
            status=401
        )

    try:
        user = CustomUser.objects.get(
            id=payload["user_id"],
            is_active=True
        )
    except (CustomUser.DoesNotExist, KeyError):
        return Response(
            {"error": "User not found or inactive"},
            status=401
        )

    new_access_token = generate_access_token(user.id)

    return Response({
        "message": "New access token generated",
        "access_token": new_access_token
    }, status=200)

@api_view(["POST"])
def create_client(request):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")

    admin = get_user_from_token(token)

    if not admin:
        return Response({"error": "Invalid token"}, status=401)

    if not has_permission(admin, "create_client"):
        return Response({"error": "Permission denied"}, status=403)

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not email or not password:
        return Response({"error": "All fields required"}, status=400)

    if CustomUser.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    if CustomUser.objects.filter(email=email).exists():
        return Response({"error": "Email already exists"}, status=400)

    role_id = request.data.get("role_id")

    if not role_id:
        return Response({"error": "Role ID required"}, status=400)


    try:
        user_role = Role.objects.get(id=role_id)
    except Role.DoesNotExist:
       return Response({"error": "Role not found"}, status=404)

    if user_role.role_name == "admin":
        return Response({
        "error": "Cannot create another Admin user"
    }, status=403)

    new_user = CustomUser(
    username=username,
    email=email,
    role=user_role,
    is_active=True
)

    new_user.set_password(password)
    new_user.save()

    return Response({
        "message": "Client created successfully",
        "client_id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }, status=201)

@api_view(["GET"])
def view_clients(request):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")

    current_user = get_user_from_token(token)

    if not current_user:
        return Response({"error": "Invalid token"}, status=401)

    if not has_permission(current_user, "view_client"):
        return Response({"error": "Permission denied"}, status=403)

    role_id = request.query_params.get("role_id")

    if not role_id:
        return Response({"error": "Role ID required"}, status=400)

    try:
        role = Role.objects.get(id=role_id)
    except Role.DoesNotExist:
        return Response({"error": "Role not found"}, status=404)

    users = CustomUser.objects.filter(role=role)

    data = []

    for user in users:
        data.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.role_name,
            "is_active": user.is_active
        })

    return Response({
        "message": "Users retrieved successfully",
        "users": data
    }, status=200)

@api_view(["PUT"])
def update_client(request, user_id):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")

    current_user = get_user_from_token(token)

    if not current_user:
        return Response({"error": "Invalid token"}, status=401)

    if not has_permission(current_user, "update_client"):
        return Response({"error": "Permission denied"}, status=403)

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    if current_user.id != user.id:
        return Response({"error": "update only your own details"}, status=403)


    if not has_permission(user,"client_account"):
        return Response({
            "error":"client account only updated"
        },status=403)

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    
    if username:
        user.username = username

    if email:
        user.email = email

    if password:
        user.set_password(password)


    user.save()

    return Response({
        "message": "User updated successfully",
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role.role_name
    }, status=200)

@api_view(["DELETE"])
def delete_client(request, user_id):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")

    current_user = get_user_from_token(token)

    if not current_user:
        return Response({"error": "Invalid token"}, status=401)
    

    if not has_permission(current_user, "delete_client"):
        return Response({"error": "Permission denied"}, status=403)

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    if current_user.id != user.id:
        if not has_permission(current_user, "delete_client"):
           return Response({
            "error": "cannot delete another client details"
        }, status=403)

    if not has_permission(user, "client_account"):
        return Response({
         "error": "client account only deleted"
    }, status=403)

    user.delete()

    return Response({
        "message": "User deleted successfully"
    }, status=200)



@api_view(["POST"])
def create_status(request):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")

    current_user = get_user_from_token(token)

    if not current_user:
        return Response({"error": "Invalid token"}, status=401)

    if not has_permission(current_user, "create_status"):
        return Response({"error": "Permission denied"}, status=403)

    status_name = request.data.get("status_name")

    if not status_name:
        return Response(
            {"error": "Status name required"},
            status=400
        )

    if TaskStatus.objects.filter(status_name=status_name).exists():
        return Response(
            {"error": "Status already exists"},
            status=400
        )

    status = TaskStatus.objects.create(
        status_name=status_name
    )

    return Response({
        "message": "Status created successfully",
        "status_id": status.id,
        "status_name": status.status_name
    }, status=201)


@api_view(["POST"])
def create_task(request):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")

    current_user = get_user_from_token(token)

    if not current_user:
        return Response({"error": "Invalid token"}, status=401)

    if not has_permission(current_user, "create_task"):
        return Response({"error": "Permission denied"}, status=403)

    title = request.data.get("title")
    description = request.data.get("description")
    assigned_to_id = request.data.get("assigned_to_id")
    status_id = request.data.get("status_id")

    if not title or not description or not assigned_to_id or not status_id:
        return Response({"error": "All fields required"}, status=400)

    try:
        assigned_user = CustomUser.objects.get(id=assigned_to_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "Assigned user not found"}, status=404)

    try:
        task_status = TaskStatus.objects.get(id=status_id)
    except TaskStatus.DoesNotExist:
        return Response({"error": "Task status not found"}, status=404)

    task = Task.objects.create(
        title=title,
        description=description,
        assigned_to=assigned_user,
        status=task_status
    )


    return Response({
        "message": "Task created successfully",
        "task_id": task.id,
        "title": task.title,
        "description": task.description,
        "assigned_to": task.assigned_to.username,
        "status": task.status.status_name
    }, status=201)

@api_view(["GET"])
def view_tasks(request):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")

    current_user = get_user_from_token(token)

    if not current_user:
        return Response({"error": "Invalid token"}, status=401)

    if not has_permission(current_user, "view_task"):
        return Response({"error": "Permission denied"}, status=403)

    tasks = Task.objects.all()

    if current_user.role.role_name.lower() != "admin":
       tasks = Task.objects.filter(assigned_to=current_user)

    data = []

    for task in tasks:
        data.append({
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "assigned_to": task.assigned_to.username,
            "status": task.status.status_name,
            "created_at": task.created_at,
            "updated_at": task.updated_at
        })

    return Response({
        "message": "Tasks retrieved successfully",
        "tasks": data
    }, status=200)


@api_view(["PUT"])
def update_task(request, task_id):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")

    current_user = get_user_from_token(token)

    if not current_user:
        return Response({"error": "Invalid token"}, status=401)

    if not has_permission(current_user, "update_task"):
        return Response({"error": "Permission denied"}, status=403)

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    title = request.data.get("title")
    description = request.data.get("description")
    assigned_to_id = request.data.get("assigned_to_id")
    status_id = request.data.get("status_id")

    if title:
        task.title = title

    if description:
        task.description = description

    if assigned_to_id:
        try:
            assigned_user = CustomUser.objects.get(id=assigned_to_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        task.assigned_to = assigned_user

    if status_id:
        try:
            task_status = TaskStatus.objects.get(id=status_id)
        except TaskStatus.DoesNotExist:
            return Response({"error": "Status not found"}, status=404)

        old_status = task.status

        if old_status.id != task_status.id:

            task.status = task_status

            TaskHistory.objects.create(
                task=task,
                old_status=old_status,
                new_status=task_status,
                changed_by=current_user
            )

    task.save()

    return Response({
        "message": "Task updated successfully",
        "task_id": task.id,
        "title": task.title,
        "description": task.description,
        "assigned_to": task.assigned_to.username,
        "status": task.status.status_name
    }, status=200)


@api_view(["DELETE"])
def delete_task(request, task_id):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")

    current_user = get_user_from_token(token)

    if not current_user:
        return Response({"error": "Invalid token"}, status=401)

    if not has_permission(current_user, "delete_task"):
        return Response({"error": "Permission denied"}, status=403)

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    task.delete()

    return Response({
        "message": "Task deleted successfully"
    }, status=200)

@api_view(["GET"])
def client_view_tasks(request):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")

    current_user = get_user_from_token(token)

    if not current_user:
        return Response({"error": "Invalid token"}, status=401)

    if not has_permission(current_user, "view_task"):
        return Response({"error": "Permission denied"}, status=403)

    tasks = Task.objects.filter(assigned_to=current_user)

    data = []

    for task in tasks:
        data.append({
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status.status_name,
            "created_at": task.created_at,
            "updated_at": task.updated_at
        })

    return Response({
        "message": "Your tasks retrieved successfully",
        "tasks": data
    }, status=200)

@api_view(["PUT"])
def client_update_task_status(request, task_id):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")

    current_user = get_user_from_token(token)

    if not current_user:
        return Response({"error": "Invalid token"}, status=401)

    if not has_permission(current_user, "update_task_status"):
        return Response({"error": "Permission denied"}, status=403)

    try:
        task = Task.objects.get(
            id=task_id,
            assigned_to=current_user
        )
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    status_id = request.data.get("status_id")

    if not status_id:
        return Response({"error": "Status ID required"}, status=400)

    try:
        new_status = TaskStatus.objects.get(id=status_id)
    except TaskStatus.DoesNotExist:
        return Response({"error": "Status not found"}, status=404)

    old_status = task.status
 
    task.status = new_status
    task.save()

    if old_status.id == new_status.id:
        return Response({
           "message": "Task already has this status"
        }, status=400)

    TaskHistory.objects.create(
      task=task,
      old_status=old_status,
      new_status=new_status,
      changed_by=current_user
    )

    return Response({
        "message": "Task status updated successfully",
        "task_id": task.id,
        "old_status": old_status.status_name,
        "new_status": new_status.status_name
    }, status=200)

@api_view(["GET"])
def view_task_history(request, task_id):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")

    current_user = get_user_from_token(token)

    if not current_user:
        return Response({"error": "Invalid token"}, status=401)

    if not has_permission(current_user, "view_task_history"):
        return Response({"error": "Permission denied"}, status=403)

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    if task.assigned_to != current_user:
        if not has_permission(current_user, "view_all_task_history"):
            return Response({"error": "Permission denied"}, status=403)

    histories = TaskHistory.objects.filter(task=task).order_by("-changed_at")

    data = []

    for history in histories:
        data.append({
            "old_status": history.old_status.status_name,
            "new_status": history.new_status.status_name,
            "changed_by": history.changed_by.username,
            "changed_at": history.changed_at
        })

    return Response({
        "message": "Task history retrieved successfully",
        "task_id": task.id,
        "history": data
    }, status=200)

@api_view(["GET"])
def client_dashboard(request):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")

    current_user = get_user_from_token(token)

    if not current_user:
        return Response({"error": "Invalid token"}, status=401)

    if not has_permission(current_user, "view_dashboard"):
        return Response({"error": "Permission denied"}, status=403)

    tasks = Task.objects.filter(assigned_to=current_user)

    total_tasks = tasks.count()

    status_summary = {}

    statuses = TaskStatus.objects.all()

    for status in statuses:
        count = tasks.filter(status=status).count()

        status_summary[status.status_name] = count

    return Response({
        "message": "Dashboard retrieved successfully",
        "total_tasks": total_tasks,
        "status_summary": status_summary
    }, status=200)

@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def upload_task_proof(request, task_id):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")

    current_user = get_user_from_token(token)

    if not current_user:
        return Response({"error": "Invalid token"}, status=401)

    if not has_permission(current_user, "upload_task_proof"):
        return Response({"error": "Permission denied"}, status=403)

    try:
        task = Task.objects.get(
            id=task_id,
            assigned_to=current_user
        )
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    proof = request.FILES.get("completion_proof")

    if not proof:
        return Response({"error": "Proof file required"}, status=400)

    task.completion_proof = proof
    task.save()

    return Response({
        "message": "Proof uploaded successfully",
        "task_id": task.id,
        "completion_proof": task.completion_proof.url
    }, status=200)

@api_view(["GET"])
def search_tasks(request):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")
    current_user = get_user_from_token(token)

    if not current_user:
        return Response({"error": "Invalid token"}, status=401)

    if not has_permission(current_user, "view_task"):
        return Response({"error": "Permission denied"}, status=403)

    search = request.query_params.get("search")

    tasks = Task.objects.filter(title=search)
    if current_user.role.role_name.lower() != "admin":
       tasks = tasks.filter(assigned_to=current_user)

    data = []

    for task in tasks:
        data.append({
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "assigned_to": task.assigned_to.username,
            "status": task.status.status_name
        })

    return Response({
        "message": "Tasks retrieved successfully",
        "tasks": data
    }, status=200)

@api_view(["GET"])
def filter_tasks(request):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")
    current_user = get_user_from_token(token)

    if not current_user:
        return Response({"error": "Invalid token"}, status=401)

    if not has_permission(current_user, "view_task"):
        return Response({"error": "Permission denied"}, status=403)

    status_id = request.query_params.get("status_id")

    tasks = Task.objects.filter(status_id=status_id)

    data = []

    for task in tasks:
        data.append({
            "task_id": task.id,
            "title": task.title,
            "status": task.status.status_name,
            "assigned_to": task.assigned_to.username
        })

    return Response({
        "message": "Tasks filtered successfully",
        "tasks": data
    }, status=200)

@api_view(["GET"])
def pagination_tasks(request):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")
    current_user = get_user_from_token(token)

    if not current_user:
        return Response({"error": "Invalid token"}, status=401)

    if not has_permission(current_user, "view_task"):
        return Response({"error": "Permission denied"}, status=403)

    tasks = Task.objects.all()

    page_number = request.query_params.get("page", 1)

    paginator = Paginator(tasks, 5)

    page = paginator.get_page(page_number)

    data = []

    for task in page:
        data.append({
            "task_id": task.id,
            "title": task.title,
            "status": task.status.status_name,
            "assigned_to": task.assigned_to.username
        })

    return Response({
        "total_tasks": paginator.count,
        "total_pages": paginator.num_pages,
        "current_page": page.number,
        "tasks": data
    }, status=200)

@api_view(["GET"])
def admin_dashboard(request):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")

    current_user = get_user_from_token(token)

    if not current_user:
        return Response({"error": "Invalid token"}, status=401)

    if not has_permission(current_user, "view_dashboard"):
        return Response({"error": "Permission denied"}, status=403)

    total_tasks = Task.objects.count()

    pending_status = TaskStatus.objects.get(status_name="Pending")
    completed_status = TaskStatus.objects.get(status_name="Completed")

    pending_tasks = Task.objects.filter(status=pending_status).count()
    completed_tasks = Task.objects.filter(status=completed_status).count()

    return Response({
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks
    }, status=200)


@api_view(["PUT"])
def update_admin(request, user_id):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")

    current_user = get_user_from_token(token)

    if not current_user:
        return Response({"error": "Invalid token"}, status=401)

    
    if not has_permission(current_user, "update_admin"):
        return Response({"error": "Permission denied"}, status=403)

    
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

  
    if not has_permission(user, "admin_account"):
        return Response({
            "error": "Only admin accounts can be updated here"
        }, status=403)

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if username:
        user.username = username

    if email:
        user.email = email

    if password:
        user.set_password(password)

    user.save()

    return Response({
        "message": "Admin updated successfully",
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role.role_name
    }, status=200)


@api_view(["DELETE"])
def delete_admin(request, user_id):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")

    current_user = get_user_from_token(token)

    if not current_user:
        return Response({"error": "Invalid token"}, status=401)

    
    if not has_permission(current_user, "delete_admin"):
        return Response({"error": "Permission denied"}, status=403)

   
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

   
    if not has_permission(user, "admin_account"):
        return Response({
            "error": "Only admin accounts can be deleted here"
        }, status=403)

    user.delete()

    return Response({
        "message": "Admin deleted successfully"
    }, status=200)
