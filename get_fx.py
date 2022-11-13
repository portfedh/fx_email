# Script to get the official FX USD:MXN from Banxico
# Can get FIX or Obligaciones

import os
import requests
import pandas as pd

class GetFx():

    def __init__(self):
        self.token = os.environ.get("token_banxico")

    def get_dates(self):
        print("\nBusqueda de FX para Solventar Obligaciones: \n")
        self.fecha_inicial = str(input("Fecha Inicial de Busqueda yyyy-mm-dd: "))
        self.fecha_final = str(input("Fecha Final de Busqueda yyyy-mm-dd: "))
    
    def get_series(self):
        while True:
            self.series = str(input("Definir serie de datos (fix, obligaciones): "))
            if self.series == 'fix':
                self.series = "SF63528"
                break
            elif self.series == 'obligaciones':
                self.series = "SF60653"
                break
            else:
                print('Error en seleccion. Intenta de nuevo.')

    def get_data(self, series, fechainicio, fechafin):
        url = (
            "https://www.banxico.org.mx/SieAPIRest/service/v1/series/"
            + series
            + "/datos/"
            + fechainicio
            + "/"
            + fechafin
            )
        # Se crea un diccionarion con el token del API
        headers = {"Bmx-Token": self.token}
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
            print(status)

    def print_output(self):
        print("\n")
        print(self.df.to_string(index=False))
        print("\n")


if __name__ == '__main__':
    oGetFx = GetFx()
    oGetFx.get_dates()
    oGetFx.get_series()
    oGetFx.get_data(
        series=oGetFx.series,
        fechainicio=oGetFx.fecha_inicial,
        fechafin=oGetFx.fecha_final,
    )
    oGetFx.print_output()
