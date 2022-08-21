from .login import *
from .produtos import *
from django.shortcuts import render
from principal.models import EstoqueProdutoCategoria, EstoqueProduto, EstoqueProdutoCategoria


def quem_somos(req):
    return render(req, 'paginas/quem-somos.html', {
        "pagina": {
            "titulo": "Quem Somos",
            "descricao": "Página de quem somos",
            "atual": "quem-somos"
        }
    })


def index(request):
    return render(request, 'paginas/inicio.html', {
        "pagina":
        {
            "titulo": "Inicio",
            "descricao": "Página inicial",
            "atual": "inicio"
        },
        "produtos": EstoqueProduto.objects.filter(mostrar_inicio=True)[:5],
        "categorias": EstoqueProdutoCategoria.objects.filter(mostrar_inicio=True).order_by('nome')[:5]
    })


def categoria(request, id=None, txt=None):
    return render(request, 'paginas/categorias.html', {
        "pagina":
        {
            "titulo": "Categorias",
            "descricao": "Lista de todas as categorias disponíveis no sistema",
            "atual": "categorias"
        },
        "dados": {
            "categorias": EstoqueProdutoCategoria.objects.all()
        }
    })
