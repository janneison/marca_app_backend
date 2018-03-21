from django.contrib import admin
from asistencia.models import (Horario, Asistencia, Retraso, Permiso)


class AdminAsistencia(admin.ModelAdmin):
	list_display=('usuario','proyecto','entrada')
	search_fields=('entrada','usuario')
	list_filter=('proyecto','usuario')

class AdminHorario(admin.ModelAdmin):
	list_display=('proyecto','fechaInicio','fechaFin')
	search_fields=('fechaInicio','fechaFin')
	list_filter=('proyecto',)

class AdminPermiso(admin.ModelAdmin):
	list_display=('tipoAsignacion','fechaInicio','fechaFin')
	search_fields=('autorizo',)
	list_filter=('tipoAsignacion',)

admin.site.register(Asistencia,AdminAsistencia)
admin.site.register(Horario,AdminHorario)
admin.site.register(Permiso,AdminPermiso)