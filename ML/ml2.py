import numpy as np
import pandas as pd
import re

from sklearn.linear_model import LinearRegression

informacion = {
    'habitaciones' : '4',
    'parqueadero' : '4',
    'banos' : '3',
    'sector' : '13',
    'area' : '1000', 
    'tipoAcabados' : '2',
    'acabados' : '400'
}

def ml():
    fichero = 'data.csv'
    data = pd.read_csv(fichero)
    limpiarData(data)

    #variables que el modelo usa para aprender.
    codigoSector = data["codigoSector"] #cada sector tiene un codigo, ejem. (Cumbaya = 1, Puembo = 2)....
    banos = data["banos"] #numero de banos.
    parqueadero = data["parqueadero"] #numero de parqueaderos
    acabados = data["acabados"] #el precio del acabado
    tipoAcabados = data["tipoAcabados"] # El codigo de la gama -> 3(gama alta) 2(gama media) 1(gama economica)
    area = data["area"] #area de la casa encontrado en el datasets.

    #nuestra variable a predecir
    precioCasa = data["precio"] #precio de la casa encontrado en el datasets.

    X = np.column_stack((codigoSector, banos, parqueadero, acabados, tipoAcabados, area))
    Y = precioCasa

    #el modelo se encarga ahora de aprender
    modelo = LinearRegression()
    modelo.fit(X, Y)

    #obtenemos los datos del usuario... 
    DatosUsuario = pd.DataFrame({
        "codigoSector" : [informacion['sector']],
        "banos" : [informacion['banos']],
        "parqueadero" : [informacion['parqueadero']],
        "acabados" : [informacion['acabados']],
        "tipoAcabados" : [informacion['tipoAcabados']],
        "area" : [informacion['area']]
    })

    #mandamos los datoa al modelo
    ModeloPredice = modelo.predict(DatosUsuario)

    print("{:,.0f}".format(ModeloPredice[0]))


def limpiarData(data):
    parqueadero = data["parqueadero"]
    ListadoParqueaderos = []
    
    for key,value in parqueadero.items():
        NParqueadero = int(value)
        ListadoParqueaderos.append(str(NParqueadero))

    data["parqueadero"] = ListadoParqueaderos

    data.parqueadero = pd.to_numeric(data.parqueadero, downcast='integer')    

ml()

