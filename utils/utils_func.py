import hashlib


def gen_md5_id(item):
    md5_machine = hashlib.md5()
    md5_machine.update(item.encode('utf-8'))
    return md5_machine.hexdigest()
