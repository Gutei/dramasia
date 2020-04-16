from django.utils.html import mark_safe
from django.contrib import admin
from dramasia.models import Drama, DramaTag, Genre, DramaGenre, Cast, DramaCast, Season, DramaSeason, MdlDrama
from dramasia.tasks import sync_mdl

class SeasonInline(admin.TabularInline):
    model = DramaSeason
    raw_id_fields = ('drama',)
    extra = 1

class CastInline(admin.TabularInline):
    model = DramaCast
    raw_id_fields = ('cast',)
    extra = 1

class GenreInline(admin.TabularInline):
    model = DramaGenre
    raw_id_fields = ('genre',)
    extra = 1

@admin.register(Drama, site=admin.site)
class DramaAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_image', 'is_publish', 'created', 'updated')
    search_fields = ('title',)
    list_filter = ('is_publish', 'created', 'updated')
    list_per_page = 10

    inlines = [
        CastInline,
        GenreInline,
    ]

    def get_image(self, obj):
        if obj.image:
            image = obj.image.url
            return mark_safe("<img src='{}' width='30'>".format(image))

        return '-'

    get_image.admin_order_field = 'image'
    get_image.short_description = 'Image'


@admin.register(Cast, site=admin.site)
class CastAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_image',)
    search_fields = ('name',)
    list_per_page = 10

    def get_image(self, obj):
        if obj.image:
            image = obj.image.url
            return mark_safe("<img src='{}' width='30'>".format(image))

        return '-'

    get_image.admin_order_field = 'image'
    get_image.short_description = 'Image'

@admin.register(Genre, site=admin.site)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre',)
    search_fields = ('genre',)
    list_per_page = 10


@admin.register(Season, site=admin.site)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 10

    inlines = [
        SeasonInline,
    ]


@admin.register(MdlDrama, site=admin.site)
class MdlDramaAdmin(admin.ModelAdmin):
    list_display = ('id', 'created')
    search_fields = ('id', 'mdl_id')
    list_filter = ('created',)
    exclude = ('log',)
    change_form_template = "admin/mdldrama/change_form.html"

    def save_model(self, request, obj, form, change):
        # custom stuff here
        sync_mdl.apply_async((obj.mdl_id,))
        super().save_model(request, obj, form, change)