#!/usr/bin/env python3
"""删除 WebVirtCloud 数据库里指定名字的实例记录。

由 vm-create-api 在删机后调用：直接 virsh undefine 会把记录留在面板库里，
下次打开「实例」页时面板去查一个已不存在的域就会 500。
"""
import os
import sys

BASE = "/srv/webvirtcloud"
sys.path.insert(0, BASE)
os.chdir(BASE)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webvirtcloud.settings")

import django  # noqa: E402

django.setup()

from instances.models import Instance  # noqa: E402

names = [n.strip() for n in sys.argv[1:] if n.strip()]
if not names:
    print("没有指定名字")
    sys.exit(0)

qs = Instance.objects.filter(name__in=names)
cnt = qs.count()
qs.delete()
print("forgot %d 条记录: %s" % (cnt, ", ".join(names)))