from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from .choices import SEXO_CHOICES, UNIDADE_CHOICES


class Cliente(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   # Adicionando os campos
   sexo = models.CharField(max_length=9, choices=SEXO_CHOICES)
   idade = models.IntegerField(default=0)
   renda = models.FloatField(default=0.0)

   class Meta:
      ordering = ['user']

   def __str__(self):
      return self.user.first_name + " " + self.user.last_name

   def curtiu(self, usuario, produto):
      curtidas = Curtida.objects.all()
      for x in curtidas:
         if x.user == usuario and x.produto == produto:
            return True
      descurtidas = Descurtida.objects.all()
      for x in descurtidas:
         if x.user == usuario and x.produto == produto:
            return True
      return False

@receiver(post_save, sender=User)
def criar_cliente(sender, instance, created, **kwargs):
    if created:
        Cliente.objects.create(user=instance)

@receiver(post_save, sender=User)
def salvar_cliente(sender, instance, **kwargs):
    instance.cliente.save()

class Promocao(models.Model):
   titulo = models.CharField(max_length=21)
   panfleto = models.FileField(upload_to="%Y/%m/%d/", blank=True)

   def __str__(self):
      return self.titulo

class Categoria(models.Model):
   titulo = models.CharField(max_length=20)
   class Meta:
      ordering = ['titulo']

   def __str__(self):
      return self.titulo

class Produto(models.Model):
   nome = models.CharField(max_length=21)  
   marca = models.CharField(default='', max_length=100)
   descricao = models.TextField()
   unidade = models.CharField(max_length=2, choices = UNIDADE_CHOICES) # KG, LT, PÇ
   valor = models.FloatField(default=0.0) 
   id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=1)
   quantidade = models.IntegerField(default=0)
   foto = models.FileField(upload_to="%Y/%m/%d/", blank=True)
   data_cadastro = models.DateTimeField(default=timezone.now)  
   visualizacoes = models.IntegerField(default=0)
   curtidas = models.IntegerField(default=0)   
   descurtidas = models.IntegerField(default=0)

   class Meta:
      ordering = ['nome']
   
   def __str__(self):
      return self.nome + " - R$ " + str(self.valor)  +  "  || DESCRIÇÃO: " + str(self.descricao) + "  || CATEGORIA: " + str(self.id_categoria.titulo) + " || ESTOQUE:" + " (" + str(self.quantidade) + ") ||"           
  


class Curtida(models.Model):
   user = models.ForeignKey("auth.User", on_delete=models.CASCADE) 
   produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
   data_criacao = models.DateTimeField(default=timezone.now)

   def __str__(self):
      return self.user.first_name + " " + self.user.last_name + " - Gostou do produto: " + self.produto.nome

class Descurtida(models.Model):
   user = models.ForeignKey("auth.User", on_delete=models.CASCADE) 
   produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
   data_criacao = models.DateTimeField(default=timezone.now)

   def __str__(self):
      return self.user.first_name + " " + self.user.last_name + " - Não gostou do produto: " + self.produto.nome
 
class Mensagem(models.Model):

   nome = models.CharField(max_length=100)
   email = models.EmailField(max_length=200)
   assunto = models.CharField(max_length=100)
   texto = models.TextField()
   data = models.DateTimeField(default=timezone.now)

   def __str__(self):
      return self.nome + ': ' + self.assunto