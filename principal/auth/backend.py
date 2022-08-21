from django.contrib.auth.backends import ModelBackend, UserModel


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get(UserModel.USERNAME_FIELD)
        print(email, password)
        if email is None or password is None:
            return
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            print('Usuário não encontrado')
            return
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
