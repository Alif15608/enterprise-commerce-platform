from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .permissions import IsAdmin
from .serializers import RoleSerializer, AssignRoleSerializer
from . import services
from .models import Role


class RoleListView(APIView):
    """Admin-only: list all available roles in the system."""
    permission_classes = [IsAdmin]

    def get(self, request):
        roles = Role.objects.all()
        return Response(RoleSerializer(roles, many=True).data)


class AssignRoleView(APIView):
    """Admin-only: grant a role to a user."""
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = AssignRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            _, created = services.assign_role(**serializer.validated_data)
        except services.RbacError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not created:
            return Response({"message": "User already has this role."}, status=status.HTTP_200_OK)
        return Response({"message": "Role assigned successfully."}, status=status.HTTP_201_CREATED)


class RevokeRoleView(APIView):
    """Admin-only: remove a role from a user."""
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = AssignRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.revoke_role(**serializer.validated_data)
        except services.RbacError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Role revoked successfully."})