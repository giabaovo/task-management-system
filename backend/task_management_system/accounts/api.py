from rest_framework.views import APIView, status
from rest_framework.response import Response

from accounts.serializers import AccountSerializer


class AccountRegister(APIView):
    # Register API for account
    def post(self, request):
        data = request.data
        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message": "User register successfully"}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)