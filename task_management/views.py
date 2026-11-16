from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.response import Response
from .models import TaskHistory
from django.core.paginator import Paginator
from .models import CustomUser,Task
from .utils import generate_token,verify_token

@api_view(["POST"])
def register_user(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not email or not password:
        return Response({
            "error": "all fields are required"
        }, status=400)

    if CustomUser.objects.filter(username=username).exists():
        return Response({
            "error": "username already exists"
        }, status=400)

    if CustomUser.objects.filter(email=email).exists():
        return Response({
            "error": "email already exists"
        }, status=400)

    user = CustomUser(
        username=username,
        email=email,
        role="client"
    )

    user.set_password(password)
    user.save()

    return Response({
        "message": "user register successfully",
        "username": user.username,
        "role": user.role,
    }, status=201)
@extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"}
            },
            "required": ["username", "password"]
        }
    },
    responses={
        200: {"description": "Login successful"},
        400: {"description": "Username and password required"},
        401: {"description": "Invalid username or password"},
        403: {"description": "Account inactive"}
    }
)

 

@api_view(["POST"])
def login_user(request):
    username=request.data.get("username")
    password=request.data.get("password")

    if not username or not password:
        return Response({
            "error":"username and password are required"
        },status=400)

    try:
        user=CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return Response({
            "error":"invalid username or password"
        },status=401)

    if not user.is_active:
        return Response({
            "error":"account id invalid"
        },status=403)
    if not user.check_password(password):
        return Response({
            "error":"invalid username or password"
        },status=401)
    
    token=generate_token(user)

    return Response({
        "message":"login successful",
        "token":token,
        "user_id":user.id,
        "username":user.username
    },status=200)

@api_view(["GET"])
def protected_api(request):
    token=request.headers.get("Authorization")

    if not token:
        return Response({
            "error":"token required"
        },status=401)
    
    token=token.replace("Bearer ", "")

    data=verify_token(token)

    if not data:
        return Response({
            "error":"invalid token"
        },status=401)
    
    return Response({
        "message":"login verified",
        "user_id":data["user_id"]
    })

@api_view(["POST"])
def create_admin(request):
    username=request.data.get("username")
    email=request.data.get("email")
    password=request.data.get("password")

    if not username or not email or not password:
        return Response({
            "error":"all field are required"
        },status=400)

    if CustomUser.objects.filter(username=username):
        return Response({
            "error":"username already exists"
        },status=400)
    if CustomUser.objects.filter(email=email):
        return Response({
            "error":"email already exists"
        },status=400)

    admin=CustomUser(
        username=username,
        email=email,
        role="admin"
    )
    admin.set_password(password)
    admin.save()

    return Response({
        "message":"admin created successfully",
        "username":admin.username,
        "role":admin.role
    },status=201)

@extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "email": {"type": "string"},
                "password": {"type": "string"}
            },
            "required": ["username", "email", "password"]
        }
    },
    responses={
        201: {"description": "Client created successfully"},
        400: {"description": "Required fields missing or duplicate username/email"},
        401: {"description": "Invalid token or user not found"},
        403: {"description": "Admin access required"}
    }
)


@api_view(["POST"])
def create_client(request):
    token=request.headers.get("Authorization")

    if not token:
        return Response({
            "error":"tokrn required"
        },status=400)

    token=token.replace("Bearer ", "",)
    data=verify_token(token)

    if not data:
        return Response({
            "error":"Invalid token"
        },status=401)

    try:
        admin=CustomUser.objects.get(id=data["user_id"])
    except CustomUser.DoesNotExist:
        return Response({
            "error":"User not found"
        },status=401)

    if admin.role != "admin":
        return Response({
            "error":"Admin access required"
        },status=403)
    username=request.data.get("username")
    email=request.data.get("email")
    password=request.data.get("password")

    if not username or not email or not password:
        return Response({
            "error":"required all details"
        },status=400)

    if CustomUser.objects.filter(username=username).exists():
        return Response({
            "error": "Username already exists"
        }, status=400)

    if CustomUser.objects.filter(email=email).exists():
        return Response({
            "error": "Email already exists"
        }, status=400)

    client = CustomUser(
        username=username,
        email=email,
        role="client"
    )

    client.set_password(password)
    client.save()

    return Response({
        "message": "Client created successfully",
        "client_id": client.id,
        "username": client.username,
        "role": client.role
    }, status=201)


@api_view(["POST"])
def create_task(request):
    title=request.data.get("title")
    discription=request.data.get("discription")
    assigned_to_id=request.data.get("assigned_to_id")
    token=request.headers.get("Authorization")

    if not token:
        return Response({
            "error":"token required"
        },status=400)
    token=token.replace("Bearer ","")
    data=verify_token(token)

    if not data:
        return Response({"error":"invalid token"},status=401)

    try:
        admin = CustomUser.objects.get(id=data["user_id"])
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=401)

    if admin.role != "admin":
        return Response({"error": "Admin access required"}, status=403)

    if not title or not discription or not assigned_to_id:
        return Response({"error": "All fields are required"}, status=400)

    try:
        client = CustomUser.objects.get(
            id=assigned_to_id,
            role="client"
        )
    except CustomUser.DoesNotExist:
        return Response({"error": "Client not found"}, status=404)

    task = Task.objects.create(
        title=title,
        discription=discription,
        assigned_to=client,
        created_by=admin
    )

    return Response({
        "message": "Task created successfully",
        "task_id": task.id,
        "title": task.title,
        "assigned_to": client.username,
        "status": task.status
    }, status=201)

@api_view(["GET"])
def get_all_task(request):
    token=request.headers.get("Authorization")

    if not token:
        return Response({
            "error":"token required"
        },status=400)

    token=token.replace("Bearer ", "")
    data=verify_token(token)

    if not data:
        return Response({
            "error":"invalid token"
        },status=401)
    try:
        admin=CustomUser.objects.get(id=data["user_id"])
    except CustomUser.DoesNotExist:
        return Response({
            "error":"user not found"
        },status=401)

    if admin.role != "admin":
        return Response({
            "error":"admin access required"
        },status=403)

    tasks=Task.objects.all().order_by("created_at")

    #task search
    search=request.query_params.get("search")
    if search:
        tasks=tasks.filter(title__icontains=search)

    status=request.query_params.get("status")
    if status:
        tasks=tasks.filter(status=status)

    paginator = Paginator(tasks, 5)

    page_number = request.query_params.get("page")

    page_obj = paginator.get_page(page_number)

    task_list = []

    for task in page_obj:
      task_list.append({
        "task_id": task.id,
        "title": task.title,
        "discription": task.discription,
        "assigned_to": task.assigned_to.username,
        "status": task.status,
        "created_at": task.created_at,
        "updated_at": task.updated_at
    })

    return Response({
    "total_tasks": paginator.count,
    "total_pages": paginator.num_pages,
    "current_page": page_obj.number,
    "tasks": task_list
})


@api_view(["PUT"])
def update_task(request,task_id):
    token =request.headers.get("Authorization")

    if not token:
        return Response({
            "error":"Token required"
        },status=400)

    token=token.replace("Bearer ","")
    data=verify_token(token)

    if not data:
        return Response({
            "error":"Invalid token"
        },status=401)

    try:
        admin=CustomUser.objects.get(id=data["user_id"])
    except CustomUser.DoesNotExist:
        return Response({
            "error":"user not found"
        },status=401)
    
    if admin.role != "admin":
        return Response({"error": "Admin access required"}, status=403)

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    title = request.data.get("title", task.title)
    discription = request.data.get("discription", task.discription)
    status_value = request.data.get("status", task.status)

    task.title = title
    task.discription = discription
    task.status = status_value
    task.save()

    return Response({
        "message": "Task updated successfully",
        "task_id": task.id,
        "title": task.title,
        "discription": task.discription,
        "status": task.status
    }, status=200)


@api_view(["DELETE"])
def delete_task(request,task_id):

    token=request.headers.get("Authorization")

    if not token:
        return Response({
            "error":"token required"
        },status=400)
    token=token.replace("Bearer ", "")
    data=verify_token(token)

    if not data:
        return Response({
            "error":"invalid token"
        },status=401)
    try:
        admin=CustomUser.objects.get(id=data["user_id"])
    except CustomUser.DoesNotExist:
        return Response({
            "error":"user not found"
        },status=401)

    if admin.role != "admin":
        return Response({
            "error":"admin acess required"
        },status=403)
    try:
        task=Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({
            "error":"task not found"
        },status=404)

    task.delete()

    return Response({
        "message": "Task deleted successfully",
        "task_id": task_id
    }, status=200)

@api_view(["PUT"])
def update_client(request,client_id):
    token=request.headers.get("Authorization")
    if not token:
        return Response({
            "error":"token required"
        },status=400)
    token=token.replace("Bearer ", "")
    data=verify_token(token)

    if not data:
        return Response({
            "error":"invalid token"
        },status=401)
    try:
        admin= CustomUser.objects.get(id=data["user_id"])
    except CustomUser.DoesNotExist:
        return Response({
            "error":"user not found"
        },status=401)
    if admin.role !="admin":
        return Response({
            "error":"adim acess required"
        },status=403)
    try:
        client=CustomUser.objects.get(
            id=client_id,
            role="client" 
        )
    except CustomUser.DoesNotExist:
        return Response({
            "error":"client not found"
        },status=404)
    username = request.data.get("username", client.username)
    email = request.data.get("email", client.email)
    password = request.data.get("password")

    if CustomUser.objects.filter(username=username).exclude(id=client.id).exists():
        return Response({
            "error": "username already exists"
        }, status=400)

    if CustomUser.objects.filter(email=email).exclude(id=client.id).exists():
        return Response({
            "error": "email already exists"
        }, status=400)

    client.username = username
    client.email = email

    if password:
        client.set_password(password)

    client.save()

    return Response({
        "message": "Client updated successfully",
        "client_id": client.id,
        "username": client.username,
        "email": client.email
    }, status=200)

@api_view(["DELETE"])
def delete_client(request,client_id):
    token=request.headers.get("Authorization")
    if not token:
        return Response({
            "error":"token required"
        },status=400)
    token=token.replace("Bearer ", "")
    data=verify_token(token)

    if not data:
        return Response({
            "error":"invalid token"
        },status=401)
    
    try:
        admin= CustomUser.objects.get(id=data["user_id"])
    except CustomUser.DoesNotExist:
        return Response({
            "error":"user not found"
        },status=401)
    
    if admin.role !="admin":
        return Response({
            "error":"adim acess required"
        },status=403)
    try:
        client=CustomUser.objects.get(
            id=client_id,
            role="client" 
        )
    except CustomUser.DoesNotExist:
        return Response({
            "error":"client not found"
        },status=404)

    client.delete()

    return Response({
        "message": "Client deleted successfully",
        "client_id": client_id
    }, status=200)

@api_view(["GET"])
def get_all_clients(request):
    token=request.headers.get("Authorization")
    if not token:
        return Response({
            "error":"token required"
        },status=400)
    token=token.replace("Bearer ", "")
    data=verify_token(token)

    if not data:
        return Response({
            "error":"invalid token"
        },status=401)
    
    try:
        admin= CustomUser.objects.get(id=data["user_id"])
    except CustomUser.DoesNotExist:
        return Response({
            "error":"user not found"
        },status=401)
    
    if admin.role !="admin":
        return Response({
            "error":"adim acess required"
        },status=403)

    clients = CustomUser.objects.filter(role="client").order_by("id")

    client_list = []

    for client in clients:
        client_list.append({
            "client_id": client.id,
            "username": client.username,
            "email": client.email
        })

    return Response({
        "total_clients": clients.count(),
        "clients": client_list
    }, status=200)

@api_view(["GET"])
def single_client(request,client_id):

    token=request.headers.get("Authorization")

    if not token:
        return Response({
            "error":"token required"
        },status=400)

    token=token.replace("Bearer ", "")
    data=verify_token(token)

    if not data:
        return Response({
            "error":"invalid token"
        },status=401)

    try:
        admin= CustomUser.objects.get(id=data["user_id"])
    except CustomUser.DoesNotExist:
        return Response({
            "error":"user not found"
        },status=401)

    if admin.role !="admin":
        return Response({
            "error":"adim acess required"
        },status=403)

    try:
        client=CustomUser.objects.get(
            id=client_id,
            role="client"
        )
    except CustomUser.DoesNotExist:
        return Response({
            "error":"client not found"
        },status=404)

    return Response({
        "client_id": client.id,
        "username": client.username,
        "email": client.email
    }, status=200)

@api_view(["GET"])
def admin_dashboard(request):
    token=request.headers.get("Authorization")
    if not token:
        return Response({
            "error":"token required"
        },status=400)
    token=token.replace("Bearer ", "")
    data=verify_token(token)
    if not data:
        return Response({
            "error":"invalid token"
        },status=401)
    try:
        admin= CustomUser.objects.get(id=data["user_id"])
    except CustomUser.DoesNotExist: 
        return Response({
            "error":"user not found"
        },status=401)   
    if admin.role !="admin":
        return Response({
            "error":"adim acess required"
        },status=403)   
    total_tasks=Task.objects.count()
    pending_tasks=Task.objects.filter(status="pending").count()
    completed_tasks=Task.objects.filter(status="completed").count()

    return Response({
        "total_tasks":total_tasks,
        "pending_tasks":pending_tasks,
        "completed_tasks":completed_tasks
    }, status=200)


@api_view(["GET"])
def client_task_list(request):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")
    data = verify_token(token)

    if not data:
        return Response({"error": "Invalid token"}, status=401)

    try:
        client = CustomUser.objects.get(id=data["user_id"])
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    if client.role != "client":
        return Response({"error": "Client access only"}, status=403)

    tasks = Task.objects.filter(assigned_to=client)

    task_list = []

    for task in tasks:
        task_list.append({
            "task_id": task.id,
            "title": task.title,
            "discription": task.discription,
            "status": task.status,
            "created_at": task.created_at,
            "updated_at": task.updated_at
        })

    return Response({
        "total_tasks": len(task_list),
        "tasks": task_list
    })

@api_view(["PUT"])
def update_task_status(request, task_id):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")
    data = verify_token(token)

    if not data:
        return Response({"error": "Invalid token"}, status=401)

    try:
        client = CustomUser.objects.get(id=data["user_id"])
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    if client.role != "client":
        return Response({"error": "Client access only"}, status=403)

    try:
        task = Task.objects.get(id=task_id, assigned_to=client)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    status = request.data.get("status")

    if status not in ["pending", "in_progress", "completed"]:
        return Response({"error": "Invalid task status"}, status=400)
    old_status = task.status
    
    task.status = status
    task.save()

    # Create a new entry in TaskHistory
    TaskHistory.objects.create(
        task=task,
        old_status=old_status,
        new_status=status,
        changed_by=client
    )

    return Response({
        "message": "Task status updated successfully",
        "task_id": task.id,
        "old_status": old_status,
        "new_status": task.status
    }, status=200)

@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def upload_completion_proof(request, task_id):

    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token required"}, status=401)

    token = token.replace("Bearer ", "")
    data = verify_token(token)

    if not data:
        return Response({"error": "Invalid token"}, status=401)

    try:
        client = CustomUser.objects.get(
            id=data["user_id"],
            role="client"
        )
    except CustomUser.DoesNotExist:
        return Response({"error": "Client not found"}, status=404)

    try:
        task = Task.objects.get(
            id=task_id,
            assigned_to=client
        )
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    proof = request.FILES.get("completion_proof")

    if not proof:
        return Response({"error": "Please upload a file"}, status=400)

    allowed_types = [
        "image/jpeg",
        "image/png",
        "application/pdf"
    ]

    if proof.content_type not in allowed_types:
        return Response({
            "error": "Only JPG, PNG and PDF files are allowed"
        }, status=400)

    task.completion_proof = proof
    task.save()

    return Response({
        "message": "Proof uploaded successfully",
        "proof_url": task.completion_proof.url
    }, status=200)

@api_view(["GET"])
def client_task_history(request, task_id):

    
    token = request.headers.get("Authorization")

    if not token:
        return Response(
            {"error": "Token required"},
            status=401
        )

    
    token = token.replace("Bearer ", "")

   
    data = verify_token(token)

    if not data:
        return Response(
            {"error": "Invalid token"},
            status=401
        )

    
    try:
        client = CustomUser.objects.get(
            id=data["user_id"]
        )
    except CustomUser.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=404
        )

    
    if client.role != "client":
        return Response(
            {"error": "Client access only"},
            status=403
        )

    
    try:
        task = Task.objects.get(
            id=task_id,
            assigned_to=client
        )
    except Task.DoesNotExist:
        return Response(
            {"error": "Task not found"},
            status=404
        )

    histories = TaskHistory.objects.filter(
        task=task
    ).order_by("-changed_at")

    history_data = []

    for history in histories:
        history_data.append({
            "old_status": history.old_status,
            "new_status": history.new_status,
            "changed_at": history.changed_at,
            "changed_by": history.changed_by.username
        })

    return Response({
        "task_id": task.id,
        "task_title": task.title,
        "history": history_data
    }, status=200)   

@api_view(["GET"])
def client_dashboard(request):

    
    token = request.headers.get("Authorization")

    if not token:
        return Response(
            {"error": "Token required"},
            status=401
        )

    
    token = token.replace("Bearer ", "")

    
    data = verify_token(token)

    if not data:
        return Response(
            {"error": "Invalid token"},
            status=401
        )

    
    try:
        client = CustomUser.objects.get(
            id=data["user_id"]
        )
    except CustomUser.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=404
        )

    
    if client.role != "client":
        return Response(
            {"error": "Client access only"},
            status=403
        )

    tasks = Task.objects.filter(
        assigned_to=client
    )


    total_tasks = tasks.count()

    pending_tasks = tasks.filter(
        status="pending"
    ).count()

    in_progress_tasks = tasks.filter(
        status="in_progress"
    ).count()

    completed_tasks = tasks.filter(
        status="completed"
    ).count()

    
    return Response({
        "client": client.username,
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "in_progress_tasks": in_progress_tasks,
        "completed_tasks": completed_tasks
    }, status=200)