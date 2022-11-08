from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class MyUsernameValidator(validators.RegexValidator):
    regex = r"^[0-9]+\Z"
    message = _("学号只允许为数字")
    flags = 0


@deconstructible
class PhoneNumberValidator(validators.RegexValidator):
    regex = r"^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$"
    message = _("输入正确手机号")
    flags = 0
