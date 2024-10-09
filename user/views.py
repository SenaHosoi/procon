from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import CustomUser
from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password,check_password

# Create your views here.
def index(request):
    context = {'user': request.user}
    return render(request, 'index.html', context)


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            # ここでユーザーを取得しようとします
            user = CustomUser.objects.get(username=username)
            # ユーザーが見つかった場合はリダイレクト
            return HttpResponseRedirect('/user')
        
        except ObjectDoesNotExist:
            # ユーザーが見つからなかった場合は新規作成
            hashed_password = make_password(password)  # パスワードをハッシュ化
            new_user = CustomUser(username=username, password=hashed_password)
            new_user.save()
            return HttpResponse('ユーザーの作成に成功しました')
    else:
        return HttpResponseRedirect('/user')
     

def signin(request):
    username = request.POST['username']
    password = request.POST['password']

    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return HttpResponse('ログインに失敗しました')

    # if user.password == password:
    #     login(request, user)  # これを実行するとユーザをログイン状態にできる
    #     return HttpResponseRedirect('/user')
    # else:
    #     return HttpResponse('ログインに失敗しました')
    if check_password(password, user.password):  # ハッシュ化されたパスワードを確認
        login(request, user)  # ユーザをログイン状態にする
        return HttpResponseRedirect('/user')
    else:
        return HttpResponse('ログインに失敗しました')


def signout(request):
    logout(request)
    return HttpResponseRedirect('/user')





# Username: admin
# Email address: admin@ac.jp
# Password:admin