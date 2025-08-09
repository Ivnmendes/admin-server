from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Mod
from .forms import ModForm, ModManualForm
from .utils import scrappling_steam_workshop, set_restart_pending_flag, update_server_mods
import re

@admin.register(Mod)
class ModAdmin(admin.ModelAdmin):
    list_display = ('name', 'workshop_id', 'mod_id', 'status', 'suggested_by')
    list_filter = ('status',)
    search_fields = ('name', 'workshop_id')

    actions = ['enable_mods', 'disable_mods']

    def has_change_permission(self, request, obj = ...):
        return False

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()

        info = self.model._meta.app_label, self.model._meta.model_name
        add_url_name = f'{info[0]}_{info[1]}_add'
        
        custom_urls = [
            path('add/', self.admin_site.admin_view(self.add_view),name=add_url_name),
        ]
        return custom_urls + urls

    def add_view(self, request):
        url_form = None
        manual_form = None
        title = 'Adicionar Mod por URL'

        if request.method == 'POST':
            if 'url_submit' in request.POST:
                url_form = ModForm(request.POST)
                if url_form.is_valid():
                    url = url_form.cleaned_data['mod_link']
                    name, workshop_id, mod_id = scrappling_steam_workshop(url)

                    if name and workshop_id and mod_id:
                        mod_instance = Mod(name=name, workshop_id=workshop_id, mod_id=mod_id, mod_link=url, suggested_by=request.user)
                        mod_instance.save()
                        self.message_user(request, f"Mod '{name}' adicionado com sucesso.", messages.SUCCESS)
                        return redirect(reverse('admin:mods_mod_changelist'))
                    else:
                        self.message_user(request, "Falha no scraping. Insira os dados manualmente.", messages.WARNING)
                        ws_id_fallback = re.search(r'id=(\d+)', url).group(1) if re.search(r'id=(\d+)', url) else ''
                        manual_form = ModManualForm(initial={'workshop_id': ws_id_fallback})
                        url_form = None 
                        title = 'Adicionar Mod Manualmente'

            elif 'manual_submit' in request.POST:
                manual_form = ModManualForm(request.POST)
                title = 'Adicionar Mod Manualmente'
                if manual_form.is_valid():
                    instance = manual_form.save(commit=False)
                    instance.suggested_by = request.user
                    instance.save()
                    self.message_user(request, "Mod adicionado manualmente com sucesso.", messages.SUCCESS)
                    return redirect(reverse('admin:mods_mod_changelist'))
                url_form = None

        else:
            url_form = ModForm()

        context = {
            **self.admin_site.each_context(request),
            'title': title,
            'url_form': url_form,
            'manual_form': manual_form,
            'opts': self.model._meta,
            'add': True,
            'change': False,
            'has_view_permission': self.has_view_permission(request, None),
            'has_add_permission': self.has_add_permission(request),
            'has_change_permission': False,
            'has_delete_permission': False,
            'save_as': self.save_as,
            'save_on_top': self.save_on_top,
        }
        
        return render(request, 'add_mod.html', context)
    
    @admin.action(description='Habilitar Mods')
    def enable_mods(self, request, queryset):
        updated_count = queryset.update(status='enabled')
        update_server_mods()
        if updated_count != 0:
            set_restart_pending_flag(True)
        self.message_user(request, f"{updated_count} mod(s) habilitado(s) com sucesso.", messages.SUCCESS)

    @admin.action(description='Desabilitar Mods')
    def disable_mods(self, request, queryset):
        updated_count = queryset.update(status='disabled')
        update_server_mods()
        if updated_count != 0:
            set_restart_pending_flag(True)
        self.message_user(request, f"{updated_count} mod(s) desabilitado(s) com sucesso.", messages.SUCCESS)