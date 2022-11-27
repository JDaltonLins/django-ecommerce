from django.utils import timezone
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.request import HttpRequest
from django.utils.http import urlencode
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q

from principal.models.estoque import EstoqueProduto, EstoqueProdutoCategoria, EstoqueProdutoSubcategoria, EstoqueProdutoTag


def produto(request, id, txt=''):
    try:
        produto: EstoqueProduto = EstoqueProduto.objects.get(id=id)

        if produto.data_lancamento is not None and produto.data_lancamento > timezone.now() and (not request.user.is_authenticated or request.user.is_superuser == False):
            return redirect_to(None, 'produtos')

        slug = produto.slug()
        if slug != txt:
            return redirect_to(request, ('produto', (slug, produto.id)))

        return render(request, 'paginas/produto.html', {
            "pagina": {
                "titulo": produto.nome,
                "descricao": produto.descricao
            },
            "dados": {
                "produto": produto,
                "carousel": produto.imagens.count() > 1,
                "prelancamento": produto.data_lancamento is not None and produto.data_lancamento > timezone.now(),
            },
            "produto": produto
        })
    except EstoqueProduto.DoesNotExist:
        return redirect(reverse('produtos'))


ORDER_MAP = {
    'nome': 'Nome',
    'data_lancamento': 'Data de Lançamento',
    'preco': 'Preço',
    'categoria': 'Categoria'
}

def redirect_to(request, page, **extra_fields):
    search_params = request.GET.dict() if request else {}

    for key, value in extra_fields.items():
        if value is None:
            del search_params[key]
        else:
            search_params[key] = value
    
    page, args = page if type(page) in (list, tuple) else (page, []) 

    return redirect(f'{reverse(page, args=args)}?{urlencode(search_params)}' if search_params else reverse(page, args=args))

def text_to_list(request, key):
    lista = []

    if not request or key not in request: 
        return lista

    text = request[key]
    for rawId in text.split(','):
        try:
            lista.append(int(rawId.strip()))
        except:
            pass
    
    return lista
    

def produtos(request: HttpRequest):
    pagina = 1

    if 'pagina' in request.GET:
        try:
            pagina = int(request.GET['pagina'])
        except ValueError:
            pagina = 0

    if pagina < 1:
        return redirect(request, 'produtos', pagina=1)

    produtos = EstoqueProduto.objects.all() if request.user.is_authenticated and request.user.is_superuser else EstoqueProduto.objects.filter(
        Q(data_lancamento__isnull=True) | Q(data_lancamento__lte=timezone.now()))

    categorias = text_to_list(request.GET, 'categorias')
    if categorias:
        produtos = produtos.filter(categoria__in=categorias)

    subcategorias = text_to_list(request.GET, 'subcategorias')
    if subcategorias:
        produtos = produtos.filter(id__in=EstoqueProdutoSubcategoria.objects.filter(
            id__in=subcategorias).values_list('estoqueproduto', flat=True))

    tag_list = text_to_list(request.GET, 'tags')
    if tag_list:
        produtos = produtos.filter(id__in=EstoqueProdutoTag.objects.filter(
            id__in=tag_list).values_list('estoqueproduto', flat=True))

    order_list = ORDER_MAP
    if "order_by" in request.GET:
        order = request.GET["order_by"]
        order_reverse, order_by = (True, order[1:]) if order.startswith("-") else (False, order)

        # Caso não exista essa coluna de ordenação,
        # redireciona para a pagina sem a definição desse argumento
        if order_by not in ORDER_MAP:
            return redirect_to(request, 'produtos', order_by=None)

        produtos = produtos.order_by(order)

        del order_list[order_by]

        order_key, order_value = (f'-{order_by}', f'- {ORDER_MAP[order_by]}') if not order_reverse \
            else (order_by, ORDER_MAP[order_by])

        order_list = {
            order_key: order_value,
            **order_list,
        }
    
    paginator = Paginator(produtos, 10)

    paginacao = None
    try:
        paginacao = paginator.page(pagina)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        paginacao = paginator.page(paginator.num_pages)

    return render(request, 'paginas/produtos.html', {
        "pagina": {
            "titulo": "Produtos",
            "descricao": "Produtos",
            "atual": "produtos"
        },
        "dados": {
            "selected_categorias": categorias,
            "selected_subcategorias": subcategorias,
            "selected_tags": tag_list,
            "ordens": order_list.items(),
            "paginacao": paginacao,
            "tags": EstoqueProdutoTag.objects.all(),
            "categorias": EstoqueProdutoCategoria.objects.all(),
            "subCategorias": EstoqueProdutoSubcategoria.objects.all(),

        },
        "sessao": {
            "esta_logado": True,
            "imagem_url": "https://img.freepik.com/fotos-gratis/3d-rendem-de-uma-mesa-de-madeira-com-uma-imagem-defocussed-de-um-barco-em-um-lago_1048-3432.jpg?w=2000"
        }
    })
