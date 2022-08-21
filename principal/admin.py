from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import *
from django.contrib.auth.hashers import make_password


class EstoqueProdutoAdmin (ModelAdmin):
    list_display = ('nome', 'descricao', 'categoria')
    list_filter = ('nome', 'categoria', 'tags')


class EstoqueProdutoCategoriaAdmin (ModelAdmin):
    list_display = ('nome',)


class EstoqueProdutoSubcategoriaAdmin (ModelAdmin):
    list_display = ('nome',)


admin.site.register(EstoqueProduto, EstoqueProdutoAdmin)
admin.site.register(EstoqueProdutoCategoria, EstoqueProdutoCategoriaAdmin)
admin.site.register(EstoqueProdutoSubcategoria,
                    EstoqueProdutoSubcategoriaAdmin)
admin.site.register([EstoqueProdutoImagem, EstoqueProdutoTag])
admin.site.register(Usuario)
