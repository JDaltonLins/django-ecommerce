from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from principal.models import Usuario


def logout(request):
    logout_django(request)
    return redirect('inicio')


def register(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        if 'username' not in request.POST or 'email' not in request.POST or 'password' not in request.POST or\
                len(request.POST['email']) == 0 or len(request.POST['username']) == 0 or len(request.POST['password']) == 0:
            return render(request, 'paginas/register.html', {
                "pagina":
                {
                    "titulo": "Cadastro",
                    "descricao": "Cadastro de usuário"
                },
                'dados': {
                    'error': 'Preencha todos os campos',
                    'username': request.POST.get('username', ''),
                    'email': request.POST.get('email', '')
                }
            })

        # Validação dos campos 'email', 'username' e 'password'
        email: str = request.POST['email'].strip()
        username: str = request.POST['username'].strip()
        password: str = request.POST['password']

        if len(email) < 8 or len(username) < 8 or len(password) < 6:
            return render(request, 'paginas/register.html', {
                "pagina":
                {
                    "titulo": "Cadastro",
                    "descricao": "Cadastro de usuário"
                },
                'dados': {
                    'error': 'Preencha todos os campos completamente',
                    'username': username,
                    'email': email
                }
            })
        elif len(email) > 50 or len(username) > 50 or len(password) > 20:
            return render(request, 'paginas/register.html', {
                "pagina":
                {
                    "titulo": "Cadastro",
                    "descricao": "Cadastro de usuário"
                },
                'dados': {
                    'error': 'Preencha todos os campos',
                    'username': username,
                    'email': email
                }
            })

        # Verifica se o usuário já existe
        if Usuario.objects.filter(email=email).exists():
            return render(request, 'paginas/register.html', {
                "pagina":
                {
                    "titulo": "Cadastro",
                    "descricao": "Cadastro de usuário"
                },
                'dados': {
                    'error': 'E-mail já cadastrado',
                    'email': email
                }
            })
        elif Usuario.objects.filter(username=username).exists():
            return render(request, 'paginas/register.html', {
                "pagina":
                {
                    "titulo": "Cadastro",
                    "descricao": "Cadastro de usuário"
                },
                'dados': {
                    'error': 'Usuário já cadastrado',
                    'email': email
                }
            })
        else:
            # Cria o usuário e a sessão
            login_django(request, user=Usuario.objects.create_user(
                email, username, password))
            return redirect('inicio')
    return render(request, 'paginas/register.html', {
        "pagina":
        {
            "titulo": "Cadastro",
            "descricao": "Cadastro de usuário"
        }
    })


def login(request):
    if (request.method == 'POST'):
        email, password = request.POST['email'], request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login_django(request, user)
            return redirect('inicio')
        else:
            print('Usuário não encontrado ' + email + " - " + password)
            return render(request, 'paginas/login.html',
                          {
                              "pagina":
                              {
                                  "titulo": "Home",
                                  "descricao": "Página inicial"
                              },
                              'dados': {
                                  'error': 'Usuário ou senha inválidos',
                                  'email': email
                              }
                          })
    elif request.user.is_authenticated:
        return redirect('incio')

    return render(request, 'paginas/login.html', {
        "pagina":
        {
            "titulo": "Login",
            "descricao": "Logue-se para acessar o sistema"
        },
        "sessao": {
            "esta_logado": True,
            "imagem_url": "https://img.freepik.com/fotos-gratis/3d-rendem-de-uma-mesa-de-madeira-com-uma-imagem-defocussed-de-um-barco-em-um-lago_1048-3432.jpg?w=2000"
        }
    })
