from django.urls import path, re_path

from .views import index, produto, produtos, categoria, login, logout, register, quem_somos

urlpatterns = [
    path('', index, name="inicio"),
    path('quem-somos', quem_somos, name="quem-somos"),
    path('produto/<slug:txt>-<int:id>', produto, name="produto"),
    path('produto/<int:id>', produto, name="produto"),
    re_path(r'^produtos(?P<url>\?.*)?', produtos, name="produtos"),
    path('categorias', categoria, name="categorias"),
    path('login', login, name="login"),
    path('logout', logout, name="logout"),
    path('registrar', register, name="register")
]
