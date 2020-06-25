from django.contrib import admin
from .models import Wall, Section, SectionField, Template, Circle
# Register your models here.
from django.contrib import messages

admin.site.site_header = 'Aapoon Wall'

class WallAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(WallAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

    def save_model(self, request, obj, form, change):
        if not change:  # newly created newsletter
            walls = Wall.objects.filter(created_by=obj.created_by)
            if len(walls) >= 3:
                messages.set_level(request, messages.ERROR)
                messages.error(request, "Only three Pages are allowed!")
            else:
                obj.save()
        else:
            obj.save()


admin.site.register(Wall, WallAdmin)
admin.site.register(Section)
admin.site.register(SectionField)
admin.site.register(Template)
admin.site.register(Circle)

