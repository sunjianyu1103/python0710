from django.shortcuts import render,redirect,reverse
import re
from django.http import JsonResponse
from .models import Passport
def register(request):
    '''显示用户注册页面'''
    return render(request, 'users/register.html')

# Create your views here.
def register_handle(request):
    '''进行用户注册处理'''
    # 接收数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')

    # 进行数据校验
    if not all([username, password, email]):
        # 有数据为空
        return render(request, 'users/register.html', {'errmsg': '参数不能为空!'})

    # 判断邮箱是否合法
    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        # 邮箱不合法
        return render(request, 'users/register.html', {'errmsg': '邮箱不合法!'})

    # 进行业务处理:注册，向账户系统中添加账户
    # Passport.objects.create(username=username, password=password, email=email)
    try:
        Passport.objects.add_one_passport(username=username, password=password, email=email)
    except:
        return render(request, 'users/register.html', {'errmsg': '用户名已存在！'})

    # 注册完，还是返回注册页。
    return redirect(reverse('books:index'))

def login(request):
    '''显示登录页面'''
    if request.COOKIES.get("username"):
        username = request.COOKIES.get("username")
        checked = 'checked'
    else:
        username = ''
        checked = ''
    context = {
        'username': username,
        'checked': checked,
    }

    return render(request, 'users/login.html', context)

def login_check(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')
    if not all([username, password, remember]):
        return JsonResponse({'res': 2})
    passport = Passport.objects.get_one_passport(username=username, password=password)
    if passport:
        next_url = reverse('books:index')
        jres = JsonResponse({'res':1, 'next_url': next_url})
        if remember == 'true':
            jres.set_cookie('username', username, max_age=7*24*3600)
        else:
            jres.delete_cookie('username')
        request.session['islogin'] = True
        request.session['username'] = username
        request.session['passport_id'] = passport.id
        return jres
    else:
        return JsonResponse({'res':0})
def logout(request):
    request.session.flush()
    return redirect(reverse('books:index'))

