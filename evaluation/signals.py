from django.db.models.signals import post_save
from django.dispatch import receiver

from evaluation.models import EvaluationForm
from organization.models import UserProfile


@receiver(post_save, sender=EvaluationForm)
def eva_rate_cal(instance, created, **kwargs):
    if created:
        rp_man = instance.repair_man
        eva_forms = EvaluationForm.objects.filter(repair_man=rp_man)
        total_rate = eva_forms.values_list('total_rate', flat=True)
        attitude_rate = eva_forms.values_list('attitude_rate', flat=True)
        proficiency_rate = eva_forms.values_list('proficiency_rate', flat=True)
        speed_rate = eva_forms.values_list('speed_rate', flat=True)

        rp_man_profile = UserProfile.objects.get(user=rp_man)
        rp_man_profile.total_avg = sum(total_rate) / len(total_rate)
        rp_man_profile.attitude_avg = sum(attitude_rate) / len(attitude_rate)
        rp_man_profile.proficiency_avg = sum(proficiency_rate) / len(proficiency_rate)
        rp_man_profile.speed_avg = sum(speed_rate) / len(speed_rate)
        rp_man_profile.service_num = eva_forms.count()
        rp_man_profile.save()
