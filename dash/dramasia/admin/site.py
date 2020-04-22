from django.contrib import admin
from dramasia.models import SiteTemplate
from django import forms
from django_ace import AceWidget


class LayoutForm(forms.ModelForm):
    content = forms.CharField(widget=AceWidget(mode='html', width="100%", height="500px"))
    class Meta:
        model = SiteTemplate
        fields = '__all__'


@admin.register(SiteTemplate, site=admin.site)
class SiteTemplateAdmin(admin.ModelAdmin):
    list_display = ('code', 'origin', 'is_active')
    search_fields = ('code', 'origin')
    list_filter = ('is_active', )
    list_per_page = 10
    form = LayoutForm
