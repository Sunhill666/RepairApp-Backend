from rest_framework import generics, permissions, filters

from evaluation.models import EvaluationForm
from evaluation.serializers import GeneralEvaluationFormListSerializer, GeneralEvaluationFormSerializer
from repair.models import RepairForm
from utils.pagination import NumPagination


class EvaluationListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = NumPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['=evaluation_man']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return EvaluationForm.objects.all()
        rp_query = RepairForm.objects.filter(report_man=self.request.user)
        return EvaluationForm.objects.filter(repair_form__in=rp_query)

    def perform_create(self, serializer):
        rp = serializer.validated_data.get('repair_form')
        rp.status = RepairForm.Status.FID
        rp.save()
        serializer.save()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GeneralEvaluationFormListSerializer
        return GeneralEvaluationFormSerializer


class EvaluationRetrieveView(generics.RetrieveAPIView):
    serializer_class = GeneralEvaluationFormSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return EvaluationForm.objects.all()
        rp_query = RepairForm.objects.filter(report_man=self.request.user)
        return EvaluationForm.objects.filter(repair_form__in=rp_query)
