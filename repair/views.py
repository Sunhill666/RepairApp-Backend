import datetime
from rest_framework import generics, status
from rest_framework import permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from organization import custom_permissions
from organization.models import User
from repair.models import RepairForm
from repair.serializers import NormalRepairFormDetailSerializer, GeneralRepairFormListSerializer, \
    AdminRepairFormDetailSerializer
from utils.pagination import NumPagination


class RepairFormListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = NumPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['=contact', '=open_id']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return RepairForm.objects.all()
        return RepairForm.objects.filter(report_man=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GeneralRepairFormListSerializer
        return NormalRepairFormDetailSerializer

    def perform_create(self, serializer):
        serializer.save(report_man=self.request.user)


class RepairFormRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return RepairForm.objects.all()
        return RepairForm.objects.filter(report_man=self.request.user)

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return AdminRepairFormDetailSerializer
        return NormalRepairFormDetailSerializer

    def perform_update(self, serializer):
        try:
            rp = self.queryset.get(pk=self.kwargs.get('pk'))
        except RepairForm.DoesNotExist:
            raise ValidationError({'detail': "表单id不存在"})
        rp_status = rp.status
        if self.request.user.is_superuser or rp_status == RepairForm.Status.RPT:
            serializer.save()
        else:
            raise ValidationError({'detail': "当前状态不允许修改"})

    def perform_destroy(self, instance):
        if instance.status == RepairForm.Status.RPT:
            instance.delete()
        raise ValidationError({'detail': "此维修单已委派禁止删除"})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def finish_repair(request):
    if request.data.__contains__('id'):
        try:
            rp = RepairForm.objects.filter(report_man=request.user).get(pk=request.data.get('id'))
        except RepairForm.DoesNotExist:
            return Response({'detail': "表单id不存在"}, status=status.HTTP_400_BAD_REQUEST)
        if rp.status != RepairForm.Status.APT:
            return Response({'detail': "表单未委派或已完成"}, status=status.HTTP_400_BAD_REQUEST)
        rp.status = RepairForm.Status.NRD
        rp.save()
        return Response({'detail': "已完成维修"}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': "表单id为空"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([custom_permissions.IsAdminUser])
def appoint_repair(request):
    if not request.data.__contains__('user') and not request.data.__contains__('repair_id'):
        return Response({'detail': "队员id和表单id未填写"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(pk=request.data.get('user'))
        rp = RepairForm.objects.get(pk=request.data.get('repair_id'))
    except User.DoesNotExist or RepairForm.DoesNotExist:
        return Response({'detail': "队员或表单不存在"}, status=status.HTTP_400_BAD_REQUEST)

    rp.appointment = user
    rp.status = RepairForm.Status.APT
    rp.accept_time = datetime.datetime.now()
    rp.save()
    return Response({'detail': "委派成功"}, status=status.HTTP_200_OK)
