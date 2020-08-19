from django.contrib import admin
from .models import Wall, Section, SectionField, Template, Circle
# Register your models here.
from django.contrib import messages
from django.utils.html import mark_safe
from django.urls import reverse

admin.site.site_header = 'Aapoon Wall'

class WallAdmin(admin.ModelAdmin):

    readonly_fields = ['wall_link_url']
    exclude = ['created_by']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'template':
            kwargs['initial'] = "Basic"

        return super(WallAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


    def wall_link_url(self, obj):
        url = reverse('wall', args=["test"])
        return mark_safe("<a target='_new' href='%s'>%s</a>" % (url, url))

    def get_queryset(self, request):
        qs = super(WallAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        # if not change:  # newly created newsletter
        #     walls = Wall.objects.filter(created_by=request.user)
        #     if len(walls) >= 3:
        #         messages.set_level(request, messages.ERROR)
        #         messages.error(request, "Only three Pages are allowed!")
        #         from django.http import HttpResponseRedirect
        #         return HttpResponseRedirect(request.path)
        #     else:
        #         obj.save()
        # else:
        obj.save()


admin.site.register(Wall, WallAdmin)
admin.site.register(Section)
admin.site.register(SectionField)
admin.site.register(Template)
admin.site.register(Circle)

