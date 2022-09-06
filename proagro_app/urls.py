from django.contrib import admin
from django.urls import include, path
from proagro_app import views


app_name = 'view_proagro'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('novo_cadastro', views.novo_cadastro, name = 'novo_cadastro'),
    path('cadastros', views.listar_cadastros, name = 'listar_cadastros'),
    path('editar/<int:pk>', views.editar_cadastro, name = 'editar_cadastro'),
    path('excluir/<int:pk>', views.excluir_cadastro, name = 'excluir_cadastro'),

]
