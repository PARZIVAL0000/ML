import numpy as np
import pandas as pd
import re

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

import matplotlib.pyplot as plt
import seaborn as sns

informacion = {
    'habitaciones' : '',
    'parqueadero' : '',
    'banos' : '',
    'sector' : '',
    'area' : '', 
    'tipoAcabados' : '',
    'acabados' : ''
}

fichero1 = 'ML/casas_venta.csv'

respuesta = [{
    "Cliente" : dict(), 
    "Modelo" : dict(), 
}]

precioSectores = []
def ML():
    #obtenidos los datos de nuestro formulario... ahora lo que tenemos que realizar a continuacion es el medio de prediccion..
    data = pd.read_csv(fichero1)
    data['codigoSector'] = 'nan'
    data = limpiar(data)    
    data = codigosPaises(data)
    
    #sacar precio de la parte no construida....
    verificarPrecioNoConstruido(data)
    #sacar acabados
    
    acabados = sacarAbacadosCasas(data)
    data['acabados'] = acabados 

    verificarAcabados(data)



    # Definir las características (X) y la variable objetivo (y)
    num_habitaciones = data['habitaciones']
    num_parqueaderos = data['parqueadero'] 
    num_banos = data['banos']
    num_codigoSector = data['codigoSector']
    num_area = data['area']
    num_acabados = data['acabados']
    num_tipoAcabados = data['tipoAcabados']

    X = np.column_stack((num_habitaciones, num_parqueaderos, num_banos, num_codigoSector, num_area, num_acabados, num_tipoAcabados))  # Características
    y = data['precio']  # Variable objetivo

    model = LinearRegression()
    model.fit(X, y)

    #habitaciones', 'banos', 'parqueadero', 'sector', 'area'
    new_data = pd.DataFrame({'habitaciones': [informacion["habitaciones"]], 'parqueadero': [informacion['parqueadero']], 'banos' : [informacion['banos']], 'codigoSector' : [informacion['sector']], 'area': [informacion['area']], 'acabados' : [informacion['acabados']], 'tipoAcabados' : [informacion['tipoAcabados']] })
    predicted_price = model.predict(new_data)
    # Realizar una predicción

    #======================================================
    #           RECOLECTAR INFORMACION RETORNO
    #======================================================
    informacion_modelo = {
        "precioModelo" : "{:,.0f}".format(predicted_price[0]),
    }

    respuesta[0]["Cliente"] = informacion
    respuesta[0]["Modelo"] = informacion_modelo

    return respuesta



def limpiar(data):    
    data.drop(['fecha'], axis=1, inplace=True)
    listado_sector = []
    listado_ciudad = []

    for s in data.sector:
        s = str(s).split(",")[0]
        listado_sector.append(s)

    for s2 in data.sector:
        s2 = str(s2).split(",")[-1]
        listado_ciudad.append(s2)

    data['sector'] = listado_sector
    #data['ciudad'] = listado_ciudad

    listado_precios = []
    listado_areas = []
    listado_habitaciones = []
    listado_banos = []
    for v in data.precio:
        v = str(v).replace('.', '')
        listado_precios.append(v)

    for j in data.area:
        j = str(j)
    
        if(j.find('m²') == -1 and j.find('estac.') == -1):
            listado_areas.append(j)
        else:
            pattern = r"^.estac\."

            if(re.search(pattern, j)):
                listado_areas.append('nan')
            else:
                signo = j[-2:]
                j = j.replace(signo, '')
                listado_areas.append(j)
       

    for h in data.habitaciones:
        h = str(h)
        pattern = r"^.+(baños|baño)$"
        if((not re.search(pattern, h)) and h.find('estac.') == -1):
            listado_habitaciones.append(h)
        else:
            listado_habitaciones.append('nan')

    for b in data.banos:
        b = str(b)
        if(b.find('estac.') == -1):
            listado_banos.append(b)
        else:
            listado_banos.append('nan')

    data.precio = listado_precios
    data.area = listado_areas
    data.habitaciones = listado_habitaciones
    data.banos = listado_banos

    resultado = data.loc[: , 'precio'] != 'nan'
    data = data.loc[resultado]

    resultado = data.loc[:, 'area'] != 'nan'
    data = data.loc[resultado]

    resultado = data.loc[:, 'habitaciones'] != 'nan'
    data = data.loc[resultado]

    resultado = data.loc[:, 'banos'] != 'nan'
    data = data.loc[resultado]

    data.precio = pd.to_numeric(data.precio, downcast='integer')
    data.area = pd.to_numeric(data.area, downcast='integer')
    data.habitaciones = pd.to_numeric(data.habitaciones, downcast='integer')
    data.banos = pd.to_numeric(data.banos, downcast='integer')

    return data



def verificarPrecioNoConstruido(data):
    lista = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    sector = None

    for i in lista:
        sector = imprimir_Sector(i) # 5 -> 

        r = data.loc[:, 'sector'] == sector
        resultado = data.loc[r]
        precioCasa = resultado['precio']
        m2Casa = resultado['area']

        m2Terreno = []
        for i,j in precioCasa.items():
            precio = float(j)
            precioM2 = int(m2Casa[i]) 
            
            precioBase = precio/precioM2
            precioBase = round(precioBase)
            #precioBase = "{:,.0f}".format(precioBase)
            #precioBase = precioBase.replace(",", ".")
            precioBase = str(precioBase)
            m2Terreno.append(precioBase)

        resultado['precioM2Base'] = m2Terreno
        
        resultado.precioM2Base = pd.to_numeric(resultado.precioM2Base, downcast='integer')
        
        precioPromedio = round(np.mean(resultado.precioM2Base))
        
        precioSectores.append(precioPromedio)

    #codigo de prueba (eliminar despues)

    
def sacarAbacadosCasas(data):
    parqueaderos = data["parqueadero"]
    codigo = data["codigoSector"]
    precioCasa = data["precio"]

    lista_acabados = []

    for key, value in codigo.items():
        indice = int(value)-1
        preciom2 = float(precioSectores[indice]) 
        m2ParqueaderoMinimo = 18
        parqueadero = int(parqueaderos[key])
        total = m2ParqueaderoMinimo * parqueadero

        b = total * preciom2
    
        y = float(precioCasa[key])

        x = informacion['area']
        
        acabados = (y - b)/int(x)
        acabados = round(acabados)

        #acabados = "{:,.0f}".format(acabados)
        #acabados = acabados.replace(",", ".")

        lista_acabados.append(acabados)

    return lista_acabados




def verificarAcabados(data):
    acabados = data['acabados'] 
    
    tipoAcabados = []
    for i in acabados: 
        acabado = float(i)

        if(acabado >= 800):
            tipoAcabados.append("3") #gama alta
        elif(acabado > 300 and acabado < 800):
            tipoAcabados.append("2") #gama media
        elif(acabado <= 300):
            tipoAcabados.append("1") #economico
        else:
            print("Diferente")

    data['tipoAcabados'] = tipoAcabados 



def imprimir_Sector(codigo):
    codigo = int(codigo)
    if(codigo == 1):
        return "Pomasqui"
    elif(codigo == 2):
        return "El Batán"
    elif(codigo == 3):
        return "Iñaquito Alto"
    elif(codigo == 4):
        return "San Carlos"
    elif(codigo == 5):
        return "Ponceano"
    elif(codigo == 6):
        return "La Luz"
    elif(codigo == 7):
        return "Ponceano"
    elif(codigo == 8):
        return "La Luz"
    elif(codigo == 9):
        return "Carcelén"
    elif(codigo == 10):
        return "Bellavista"
    elif(codigo == 11):
        return "González Suárez"
    elif(codigo == 12):
        return "Quito Tenis"
    elif(codigo == 13):
        return "Puembo"
    elif(codigo == 14):
        return "Cumbayá"
    

""" CODIGOS DE CADA UNO DE LOS PAISES....
    "1" : 'Pomasqui',
    "2" : 'El Batán',
    "3"  : 'Iñaquito Alto', 
    "4" : 'San Carlos',
    "5"  : 'Ponceano', 
    "6"  : 'La Luz', 
    "7"  : 'Carcelen', 
    "8"  : 'Ponceano',  
    "9"  : 'La Luz',
    "10"  : 'Carcelén', 
    "11" : "Bellavista",
    "12" : "Guápulo", 
    "13" : "González Suárez",
    "14" : "Quito Tenis", 
    "15" : "Puembo",
    "16" : "Cumbayá"
"""
def codigosPaises(data):
    listado = []
    for key,value in data["sector"].items():
        if(value == "Cumbayá"):
            listado.append('14')
        elif(value == "Puembo"):
            listado.append('13')
        elif(value == "Quito Tenis"):
            listado.append('12')
        elif(value == "González Suárez"):
            listado.append('11')
        elif(value == "Bellavista"):
            listado.append('10')
        elif(value == "Carcelén"):
            listado.append('9')
        elif(value == "La Luz"):
            listado.append('8')
        elif(value == "Ponceano"):
            listado.append('7')
        elif(value == "La Luz"):
            listado.append('6')
        elif(value == "Ponceano"):
            listado.append('5')
        elif(value == "San Carlos"):
            listado.append('4')
        elif(value == "Iñaquito Alto"):
            listado.append('3')
        elif(value == "El Batán"):
            listado.append('2')
        elif(value == "Pomasqui"):
            listado.append('1')
        else:
            listado.append('0')
   
    data['codigoSector'] = listado

    resultado = data.loc[:, 'codigoSector'] != '0'
    data = data.loc[resultado]

    data['codigoSector'] = pd.to_numeric(data.codigoSector, downcast='integer')

    return data 

def entradas(entradas = []):
    if (len(entradas) != 0):
        informacion['habitaciones'] = entradas[0]['habitaciones']
        informacion['parqueadero'] = entradas[0]['parqueadero']
        informacion['banos'] = entradas[0]['banos']
        informacion['sector'] = entradas[0]['sector']
        informacion['area'] = entradas[0]['area']
        informacion['tipoAcabados'] = entradas[0]['tipoAcabados']
        informacion['acabados'] = entradas[0]['acabados']
        return True 
    else:
        return False 


