import datetime
from django.shortcuts import render, redirect
from .data_validation import DictCadastro
from .models import Cadastro
from haversine import haversine
from pydantic import ValidationError
# Create your views here.
# import pdb; pdb.set_trace()

def checar_distancia(lat_a,lon_a,lat_b,lon_b):
    loc_a = (float(lat_a),float(lon_a))
    loc_b = (float(lat_b),float(lon_b))
    return haversine(loc_a, loc_b)

def novo_cadastro(request):
    if request.method == 'POST':
            '''Cria um dicionario para a adição dos valores, adiciona um valor padrão ao status da solicitação'''
            dict_form = {"status" : "Aguardando"}
            for key, value in request.POST.items():
                '''Verifica se o input possui algum valor vazio. Esse verificação já é feita no front, mas por garantia tambem está sendo feita no backend.'''
                if value != "":
                    dict_form[key] = value
                else:
                    return render(request, 'proagro_app/novo_cadastro.html',{'modal_msg':"Todos os campos precisam ser preenchidos!"})
        
            '''Realiza o tratamento de valores, caso resulte em erro, o programa avisa o usuario.
            Esse erro dificilmente seria causado pelo uso no frontend, pois a validação do CPF já está sendo feita antes de chegar nesse ponto, e a entrada da data não é feita de maneira "escrita".
            '''   
            try:
                dict_form_validado = DictCadastro(**dict_form)
            except ValidationError as e:
                return render(request, 'proagro_app/novo_cadastro.html',{'modal_msg':e})
            
            try:
                colheita_mesma_data = Cadastro.objects.all().filter(data_colheita = dict_form_validado.data_colheita)
                for colheita in colheita_mesma_data:
                    lat_a = dict_form_validado.lat_lavoura
                    lon_a = dict_form_validado.long_lavoura
                    
                    lat_b = colheita.lat_lavoura
                    lon_b = colheita.long_lavoura
                    
                    if checar_distancia(lat_a,lon_a,lat_b,lon_b) <= 10:
                        if dict_form_validado.evento != colheita.evento:
                            return render(request, 'proagro_app/novo_cadastro.html',{'modal_msg':f"Um cadastro foi localizado com a mesma data de colheita, a menos de 10 km da propriedade atual, com eventos divergentes. CPF do produtor {colheita.cpf_produtor}"})
            except:
                '''Nenhuma colheita foi feita nessa data'''
                pass
            
            '''caso esteja tudo ok, um novo registro será criado, caso contrario, o usuario será notificado.'''
            try:
                cadastro = Cadastro()
                cadastro.nome_produtor = dict_form_validado.nome_produtor
                cadastro.email_produtor = dict_form_validado.email_produtor
                cadastro.cpf_produtor = dict_form_validado.cpf_produtor
                cadastro.lat_lavoura = dict_form_validado.lat_lavoura
                cadastro.long_lavoura = dict_form_validado.long_lavoura
                cadastro.tipo_lavoura = dict_form_validado.tipo_lavoura
                cadastro.data_colheita = dict_form_validado.data_colheita
                cadastro.evento = dict_form_validado.evento
                cadastro.status = dict_form_validado.status
                cadastro.id_analista = 1
                cadastro.save()    
                return render(request, 'proagro_app/novo_cadastro.html',{'modal_msg':"Cadastro realizado com sucesso!"})
            except Exception as e:
                return render(request, 'proagro_app/novo_cadastro.html',{'modal_msg':e})
    else:
        return render(request, 'proagro_app/novo_cadastro.html')
        
        
def criar_lista_cadastros(cadastros):
    dict_cadastros = [cadastro for cadastro in cadastros.values()]
    dict_icons = {
        "CHUVA EXCESSIVA":"water_drop",
        "GEADA":"ac_unit",
        "GRANIZO":"cloudy_snowing",
        "SECA":"sunny",
        "VENDAVAL":"air",
        "RAIO":"bolt",
        } 
    for cadastro in dict_cadastros:
        cadastro['data_colheita'] = cadastro['data_colheita'].strftime("%d/%m/%Y")
        temp_cpf = cadastro["cpf_produtor"]
        cadastro['cpf_produtor'] = '{}.{}.{}-{}'.format(temp_cpf[:3], temp_cpf[3:6], temp_cpf[6:9], temp_cpf[9:])
        cadastro['evento'] = dict_icons[cadastro['evento']]
    return dict_cadastros
        
def listar_cadastros(request):

    cadastros = Cadastro.objects.all().order_by('-data_colheita')
    lista_cadastros_todos = criar_lista_cadastros(cadastros)
    
    if request.method == 'POST':
        cpf = request.POST.get("cpf_search","").replace(".","").replace("-","")
        cadastros = Cadastro.objects.all().filter(cpf_produtor = cpf).order_by('-data_colheita')
        if len(cadastros) == 0:
            return render(request, 'proagro_app/listar_cadastros.html', {'modal_msg':"Nenhum cadastro para esse CPF",'cadastros':lista_cadastros_todos})
            
        lista_cadastros = criar_lista_cadastros(cadastros)
        return render(request, 'proagro_app/listar_cadastros.html', {'cadastros':lista_cadastros})
    
        # cadastro['data_colheita'] = datetime.strptime(v,"%Y-%m-%d")

    return render(request, 'proagro_app/listar_cadastros.html', {'cadastros':lista_cadastros_todos})

def editar_cadastro(request, pk):
    
    cadastro = Cadastro.objects.get(pk = pk)
    cadastro_dict = cadastro.__dict__


    cadastro_dict['data_colheita'] = cadastro_dict['data_colheita'].strftime("%Y-%m-%d")
    temp_cpf = cadastro_dict['cpf_produtor']
    cadastro_dict['cpf_produtor'] = '{}.{}.{}-{}'.format(temp_cpf[:3], temp_cpf[3:6], temp_cpf[6:9], temp_cpf[9:])
    # cadastro_dict['evento'] = dict_icons[cadastro_dict['evento']]
    
    
    if request.method == 'POST':
        print(request)
        dict_form = {'cpf_produtor':cadastro_dict['cpf_produtor']}
        for key, value in request.POST.items():
            '''Verifica se o input possui algum valor vazio. Esse verificação já é feita no front, mas por garantia tambem está sendo feita no backend.'''
            if value != "":
                dict_form[key] = value
            else:
                return render(request, 'proagro_app/editar_cadastro.html',{'cadastro':cadastro_dict,'modal_msg':"Todos os campos precisam ser preenchidos!"})
            
        '''Realiza o tratamento de valores, caso resulte em erro, o programa avisa o usuario.'''   
        try:
            dict_form_validado = DictCadastro(**dict_form)
        except ValidationError as e:
            return render(request, 'proagro_app/editar_cadastro.html',{'cadastro':cadastro_dict, 'modal_msg':e})
        
        try:
            cadastro.nome_produtor = dict_form_validado.nome_produtor
            cadastro.cpf_produtor = dict_form_validado.cpf_produtor
            cadastro.email_produtor = dict_form_validado.email_produtor
            cadastro.lat_lavoura = dict_form_validado.lat_lavoura
            cadastro.long_lavoura = dict_form_validado.long_lavoura
            cadastro.tipo_lavoura = dict_form_validado.tipo_lavoura
            cadastro.data_colheita = dict_form_validado.data_colheita
            cadastro.evento = dict_form_validado.evento
            cadastro.status = dict_form_validado.status
            cadastro.id_analista = 1
            cadastro.save()    
            return render(request, 'proagro_app/index.html',{'modal_msg':"Cadastro editado com sucesso!"})
        except Exception as e:
            return render(request, 'proagro_app/index.html',{'modal_msg':e})
            # return render(request, 'proagro_app/editar_cadastro.html',{'modal_msg':e})
        

    
    return render(request, 'proagro_app/editar_cadastro.html', {'cadastro':cadastro_dict})

def excluir_cadastro(request, pk):
    try:
        Cadastro.objects.get(pk = pk).delete()
    except:
        pass
    
    return redirect("view_proagro:listar_cadastros")


def home(request):
    return render(request, 'proagro_app/index.html')



