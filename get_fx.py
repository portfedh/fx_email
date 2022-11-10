# Programa para mostrar el tipo de cambio MXN:USD
# Para un periodo de fechas.
# Autor: Pablo Cruz Lemini

# Changes: 
# Class name to GetFx()
# Add fix series

import os
import requests
import pandas as pd

class GetFx():
    api_token = os.environ.get("token_banxico")
    obligaciones = "SF60653"
    fix = "SF63528"
    www = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/"

    def __init__(self):
        pass

    def get_dates(self):
        print("\nBusqueda de FX para Solventar Obligaciones: \n")
        self.fecha_inicial = str(input("Fecha Inicial de Busqueda yyyy-mm-dd: "))
        self.fecha_final = str(input("Fecha Final de Busqueda yyyy-mm-dd: "))

    def get_data(self, serie, fechainicio, fechafin, token):
        url = (GetFxTerminal.www
            + serie
            + "/datos/"
            + fechainicio
            + "/"
            + fechafin
            )
        # Se crea un diccionarion con el token del API
        headers = {"Bmx-Token": token}
        # Hacer un GET request a la pagina del API
        response = requests.get(url, headers=headers)
        # Revisar el codigo de respuesta
        status = response.status_code
        # Si el estatus esta OK:
        if status == 200:
            # Crear un objeto json
            raw_data = response.json()
            # Accesar los datos dentro del objeto json
            data = raw_data["bmx"]["series"][0]["datos"]
            # Creamos un dataframe con los datos
            self.df = pd.DataFrame(data)
            # Transformamos los datos de strings a floats
            self.df["dato"] = self.df["dato"].apply(lambda x: float(x))
            # Transformamos las fechas de strings a datetime
            self.df["fecha"] = pd.to_datetime(self.df["fecha"], format="%d/%m/%Y")
            # Renombramos las columnas
            self.df.columns = ['Fecha', 'Tipo de Cambio']
            return self.df
        # Si el estatus tiene error:
        else:
            # Imprimir el error
            print(status)

    def print_output(self):
        print("\n")
        print(self.df.to_string(index=False))
        print("\n")


if __name__ == '__main__':
    oGetFx = GetFx()
    oGetFx.get_dates()
    oGetFx.get_data(
        GetFx.obligaciones,
        oGetFx.fecha_inicial,
        oGetFx.fecha_final,
        GetFx.api_token
        )
    oGetFx.print_output()

