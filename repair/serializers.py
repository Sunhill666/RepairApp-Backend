from rest_framework import serializers

from repair.models import RepairForm


class RepairFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairForm


class AdminRepairFormDetailSerializer(RepairFormSerializer):
    class Meta:
        model = RepairForm
        fields = '__all__'


class NormalRepairFormDetailSerializer(RepairFormSerializer):
    class Meta:
        model = RepairForm
        exclude = ['report_man']
        read_only_fields = ['start_time', 'accept_time', 'end_time', 'status', 'appointment']


class GeneralRepairFormListSerializer(RepairFormSerializer):
    class Meta:
        model = RepairForm
        fields = ['id', 'name', 'role', 'type', 'start_time', 'accept_time', 'end_time', 'status', 'appointment']
