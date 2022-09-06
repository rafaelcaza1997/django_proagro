from datetime import datetime
from typing import Union
from pydantic import BaseModel, ValidationError, validator

class DictCadastro(BaseModel):    
    nome_produtor: str
    email_produtor: str
    cpf_produtor: str
    lat_lavoura: str
    long_lavoura: str
    tipo_lavoura: str
    data_colheita: Union[str, datetime]
    evento: str
    status: str
    
    @validator('cpf_produtor')
    def cpf_validation_(cls, v):
        v = v.replace(".","").replace("-","")
        if len(v) != 11:
            raise ValueError('CPF invalido')
        return v
    
    @validator('lat_lavoura')
    def lat_conv_num(cls, v):
        v = v.replace(",","")
        try:
            v = float(v)
        except:
            raise ValueError('Latitude precisa ser um valor numerico. (00.00)')
        if v > 90 or v < -90:
            raise ValueError('Latitude precisa ser um valor numerico entre 90 e -90.')
        return v
    
    @validator('long_lavoura')
    def lon_conv_num(cls, v):
        v = v.replace(",","")
        try:
            v = float(v)
        except:
            raise ValueError('Longitude precisa ser um valor numerico. (00.00)')
        if v > 90 or v < -90:
            raise ValueError('Longitude precisa ser um valor numerico entre 90 e -90.')
        return v
    
    @validator('data_colheita')
    def datetime_validador(cls, v):
        if type(v) != datetime:
            try:
                v = datetime.strptime(v,"%Y-%m-%d")
            except:
                raise ValueError('Data invalida, é esperado um formato datetime ou str(YYYY-mm-dd)')
        return v


    