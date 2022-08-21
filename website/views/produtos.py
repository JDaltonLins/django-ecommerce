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
            return redirect(reverse('produtos'))

        slug = produto.slug()
        if slug != txt:
            return redirect(reverse('produto', args=(slug, produto.id)))

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


order_map = {
    'nome': 'Nome',
    'data_lancamento': 'Data de Lançamento',
    'preco': 'Preço',
    'categoria': 'Categoria'
}


def produtos(request: HttpRequest):
    pagina = 1

    if 'pagina' in request.GET:
        try:
            pagina = int(request.GET['pagina'])
        except ValueError:
            pagina = 0

    if pagina < 1:
        return redirect(reverse('produtos') + '?' + urlencode({**request.GET.dict(), **{'pagina': 1}}))

    produtos = EstoqueProduto.objects.all() if request.user.is_authenticated and request.user.is_superuser else EstoqueProduto.objects.filter(
        Q(data_lancamento__isnull=True) | Q(data_lancamento__lte=timezone.now()))

    categorias = []
    if 'categorias' in request.GET:
        for categoria in request.GET['categorias'].split(','):
            try:
                categorias.append(int(categoria))
            except ValueError:
                pass
        produtos = produtos.filter(categoria__in=categorias)

    subcategorias = []
    if 'subcategorias' in request.GET:
        for subcategoria in request.GET['subcategorias'].split(','):
            try:
                subcategorias.append(int(subcategoria))
            except ValueError:
                pass
        produtos = produtos.filter(id__in=EstoqueProdutoSubcategoria.objects.filter(
            id__in=subcategorias).values_list('estoqueproduto', flat=True))

    tag_list = []
    if 'tags' in request.GET:
        for tag in request.GET['tags'].split(','):
            try:
                tag_list.append(int(tag))
            except ValueError:
                pass

        produtos = produtos.filter(id__in=EstoqueProdutoTag.objects.filter(
            id__in=tag_list).values_list('estoqueproduto', flat=True))

    # Realiza a ordenação dos produtos
    order_foo = request.GET['order_by'] if 'order_by' in request.GET else 'data_lancamento'
    order_by = ['data_lancamento',
                order_map['data_lancamento'], '-', '- Data Lançamento']

    order_name = order_foo.lstrip('-')  # Remove o - se existir
    order_by = [order_name, order_map[order_name],
                '-' if not order_foo.startswith('-') else '', '']
    order_by[3] = f'{order_by[2]} {order_by[1]}'
    if order_by[1]:
        produtos = produtos.order_by(order_foo)
    else:
        gict = request.GET.dict()
        gict.pop('order_by')
        return redirect(reverse('produtos') + '?' + urlencode(gict))

    order_map_rel = order_map.copy()
    order_map_rel.pop(order_by[0])

    order_map_rel = {
        **{f'{order_by[2]}{order_by[0]}': order_by[3]},
        **order_map_rel
    }
    order_by[1] = ('- ' if order_foo.startswith('-') else '') + order_by[1]

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
            "ordem": order_by,
            "ordens": order_map_rel.items(),
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
