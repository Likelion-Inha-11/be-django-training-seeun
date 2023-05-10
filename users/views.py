from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, MBTIForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy



def signup_complete(request):
    '''
    회원가입 완료 페이지를 보여주는 뷰
    '''
    return render(request, 'signup_complete.html')

def signup(request):
    '''
    회원가입을 처리하는 뷰
    GET 요청 시 회원가입 폼을 보여주고,
    POST 요청 시 회원가입 폼을 검증하고, 유효하다면 회원가입 처리 후 로그인시키고 mbti_test로 이동시킴
    '''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 회원 가입이 완료되면 로그인합니다.
            login(request, user)
            # MBTI 검사 페이지로 이동합니다.
            return redirect(reverse_lazy('mbti_test'))
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    '''
    로그인을 처리하는 뷰
    POST 요청 시 입력받은 이메일과 비밀번호로 사용자 인증 후 로그인시키고 home 페이지로 이동시킴
    '''
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, '로그인 실패: 이메일과 비밀번호를 확인하세요.')
    return render(request, 'login.html')


def user_logout(request):
    '''
    로그아웃을 처리하는 뷰
    로그아웃 후 home 페이지로 이동시킴
    '''
    logout(request)
    return redirect('home')


def home(request):
    '''
    home 페이지를 보여주는 뷰
    인증된 사용자는 자신의 이메일을 화면에 보여주고,
    인증되지 않은 사용자는 home 페이지를 보여줌
    '''
    if request.user.is_authenticated:
        username = request.user.username
        return render(request, 'home.html', {'username': username})
    else:
        return render(request, 'home.html')


# @login_required
def mbti_test(request):
    if request.method == 'POST':
        form = MBTIForm(request.POST)
        if form.is_valid():
            Q1 = form.cleaned_data['Q1']
            Q2 = form.cleaned_data['Q2']
            Q3 = form.cleaned_data['Q3']
            Q4 = form.cleaned_data['Q4']
            
            mbti = get_mbti(Q1, Q2, Q3, Q4)
            request.session['mbti'] = mbti  # MBTI 결과를 세션에 저장합니다.
            return redirect('mbti_result')
    else:
        form = MBTIForm()
    return render(request, 'mbti_test.html', {'form': form})


# @login_required
def mbti_result(request):
    mbti = request.session.get('mbti', None)  # 세션에서 MBTI 결과를 가져옵니다.
    if mbti:
        return render(request, 'mbti_result.html', {'mbti': mbti})
    else:
        return redirect('mbti_result')


@login_required
def community(request):
    return render(request, 'community.html')