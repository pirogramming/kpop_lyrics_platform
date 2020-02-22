from django.contrib import admin
from .models import Groups, Albums, Singers, Songs, Comments, Lyrics, Explanations


class SingersAdmin(admin.ModelAdmin):
    def display_singer_group(self):
        return ', '.join(group.gname for group in self.group.all()[:1])

    display_singer_group.short_description = 'group'
    list_display = ('sname', display_singer_group)


admin.site.register(Groups)
admin.site.register(Albums)
admin.site.register(Singers, SingersAdmin)
admin.site.register(Songs)
admin.site.register(Comments)
admin.site.register(Lyrics)
admin.site.register(Explanations)
