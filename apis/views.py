from django.shortcuts import render

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.validators import validate_email, ValidationError
from django.contrib.auth import authenticate, login, logout


# Create your views here.

# CBV 기반의 api 구현
class BaseView(View):
    @staticmethod
    def response(data={}, message='', status=200):
        result = {
            'data': data,
            'message': message,

        }
        return JsonResponse(result, status)


# 유저 생성 및 예외처리 구현
class UserCreateView(BaseView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)

    # post 입력 처리 및 검증 구현
    def post(self, request):
        username = request.POST.get('username', '')
        if not username:
            return self.response(message='아이디를 입력해 주세요.', status=400)
        password = request.POST.get('password', '')
        if not password:
            return self.response(message='비밀번호를 입력해 주세요.', status=400)
        email = request.POST.get('email', '')
        if not email:
            return self.response(message='이메일을 입력해 주세요.', status=400)
        else:
            try:
                validate_email(email)
            except ValidationError:
                self.response(message='올바른 이메일을 입력해 주세요.', status=400)

        # 예외 처리
        try:
            user = User.objects.create_user(username, password, email)
        except IntegrityError:
            return self.response(message='이미 존재하는 아이디 입니다.', status=400)

        return self.response({'user.id': user.id})


# 로그인 뷰
class UserLoginView(BaseView):
    def post(self, request):
        username = request.POST.get('username', '')
        if not username:
            return self.response(message='아이디를 입력해 주세요.', status=400)
        password = request.POST.get('password', '')
        if not password:
            return self.response(message='비밀번호를 입력해 주세요.', status=400)

        # authenticate 함수는 username, password이 일치하지 않을경우, None을 반환.
        user = authenticate(request, username=username, password=password)
        if user is None:
            return self.response(request, message='아이디 또는 비밀번호가 일치하지 않습니다.', status=400)
        login(request, user)

        return self.response()


class UserLogoutView(BaseView):
    def get(self, request):
        logout(self.request)
        return self.response()

