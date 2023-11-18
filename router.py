from flask import Flask 
from flask import request
from ML import ml 
import json 
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route("/")
def home(name = None):
    resultado = ml.obtenerML()
    resultado = resultado.to_json(orient="index")
    resultado = json.loads(resultado)
    return resultado
    

@app.route("/buscar/<habitaciones>/<parqueadero>/<banos>/<sector>/<area>/<tipoAcabados>", methods=["POST"])
def buscar(habitaciones, parqueadero, banos, sector, area, tipoAcabados):
    """
        habitaciones => 2/3/4/1
        parqueadero => 1/2/3/4/5
        tipoAcabados => 800(Gama alta)/ 400(gama media)/ 300(economico)
        sector => [...]
    """

    if(request.method == "POST"):
        try:
         
            tipo = ''
            if(int(tipoAcabados) == 800):
                tipo = '3'
            elif(int(tipoAcabados) == 400):
                tipo = '2'
            elif(int(tipoAcabados) == 300):
                tipo = '1'
        

            resultado = ml.entradas([
                {
                    'habitaciones' : habitaciones,
                    'parqueadero' : parqueadero,
                    'banos' : banos,
                    'sector' : sector,  
                    'area' : area, 
                    'tipoAcabados' : tipo,
                    'acabados' : tipoAcabados
                }
            ])

            if(resultado):
                resultado = ml.ML()

                return json.dumps(resultado)
            

        except AttributeError:
            return resultado


    return "[!] ATENCION: Debes usarlo con metodo POST" 




