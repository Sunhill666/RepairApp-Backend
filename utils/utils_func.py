import hashlib

from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


def gen_md5_id(item):
    md5_machine = hashlib.md5()
    md5_machine.update(item.encode('utf-8'))
    return md5_machine.hexdigest()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_header(request):
    header_dict = dict(request.headers)
    header_dict.update({'username': request.user.username})
    return Response(header_dict, status=status.HTTP_200_OK)
