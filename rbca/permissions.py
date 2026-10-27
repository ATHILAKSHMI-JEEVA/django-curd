from rest_framework.permissions import BasePermission


# class HasRolePermission(BasePermission):
#     def has_permission(self, request, view):

#         if not request.user.is_authenticated:
#             return False

#         try:
#             role=request.user.userrole.role.name
#         except Exception:
#             return False

#         return role in["Admin","Manager","Employee"]


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return(
            request.user.is_authenticated 
            and hasattr(request.user,"userrole")
            and request.user.userrole.role.name =="Admin")

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "userrole")
            and request.user.userrole.role.name == "Manager"
        )


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "userrole")
            and request.user.userrole.role.name == "Employee"
        )