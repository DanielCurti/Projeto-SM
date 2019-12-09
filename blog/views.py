# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import Produto
from .models import Mensagem
from .models import Categoria
from .models import Cliente
from .models import Curtida
from .models import Descurtida
from .models import Promocao

from .forms import FormMensagem
from .forms import FormProduto
from .forms import FormLogin
from .forms import FormCadastro

from datetime import datetime 
from django.http import HttpResponse   
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def index(request):
   data = datetime.now()
   if data.hour >= 6 and data.hour < 12:
      x = "Bom dia!"
   elif data.hour >= 12 and data.hour <= 18:
      x = "Boa tarde!"
   else:
      x = "Boa noite!"

   y = data.day

   contexto = {'x': x, 'y': y}
   return render(request, 'blog/sobre.html', contexto)


def melhoravaliado(request):
   #Verificacao de autenticacao
   if request.user.is_authenticated == False:
      form = FormLogin()
      contexto = {"form": form, "mensagem": "Apenas usuários logados podem ver as avaliações."}
      return render(request, 'blog/autenticacao.html', contexto)
      
   lista_produtos = Produto.objects.order_by("-curtidas")[0:4]
   contexto = {'lista_produtos': lista_produtos}
   return render(request, 'blog/avaliacoes.html', contexto)

def pioravaliado(request):
   #Verificacao de autenticacao
   if request.user.is_authenticated == False:
      form = FormLogin()
      contexto = {"form": form, "mensagem": "Apenas usuários logados podem ver as avaliações."}
      return render(request, 'blog/autenticacao.html', contexto)
      
   lista_produtos = Produto.objects.order_by("-descurtidas")[0:4]
   contexto = {'lista_produtos': lista_produtos}
   return render(request, 'blog/avaliacoes.html', contexto)

def maisvistos(request):
   #Verificacao de autenticacao
   if request.user.is_authenticated == False:
      form = FormLogin()
      contexto = {"form": form, "mensagem": "Apenas usuários logados podem ver as avaliações."}
      return render(request, 'blog/autenticacao.html', contexto)
      
   lista_produtos = Produto.objects.order_by("-visualizacoes")[0:4]
   contexto = {'lista_produtos': lista_produtos}
   return render(request, 'blog/maisvistos.html', contexto)

def sobre(request):
   data = datetime.now()
   if data.hour >= 6 and data.hour < 12:
      x = "Bom dia!"
   elif data.hour >= 12 and data.hour <= 18:
      x = "Boa tarde!"
   else:
      x = "Boa noite!"

   y = data.day

   contexto = {'x': x, 'y': y}
   return render(request, 'blog/sobre.html', contexto)

   
def detalhe_produto(request, x):
   #Verificacao de autenticacao
   if request.user.is_authenticated == False:
      form = FormLogin()
      contexto = {"form": form, "mensagem": "Apenas usuários logados podem fazer compras."}
      return render(request, 'blog/autenticacao.html', contexto)
   
   c = request.user
   cliente = Cliente.objects.get(user=c)

   p = Produto.objects.get(id=x)

   curtiu = cliente.curtiu(c,p)
   if curtiu == True:
      resposta = 'sim'
   else:
      resposta = 'não'
   
   bebidas = Categoria.objects.get(id=1)
   aperitivos = Categoria.objects.get(id=2)
   carnes = Categoria.objects.get(id=4)
   hortalicas = Categoria.objects.get(id=10)
   legumes = Categoria.objects.get(id=12)
   cervejas = Categoria.objects.get(id=18)

   #Homens entre 18 e 30 anos consomem cerveja com carne;
   if cliente.idade >= 18 and cliente.idade <= 40 and cliente.sexo == 'Masculino' and p.id_categoria == cervejas and p.valor <= 8:
      lista_indica = Produto.objects.filter(id_categoria=4).order_by('valor')[0:1]
   elif cliente.idade >= 18 and cliente.idade <= 40 and cliente.sexo == 'Masculino' and p.id_categoria == cervejas and p.valor >= 8.01:
      lista_indica = Produto.objects.filter(id_categoria=4).order_by('-valor')[0:1]
   elif cliente.idade >= 18 and cliente.idade <= 40 and cliente.sexo == 'Masculino' and p.id_categoria == carnes and p.valor <= 29.99:
      lista_indica = Produto.objects.filter(id_categoria=18).order_by("valor")[0:1]
   elif cliente.idade >= 18 and cliente.idade <= 40 and cliente.sexo == 'Masculino' and p.id_categoria == carnes and p.valor >= 30 :
      lista_indica = Produto.objects.filter(id_categoria=18).order_by("-valor")[0:1]

   #Mulheres entre 18 e 27 anos consomem bebidas com aperitivos;
   elif cliente.idade >= 18 and cliente.idade <= 27 and cliente.sexo == 'Feminino' and p.id_categoria == bebidas and p.valor <= 6:
      lista_indica = Produto.objects.filter(id_categoria=2).order_by('valor')[0:1]
   elif cliente.idade >= 18 and cliente.idade <= 27 and cliente.sexo == 'Feminino' and p.id_categoria == bebidas and p.valor >= 6.01:
      lista_indica = Produto.objects.filter(id_categoria=2).order_by('-valor')[0:1]
   elif cliente.idade >= 18 and cliente.idade <= 27 and cliente.sexo == 'Feminino' and p.id_categoria == aperitivos and p.valor <= 6:
      lista_indica = Produto.objects.filter(id_categoria=1).order_by("valor")[0:1]
   elif cliente.idade >= 18 and cliente.idade <= 27 and cliente.sexo == 'Feminino' and p.id_categoria == aperitivos and p.valor >= 6.01 :
      lista_indica = Produto.objects.filter(id_categoria=1).order_by("-valor")[0:1]

   #Mulheres entre 18 e 30 anos consomem bebidas com carne, geralmente suco ou refrigerante;
   elif cliente.idade >= 28 and cliente.idade <= 40 and cliente.sexo == 'Feminino' and p.id_categoria == bebidas and p.valor <= 8:
      lista_indica = Produto.objects.filter(id_categoria=4).order_by('valor')[0:1]
   elif cliente.idade >= 28 and cliente.idade <= 40 and cliente.sexo == 'Feminino' and p.id_categoria == bebidas and p.valor >= 8.01:
      lista_indica = Produto.objects.filter(id_categoria=4).order_by('-valor')[0:1]
   elif cliente.idade >= 28 and cliente.idade <= 40 and cliente.sexo == 'Feminino' and p.id_categoria == carnes and p.valor <= 29.99:
      lista_indica = Produto.objects.filter(id_categoria=1).order_by("valor")[0:1]
   elif cliente.idade >= 28 and cliente.idade <= 40 and cliente.sexo == 'Feminino' and p.id_categoria == carnes and p.valor >= 30 :
      lista_indica = Produto.objects.filter(id_categoria=1).order_by("-valor")[0:1]
   
   #Homens entre 40 e 45 anos, com bons salarios, consomem produtos mais procurados
   elif cliente.idade >= 40 and cliente.idade <= 45 and cliente.sexo == 'Masculino' and cliente.renda >= 3000:
      lista_indica = Produto.objects.filter(id__gte=40).order_by('-visualizacoes')[0:1]

   #Homens acima de 45 anos, com bons salarios, são consumistas e procuram boas avaliacoes
   elif cliente.idade >= 45 and cliente.sexo == 'Masculino' and cliente.renda >= 3000:
      lista_indica = Produto.objects.filter(id__gte=50).order_by('-curtidas')[0:1]
   
   #Mulheres entre 40 e 45 anos, com bons salarios, consomem produtos de categoria relacionada a frutas e hortaliças
   elif cliente.idade >= 40 and cliente.idade <= 45 and cliente.sexo == 'Feminino' and p.id_categoria == hortalicas:
      lista_indica = Produto.objects.filter(id_categoria=12)
   elif cliente.idade >= 40 and cliente.idade <= 45 and cliente.sexo == 'Feminino' and p.id_categoria == legumes:
      lista_indica = Produto.objects.filter(id_categoria=10)

   elif cliente.idade >= 50 and cliente.sexo == 'Masculino':
      lista_indica = Produto.objects.filter(id_categoria=8)

   elif cliente.idade >= 50 and cliente.sexo == 'Feminino':
      lista_indica = Produto.objects.filter(id_categoria=15)
      
   else:
      lista_indica = Produto.objects.filter(id_categoria=p.id_categoria).order_by("-visualizacoes")[0:1]

   p.visualizacoes = p.visualizacoes + 1
   p.save()
   contexto = {"p":p, "lista_indica":lista_indica, "resposta":resposta}
   return render(request, 'blog/detalhe_produto.html', contexto)

'''
if cliente.idade >= 20 and cliente.idade <= 29 and cliente.renda >= 500 and cliente.renda <= 999 and p.id_categoria == 'Aperitivos':
      lista_indica = Produto.objects.filter(valor__lte=1).filter(id_categoria = 'Bebidas')[0:1]
   elif cliente.idade >= 20 and cliente.idade <= 29 and cliente.renda >= 500 and cliente.renda <= 999 and p.id_categoria == 'Bebidas':
      lista_indica = Produto.objects.filter(valor__lte=1).filter(id_categoria = 'Aperitivos')[0:1]
   elif cliente.idade >= 30 and cliente.idade <= 39 and cliente.renda >= 1000 and cliente.renda <= 1999 and p.id_categoria == 'Aperitivos':
      lista_indica = Produto.objects.filter(valor__lte=5).filter(id_categoria = 'Bebidas')[0:1]
   elif cliente.idade >= 30 and cliente.idade <= 39 and cliente.renda >= 1000 and cliente.renda <= 1999 and p.id_categoria == 'Bebidas':
      lista_indica = Produto.objects.filter(valor__lte=5).filter(id_categoria = 'Aperitivos')[0:1]
   elif cliente.idade >= 40 and cliente.idade <= 49 and cliente.renda >= 2000 and cliente.renda <= 2999 and p.id_categoria == 'Aperitivos':
      lista_indica = Produto.objects.filter(valor__lte=10).filter(id_categoria = 'Bebidas')[0:1]
   elif cliente.idade >= 40 and cliente.idade <= 49 and cliente.renda >= 2000 and cliente.renda <= 2999 and p.id_categoria == 'Bebidas':
      lista_indica = Produto.objects.filter(valor__lte=10).filter(id_categoria = 'Aperitivos')[0:1]
   else:
      lista_indica = Produto.objects.filter(isualizacoes <= 10)[0:1]
'''

def categoria_produto(request, x):
   #Verificacao de autenticacao
   if request.user.is_authenticated == False:
      form = FormLogin()
      contexto = {"form": form, "mensagem": "Apenas usuários logados podem verificar produtos e suas categorias."}
      return render(request, 'blog/autenticacao.html', contexto)
      
   lista_produtos = Produto.objects.filter(id_categoria = x).order_by('valor')
   lista_categoria = Categoria.objects.order_by('titulo')
   contexto = {"lista_produtos":lista_produtos, "lista_categoria":lista_categoria}
   return render(request, 'blog/categoria_produto.html', contexto)

def novo_like(request, x):
   #Verificacao de autenticacao
   if request.user.is_authenticated == False:
      form = FormLogin()
      contexto = {"form": form, "mensagem": "Apenas usuários logados podem avaliar um produto."}
      return render(request, 'blog/autenticacao.html', contexto)
   else:
      usuario = request.user
      produto = Produto.objects.get(id=x)
      c = Curtida(user=usuario, produto=produto)
      c.save()
      
      produto.curtidas = produto.curtidas + 1
      produto.save()
      
   return HttpResponseRedirect("/blog/"+str(x)+"/detalhe_produto")
   
def novo_dislike(request, x):
   #Verificacao de autenticacao
   if request.user.is_authenticated == False:
      form = FormLogin()
      contexto = {"form": form, "mensagem": "Apenas usuários logados podem avaliar um produto."}
      return render(request, 'blog/autenticacao.html', contexto)
   else:
      usuario = request.user
      produto = Produto.objects.get(id=x)
      d = Descurtida(user=usuario, produto=produto)
      d.save()

      produto.descurtidas = produto.descurtidas + 1
      produto.save()
      
   return HttpResponseRedirect("/blog/"+str(x)+"/detalhe_produto")
   
def comprar(request, x):
   #Verificacao de autenticacao
   if request.user.is_authenticated == False:
      form = FormLogin()
      contexto = {"form": form, "mensagem": "Apenas usuários logados podem fazer compras."}
      return render(request, 'blog/autenticacao.html', contexto)
   
   p = Produto() 
   p = Produto.objects.get(id=x)
   p.quantidade = p.quantidade - 1
   p.save()
   return HttpResponseRedirect('/blog/produtos')



def excluir(request, x):
   #Verificacao de autenticacao
   if request.user.is_authenticated == False:
      form = FormLogin()
      contexto = {"form": form, "mensagem": "Apenas administrador logados podem excluir produtos."}
      return render(request, 'blog/autenticacao.html', contexto)
      
   p = Produto() 
   p = Produto.objects.get(id=x).delete()
   return HttpResponseRedirect('/blog/produtos')


def produtos(request):
   #Verificacao de autenticacao
   if request.user.is_authenticated == False:
      form = FormLogin()
      contexto = {"form": form, "mensagem": "Apenas usuários logados podem fazer compras."}
      return render(request, 'blog/autenticacao.html', contexto)
      
   lista_produtos = Produto.objects.order_by('valor') #consulta
   lista_categoria = Categoria.objects.order_by('titulo')
   lista_promocoes = Promocao.objects.all()
   contexto = {"lista_produtos": lista_produtos, "lista_categoria" : lista_categoria, "lista_promocoes":lista_promocoes} #contexto  
   return render(request, 'blog/produtos.html', contexto)


def nova_mensagem(request):
   #Verificacao de autenticacao
   if request.user.is_authenticated == False:
      form = FormLogin()
      contexto = {"form": form, "mensagem": "Apenas usuários logados podem enviar mensagens."}
      return render(request, 'blog/autenticacao.html', contexto)
      
   if request.method == 'POST':
      form = FormMensagem(request.POST)
      if form.is_valid():
           
          ### Salva a mensagem 
         m = Mensagem()
         m.nome = form.cleaned_data['nome']
         m.texto = form.cleaned_data['texto']
         m.assunto = form.cleaned_data['assunto']
         m.email = form.cleaned_data['email']
         m.save()

         return HttpResponseRedirect('/blog/') 
   else:
      form = FormMensagem() 

   contexto = {"form": form}
   return render(request, 'blog/mensagem.html', contexto)


def novo_produto(request):
   #Verificacao de autenticacao
   if request.user.is_authenticated == False:
      form = FormLogin()
      contexto = {"form": form, "mensagem": "Apenas usuários logados podem cadastrar produtos."}
      return render(request, 'blog/autenticacao.html', contexto)
      
   if request.method == 'POST':
      #Tratar os dados vindos do formulário
      form = FormProduto(request.POST)
      if form.is_valid():
         #Salvando um novo post
         p = Produto() 
         p.nome = form.cleaned_data['nome']
         p.marca = form.cleaned_data['marca']
         p.descricao = form.cleaned_data['descricao']
         p.unidade = form.cleaned_data['unidade']
         p.categoria = form.cleaned_data['categoria']
         p.valor = form.cleaned_data['valor']
         p.quantidade = form.cleaned_data['quantidade']
         p.foto = form.cleaned_data['foto']
         p.data_cadastro = form.cleaned_data['data_cadastro']
         p.save()
         return HttpResponseRedirect('/blog/produtos')
      else:
         return HttpResponse("Formulário inválido")
   else:
      #Exibir o formulário (Vindo do GET)
      form = FormProduto()
      contexto = {"form": form}
      return render(request, 'blog/novo_produto.html', contexto)


def cadastro(request):
	#Verificacao de autenticacao
   if request.user.is_authenticated == True:
      form = FormCadastro()
      contexto = {"form": form, "mensagem": "Você já esta cadastrado."}
      return render(request, 'blog/produtos.html', contexto)

   if request.method == 'POST':
      #Tratar os dados vindos do formulário
      form = FormCadastro(request.POST)
      if form.is_valid():
         #Salvando um novo cliente
         nome = form.cleaned_data['nome']
         sobrenome = form.cleaned_data['sobrenome']
         usuario = form.cleaned_data['usuario']
         email = form.cleaned_data['email']
         senha = form.cleaned_data['senha']

         sexo = form.cleaned_data['sexo']
         idade = form.cleaned_data['idade']
         renda = form.cleaned_data['renda']

         novoUsuario = User.objects.create_user(first_name=nome, last_name=sobrenome, username=usuario, email=email, password=senha)
         novoUsuario.cliente.sexo = sexo
         novoUsuario.cliente.idade = idade
         novoUsuario.cliente.renda = renda

         novoUsuario.save()
         
         contexto = {"mensagem": "Você foi cadastrado com sucesso! Faça login para começar a desfrutar dos nossos serviços"}
         return HttpResponseRedirect('/blog/autenticar', contexto)
      else:
         return HttpResponse("Formulário inválido")
   else:
      #Exibir o formulário (Vindo do GET)
      form = FormCadastro()
      contexto = {"form": form}
      return render(request, 'blog/cadastro.html', contexto)


def autenticar(request):
   if request.method == 'POST':
      #Tratar os dados vindos do formulário
      form = FormLogin(request.POST)
      if form.is_valid():
         username = form.cleaned_data['usuario']
         senha = form.cleaned_data['senha']
         
         #Autenticar
         usuario = authenticate(request, username=username, password=senha)
         if usuario is not None:
            login(request, usuario) #Mantém o usuário logado
            return HttpResponseRedirect('/blog/produtos')
         else:
            contexto = {"form": form, "mensagem": "Usuário ou senha inválida" }
            return render(request, 'blog/autenticacao.html', contexto)
      else:
         return HttpResponse("Formulário inválido")
   else:
      #Exibir o formulário (Vindo do GET)
      form = FormLogin()
      contexto = {"form": form}
      return render(request, 'blog/autenticacao.html', contexto)


def sair(request):
    logout(request)
    return HttpResponseRedirect('/blog/')

    




    
