from django.contrib import admin
from .models import Produto, Categoria
from .models import Mensagem
from .models import Cliente
from .models import Curtida
from .models import Descurtida
from .models import Promocao

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#from .models import Recomendacao

admin.site.register(Produto)
admin.site.register(Categoria)
admin.site.register(Mensagem)
admin.site.register(Cliente)
admin.site.register(Curtida)
admin.site.register(Descurtida)
admin.site.register(Promocao)
#admin.site.register(Recomendacao)

class ClienteInline(admin.StackedInline):
   model = Cliente
   can_delete = False
   verbose_name_plural = 'cliente'

class UserAdmin(BaseUserAdmin):
   inlines = (ClienteInline, )