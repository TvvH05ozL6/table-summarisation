from django.contrib import admin

from .models import Tables, Table_Datas, Table_Annotations

admin.site.register(Tables)
admin.site.register(Table_Datas)
admin.site.register(Table_Annotations)
