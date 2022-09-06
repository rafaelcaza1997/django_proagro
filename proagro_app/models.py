from django.db import models

# Create your models here.
class Cadastro(models.Model):

    nome_produtor = models.CharField(max_length=254)
    email_produtor = models.EmailField(max_length=254)
    cpf_produtor = models.CharField(max_length = 11)
    lat_lavoura = models.CharField(max_length = 20)
    long_lavoura = models.CharField(max_length = 20)
    tipo_lavoura = models.CharField(max_length = 20)
    data_colheita = models.DateField()
    evento = models.CharField(max_length = 20)
    status = models.CharField(max_length = 20)
    
    data_solicitacao = models.DateField(auto_now_add = True)
    data_ultima_modificacao = models.DateField(auto_now = True)
    id_analista = models.CharField(max_length = 5)
