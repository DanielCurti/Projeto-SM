from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Cliente
from .choices import SEXO_CHOICES, UNIDADE_CHOICES


class FormMensagem(forms.Form):
   nome = forms.CharField(label='Nome completo', max_length=100)
   email = forms.EmailField(max_length=200)
   assunto = forms.CharField(max_length=100)
   texto = forms.CharField(widget=forms.Textarea, max_length=1000)
   #Adicionando uma classe do Bootstrap para cada campo
   nome.widget.attrs['class'] = "form-control"
   email.widget.attrs['class'] = "form-control"
   assunto.widget.attrs['class'] = "form-control"
   texto.widget.attrs['class'] = "form-control"
   nome.widget.attrs['placeholder'] = "Informe seu nome completo"
   email.widget.attrs['placeholder'] = "Informe um e-mail válido para contato"
   assunto.widget.attrs['placeholder'] = "Informe sobre o que se trata sua reclamação"
   texto.widget.attrs['placeholder'] = "Escreva detalhadamente qual a sua dificuldade ou problema"
   

class FormProduto(forms.Form):
   nome = forms.CharField(max_length=21)
   marca = forms.CharField(max_length=100)   
   descricao = forms.CharField(widget=forms.Textarea)
   unidade = forms.CharField(max_length=2) # KG, LT, PÇ
   categoria = forms.CharField(widget=forms.Select, max_length=100)
   valor = forms.FloatField(initial=0.0) 
   quantidade = forms.IntegerField(initial=0.0)
   data_cadastro = forms.DateTimeField(widget=forms.SelectDateWidget, initial=timezone.now)  


class FormLogin(forms.Form):
   usuario = forms.CharField(label="Usuário", max_length=20) 
   senha = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=20)  
   #Adicionando uma classe do Bootstrap para cada campo
   usuario.widget.attrs['class'] = "form-control"
   senha.widget.attrs['class'] = "form-control"


class FormCadastro(forms.Form):
   model = Cliente

   nome = forms.CharField(label="Nome", max_length=100)
   sobrenome = forms.CharField(label="Sobrenome", max_length=100)
   email = forms.EmailField(max_length=50)
   usuario = forms.CharField(label="Usuário", max_length=20)
   senha = forms.CharField(max_length=20)

   sexo = forms.ChoiceField(choices = SEXO_CHOICES, label="", initial='', widget=forms.Select(), required=True)
   idade = forms.IntegerField()
   renda = forms.FloatField(initial=0.0) 

   nome.widget.attrs['class'] = "form-control"
   sobrenome.widget.attrs['class'] = "form-control"
   email.widget.attrs['class'] = "form-control"
   usuario.widget.attrs['class'] = "form-control"
   senha.widget.attrs['class'] = "form-control"
   sexo.widget.attrs['class'] = "form-control"
   idade.widget.attrs['class'] = "form-control"
   renda.widget.attrs['class'] = "form-control"

   nome.widget.attrs['placeholder'] = "Informe seu primeiro nome"
   sobrenome.widget.attrs['placeholder'] = "Informe seu segundo nome"
   email.widget.attrs['placeholder'] = "Informe um e-mail de confirmação"
   usuario.widget.attrs['placeholder'] = "Informe um nome de usuário para acesso"
   senha.widget.attrs['placeholder'] = "Cuidadosamente, informe sua senha"
   sexo.widget.attrs['placeholder'] = "Diga qual seu gênero sexual"
   idade.widget.attrs['placeholder'] = "Informe sua idade"
   renda.widget.attrs['placeholder'] = "Informe sua renda mensal"
   
   
   
   


















