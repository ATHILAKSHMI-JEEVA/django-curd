
from .models import RolePermission, File


def has_permission(user_role, permission_name):
    return RolePermission.objects.filter(
        role=user_role.role,
        permission__name=permission_name
    ).exists()


def can_access_file(user_role, file_obj, action):
    user = user_role.user

    # Admin
    if has_permission(user_role, f"file.{action}.all"):
        return True

    # Own files
    if (
        file_obj.owner_id == user.id
        and has_permission(user_role, f"file.{action}.own")
    ):
        return True

    # Team files
    if (
        user_role.team
        and file_obj.team == user_role.team
        and has_permission(user_role, f"file.{action}.team")
    ):
        return True

    return False


def get_accessible_files(user_role, action="view"):
    user = user_role.user

    # All files
    if has_permission(user_role, f"file.{action}.all"):
        return File.objects.all()

    # Own files
    own_files = File.objects.none()
    if has_permission(user_role, f"file.{action}.own"):
        own_files = File.objects.filter(owner=user)

    # Team files
    team_files = File.objects.none()
    if (
        user_role.team
        and has_permission(user_role, f"file.{action}.team")
    ):
        team_files = File.objects.filter(team=user_role.team)

    return (own_files | team_files).distinct()
