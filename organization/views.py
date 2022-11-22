import datetime
from io import BytesIO

from django.middleware.csrf import get_token
from rest_framework import filters, viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_pandas.io import read_frame
from django.http import HttpResponse

from organization import custom_permissions
from organization.models import User, Team, UserProfile
from organization.serializers import TeamSerializer, UserSerializer, AdminUserListSerializer


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
    df = read_frame(qs=qs)
    df.drop('id', axis=1, inplace=True)
    for row_index,row in df.iterrows():
        df.loc[row_index, 'user'] = User.objects.get(username=row['user']).get_full_name()  # type: ignore
    df.rename(
        columns={
            'user': "姓名",
            'service_num': "服务次数",
            'total_avg': "总评平均评分",
            'attitude_avg': "态度平均评分",
            'proficiency_avg': "效率平均评分",
            'speed_avg': "速度平均评分",
        }, inplace=True
    )
    output = BytesIO()
    df.to_excel(output, index=False)
    filename = "export_data_" + datetime.datetime.now().strftime("%Y-%m-%d")
    response = HttpResponse(output.getvalue(), headers={
        'Content-Type': 'application/vnd.ms-excel',
        'Content-Disposition': 'attachment; filename="{0}.xlsx"'.format(filename)
    })
    return response
