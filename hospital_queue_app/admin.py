from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import *

admin.site.register(Patient)
admin.site.register(Cabinet)
admin.site.register(Profession)
admin.site.register(Procedure)
admin.site.register(Heap)
admin.site.register(HistoryHeap)
admin.site.unregister(User)
admin.site.unregister(Group)
