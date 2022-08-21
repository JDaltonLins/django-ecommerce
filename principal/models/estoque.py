from django.db import models
from slugify import slugify


class EstoqueProduto (models.Model):
    nome = models.CharField(max_length=100)
    mostrar_inicio = models.BooleanField(default=True)
    descricao = models.TextField()
    informacoes = models.TextField()
    preco = models.DecimalField(max_digits=7, decimal_places=2)
    categoria = models.ForeignKey(
        'EstoqueProdutoCategoria', on_delete=models.RESTRICT)
    subcategorias = models.ManyToManyField(
        'EstoqueProdutoSubcategoria', blank=True)
    tags = models.ManyToManyField('EstoqueProdutoTag', blank=True)
    imagens = models.ManyToManyField('EstoqueProdutoImagem')
    data_lancamento = models.DateTimeField(blank=True, null=True)

    def slug(self):
        return slugify(self.nome)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['descricao']


class EstoqueProdutoImagem (models.Model):
    imagem = models.ImageField(upload_to='produtos')

    class Meta:
        verbose_name = 'Image de Produto'
        verbose_name_plural = 'Imagens de Produtos'


class EstoqueProdutoTag (models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['nome']


class EstoqueProdutoCategoria (models.Model):
    nome = models.CharField(max_length=100)
    mostrar_inicio = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

    def produtos(self, limit=15):
        return EstoqueProduto.objects.filter(categoria=self.id)[:limit]

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']


class EstoqueProdutoSubcategoria (models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Subcategoria'
        verbose_name_plural = 'Subcategorias'
