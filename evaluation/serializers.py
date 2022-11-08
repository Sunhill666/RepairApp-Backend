from rest_framework import serializers

from evaluation.models import EvaluationForm


class EvaluationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationForm


class GeneralEvaluationFormSerializer(EvaluationFormSerializer):
    class Meta:
        model = EvaluationForm
        fields = '__all__'


class GeneralEvaluationFormListSerializer(EvaluationFormSerializer):
    class Meta:
        model = EvaluationForm
        fields = ['repair_form', 'repair_man', 'evaluation_man', 'total_rate']
