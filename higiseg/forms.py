from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Funcionario, Agendamento

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Login:', widget=forms.TextInput(attrs={'class': 'form-control', 'id':'name', 'placeholder': 'Usuario', 'data-sb-validations':'required'}))
    password = forms.CharField(label='Senha:', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id':'password', 'placeholder': 'Password', 'data-sb-validations':'required'}))

class AgendamentoForm(forms.ModelForm):
    dataAgendamento = forms.DateTimeField(label='Selecione a nova data', widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    funcionarioAgendamento = forms.ModelChoiceField(queryset=Funcionario.objects.all(), label='Selecione o funcionário', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Agendamento
        fields = ['funcionarioAgendamento', 'dataAgendamento']
        labels = {
            'dataAgendamento': 'Data do Agendamento'}
