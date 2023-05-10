from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MyUser


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    nickname = forms.CharField(max_length=30, required=True)
    mbti = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = MyUser
        fields = ('email', 'password1', 'password2', 'nickname', 'mbti')
        labels = {
            'email': '이메일',
            'password1': '비밀번호',
            'password2': '비밀번호 확인',
            'nickname': '닉네임',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.mbti = self.cleaned_data.get('mbti', None)
        if commit:
            user.save()
        return user



class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


MBTI_CHOICES = [
    ('ISTJ', 'ISTJ'), ('ISFJ', 'ISFJ'), ('INFJ', 'INFJ'), ('INTJ', 'INTJ'),
    ('ISTP', 'ISTP'), ('ISFP', 'ISFP'), ('INFP', 'INFP'), ('INTP', 'INTP'),
    ('ESTP', 'ESTP'), ('ESFP', 'ESFP'), ('ENFP', 'ENFP'), ('ENTP', 'ENTP'),
    ('ESTJ', 'ESTJ'), ('ESFJ', 'ESFJ'), ('ENFJ', 'ENFJ'), ('ENTJ', 'ENTJ'),
]

class MBTIForm(forms.Form):
    mbti = forms.ChoiceField(choices=MBTI_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), label='')
    # 문항 추가
    Q1 = forms.ChoiceField(label='당신은 외향적인 사람인가요?',
                           widget=forms.RadioSelect, 
                           choices=[('a', '예'), ('b', '아니오')])
    Q2 = forms.ChoiceField(label='당신은 생각이 깊지 않은 편인가요?',
                           widget=forms.RadioSelect, 
                           choices=[('a', '예'), ('b', '아니오')])
    Q3 = forms.ChoiceField(label='당신은 감성보다 이성을 중요시하나요?',
                           widget=forms.RadioSelect, 
                           choices=[('a', '예'), ('b', '아니오')])
    Q4 = forms.ChoiceField(label='당신은 계획적인 사람인가요?',
                           widget=forms.RadioSelect, 
                           choices=[('a', '예'), ('b', '아니오')])


    def calculate_mbti(self):
        # 문항 처리
        score_E = 0
        score_I = 0
        score_S = 0
        score_N = 0
        score_T = 0
        score_F = 0
        score_J = 0
        score_P = 0

        if self.cleaned_data['Q1'] == 'a':
            score_E += 1
        else:
            score_I += 1

        if self.cleaned_data['Q2'] == 'a':
            score_S += 1
        else:
            score_N += 1

        if self.cleaned_data['Q3'] == 'a':
            score_T += 1
        else:
            score_F += 1

        if self.cleaned_data['Q4'] == 'a':
            score_J += 1
        else:
            score_P += 1


        # MBTI 계산
        mbti = ''
        if score_E > score_I:
            mbti += 'E'
        else:
            mbti += 'I'
        if score_S > score_N:
            mbti += 'S'
        else:
            mbti += 'N'
        if score_T > score_F:
            mbti += 'T'
        else:
            mbti += 'F'
        if score_J > score_P:
            mbti += 'J'
        else:
            mbti += 'P'
        return mbti
