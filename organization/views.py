import datetime
from io import BytesIO

from django.middleware.csrf import get_token
from django.http import HttpResponse
from rest_framework import filters, viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from openpyxl import Workbook 

from organization import custom_permissions
from organization.models import User, Team, UserProfile
from organization.serializers import TeamSerializer, UserSerializer, AdminUserListSerializer, ExportUserProfileSerializer


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=True)
    permission_classes = [custom_permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]
    serializer_class = UserSerializer
    search_fields = ['=username']

    def get_serializer_class(self):
        if not self.kwargs.get('pk') and self.request.method == "GET":
            return AdminUserListSerializer
        else:
            return UserSerializer


class AdminTeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    permission_classes = [custom_permissions.IsAdminUser]


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def change_pwd(request):
    user = request.user
    if user.check_password(request.data.get('password')):
        request.data.update({'password': request.data.get('new_password')})
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': "密码修改成功"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'detail': "旧密码错误"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_csrf_token(request):
    return Response({'csrf_token': get_token(request)})


@api_view(['GET'])
@permission_classes([custom_permissions.IsAdminUser])
def get_workbook(request):
    qs = UserProfile.objects.all()
    datas = ExportUserProfileSerializer(instance=qs, many=True).data
    wb = Workbook()
    ws = wb.active
    ws.append([
        "姓名", "服务次数", "总评平均评分", "态度平均评分", "效率平均评分", "速度平均评分",
    ])
    for data in datas:
        ws.append([
            User.objects.get(username=data.get('user')).get_full_name(),
            data['service_num'],
            data['total_avg'],
            data['attitude_avg'],
            data['proficiency_avg'],
            data['speed_avg'],
        ])
    output = BytesIO()
    wb.save(output)
    wb.close()
    filename = "export_data_" + datetime.datetime.now().strftime("%Y-%m-%d")
    response = HttpResponse(output.getvalue(), headers={
        'Content-Type': 'application/vnd.ms-excel',
        'Content-Disposition': 'attachment; filename="{0}.xlsx"'.format(filename)
    })
    return response
