# Importing Modules
######################
import datetime as dt
import requests
import pandas as pd
import smtplib
import matplotlib.pyplot as plt
import os
import imghdr
from email.message import EmailMessage

# Import recipient list
#######################
import recipient_list
recipient_list_to = recipient_list.recipients_to
recipient_list_cc = recipient_list.recipients_cc
recipient_list_bcc = recipient_list.recipients_bcc

# Variables Banxico
###################
token = os.environ.get("token_banxico")

# Clave de Descarga Banxico
fix = "SF63528"  # Fecha de Determinacion (FIX)
obligaciones = "SF60653"  # Para Solventar Obligaciones

# Fechas
########
# Fecha actual
today = dt.date.today()  # - dt.timedelta(21)  ## Para pruebas
print("Today is = " + str(today))

# Primer dia del mes
first_day = today.replace(day=1)
print("The first day of this month is = " + str(first_day))

# Dia de la semana
week_day = today.weekday()
print("Today is day number: " + str(week_day) + "\n(Date range is 0 to 6)")


# Funcion de Descarga de datos de Banxico
#########################################
def descarga_bmx_serie(serie, fechainicio, fechafin, token):
    try:
        # Al site de banxico se le pegan los datos de consulta
        url = (
               "https://www.banxico.org.mx/SieAPIRest/service/v1/series/"
               + serie
               + "/datos/"
               + fechainicio
               + "/"
               + fechafin
               )
        print(url)

        # Se le tienen que pasar Headers
        headers = {"Bmx-Token": token}
        # Se pasa el token de banxico en un diccionario.
        response = requests.get(url, headers=headers)
        # Se pasa como un request con metodo get
        status = response.status_code
        # Se le solicita el codigo de respuesta al servidor.
        if status == 200:
            # Si el estatus esta Ok armar el dataframe
            raw_data = response.json()
            # Se guarda la respuesta como una variable.
            data = raw_data["bmx"]["series"][0]["datos"]
            # Se filtra el json
            # Se accesa el diccionario con los datos
            global df
            # Hacemos que la variable global para poder accesarla despues
            df = pd.DataFrame(data)
            # Creamos un dataframe con la informacion
            df["dato"] = df["dato"].apply(lambda x: float(x))
            # Volvemos los datos floats en vez de strings
            df["fecha"] = pd.to_datetime(df["fecha"], format="%d/%m/%Y")
            # Volvemos las fechas a formato fecha
            df.columns = ["Fecha", "Tipo de Cambio"]
            # Cambia el nombre de la columna "dato"  por tipo de cambio
            print("A-Ok")
            return df
            # Regresa el dataframe
        else:
            # Si el estatus esta mal imprimir el error en la terminal.
            print(status)
    except Exception:
        print("An exception occurred")
        print(Exception)


# Descargando Tipo de Cambio: Obligaciones
##########################################
fx_obligaciones = descarga_bmx_serie(obligaciones,
                                     str(first_day),
                                     str(today),
                                     token)
df.set_index("Fecha", inplace=True)


# # Descargando Tipo de Cambio: FIX
###################################

# Para la fecha inicial, nos vamos 4 dias hacia atras.
# Por si la busqueda se ejecuta el primer dia de mes y cae en fin de semana.
fx_fix = descarga_bmx_serie(fix,
                            str(first_day - dt.timedelta(4)),
                            str(today),
                            token)
df.set_index("Fecha", inplace=True)


# Creando el Dataframe para FX Obligaciones Futuras
####################################################

# Create an empty dataframe with column names
fx_obligaciones_f = pd.DataFrame(columns=["Fecha", "Tipo de Cambio"])

# Volver los valores de fecha un datetime y no un string
datetime_series = pd.to_datetime(fx_obligaciones_f["Fecha"])
datetime_series = pd.to_datetime(fx_obligaciones_f["Fecha"])
datetime_index = pd.DatetimeIndex(datetime_series.values)
fx_obligaciones_f = (fx_obligaciones_f
                     .set_index(datetime_index)
                     .rename_axis("Fecha", axis=1)
                     )
fx_obligaciones_f.drop("Fecha", axis=1, inplace=True)


# Sacando el FX Obligaciones de los proximos dias
#################################################
# Fechas Futuras
day_plus1 = today + dt.timedelta(1)
day_plus2 = today + dt.timedelta(2)
day_plus3 = today + dt.timedelta(3)
day_plus4 = today + dt.timedelta(4)

if week_day == 4:
    # Codigo si fecha cae en viernes
    ################################
    # Valores de tipo de cambio Fix a añadir
    fx_fix_1d = fx_fix["Tipo de Cambio"].iloc[-1]  # Fix ayer
    fx_fix_2d = fx_fix["Tipo de Cambio"].iloc[-2]  # Fix antier

    fx_obligaciones_plus1 = {"Tipo de Cambio": fx_fix_2d}
    fx_obligaciones_plus2 = {"Tipo de Cambio": fx_fix_2d}
    fx_obligaciones_plus3 = {"Tipo de Cambio": fx_fix_2d}
    fx_obligaciones_plus4 = {"Tipo de Cambio": fx_fix_1d}

    # Create a new dataframe with these rows
    fx_obligaciones_f = fx_obligaciones_f.append(
        pd.DataFrame(fx_obligaciones_plus1, index=[day_plus1])
    )
    fx_obligaciones_f = fx_obligaciones_f.append(
        pd.DataFrame(fx_obligaciones_plus2, index=[day_plus2])
    )
    fx_obligaciones_f = fx_obligaciones_f.append(
        pd.DataFrame(fx_obligaciones_plus3, index=[day_plus3])
    )
    fx_obligaciones_f = fx_obligaciones_f.append(
        pd.DataFrame(fx_obligaciones_plus4, index=[day_plus4])
    )

    # Transform dates to datetime format
    fx_obligaciones_f.index = pd.to_datetime(fx_obligaciones_f.index)

elif week_day == 5:
    # Codigo si fecha cae en Sabado
    ###############################
    # Valores de tipo de cambio Fix a añadir
    fx_fix_1d = fx_fix["Tipo de Cambio"].iloc[-1]  # Fix ayer
    fx_fix_2d = fx_fix["Tipo de Cambio"].iloc[-2]  # Fix antier

    fx_obligaciones_plus1 = {"Tipo de Cambio": fx_fix_2d}
    fx_obligaciones_plus2 = {"Tipo de Cambio": fx_fix_2d}
    fx_obligaciones_plus3 = {"Tipo de Cambio": fx_fix_1d}

    # Create a new dataframe with these rows
    fx_obligaciones_f = fx_obligaciones_f.append(
        pd.DataFrame(fx_obligaciones_plus1, index=[day_plus1])
    )
    fx_obligaciones_f = fx_obligaciones_f.append(
        pd.DataFrame(fx_obligaciones_plus2, index=[day_plus2])
    )
    fx_obligaciones_f = fx_obligaciones_f.append(
        pd.DataFrame(fx_obligaciones_plus3, index=[day_plus3])
    )

    # Transform dates to datetime format
    fx_obligaciones_f.index = pd.to_datetime(fx_obligaciones_f.index)

else:
    # Codigo si fecha cae en Lunes-Jueves o Domingo
    ###############################################
    # Valores de tipo de cambio Fix a añadir
    fx_fix_1d = fx_fix["Tipo de Cambio"].iloc[-1]  # Fix ayer
    fx_fix_2d = fx_fix["Tipo de Cambio"].iloc[-2]  # Fix antier

    fx_obligaciones_plus1 = {"Tipo de Cambio": fx_fix_2d}
    fx_obligaciones_plus2 = {"Tipo de Cambio": fx_fix_1d}

    # Añadir valores al dataframe fx_obligaciones_f
    fx_obligaciones_f = fx_obligaciones_f.append(
        pd.DataFrame(fx_obligaciones_plus1, index=[day_plus1])
    )
    fx_obligaciones_f = fx_obligaciones_f.append(
        pd.DataFrame(fx_obligaciones_plus2, index=[day_plus2])
    )

    # Transformar valores a datetime
    fx_obligaciones_f.index = pd.to_datetime(fx_obligaciones_f.index)


# Juntando Fx Obligaciones con Fx Obligaciones Futuras
######################################################
# Juntar fx_obligaciones y fx_obligaciones_f
fx_join = pd.concat([fx_obligaciones, fx_obligaciones_f], axis=0)

# Creando la grafica
#####################
# Creating a Figure (empty canvas)
fig = plt.figure(figsize=(10, 3))

# Adding a set of axes to the figure
axes = fig.add_axes([0.0,  # left
                     0.0,  # bottom
                     0.9,  # width
                     0.9]  # height
                    )  # (range 0 to 1)

# Ploting on that set of axes
axes.plot(
          fx_join["Tipo de Cambio"],
          color="red",
          linewidth=1.5,
          label="FX Obligaciones",
          marker="o",
          markersize=4,
          markerfacecolor="red",
          markeredgewidth=2,
          markeredgecolor="red",
          )
axes.set_xlabel("Fecha")
axes.set_ylabel("Tipo de Cambio: $ MXN / USD")
axes.set_ylim(auto=bool)
axes.grid(bool, which="major", axis="y")
axes.set_title("Tipo de Cambio para Solventar Obligaciones",
               fontweight="bold",
               pad=20)
axes.legend(loc=0)

# Guardando la imagen
fig.savefig("TipoDeCambio.png", bbox_inches="tight", dpi=300)


# Calculando la Ganancia o Perdida Cambiaria
###############################################
fx_inicial = fx_join["Tipo de Cambio"].values[0]
print("El tipo de cambio a inicio de mes fue de: $" + str(fx_inicial))

fx_final = fx_join["Tipo de Cambio"].values[-1]
print("El tipo de cambio a la fecha es de: $" + str(fx_final))

cambio_fx = ((fx_final / fx_inicial) - 1) * 100
cambio_fx_redondeado = round(cambio_fx, 2)

print(("La diferencia cambiaria a la fecha es de: "
       + str(cambio_fx_redondeado)
       + "%")
      )


# Analisis de conveniencia usando Threshold
############################################
cambio_fx_absoluto = abs(cambio_fx_redondeado)
# Threshold de porcentaje de cambio de FX para comprar SHV
threshold = 0.00  # --> Expresar porcentaje como decimal
print("Threshold: " + str(threshold * 100) + "%")

comprar_SHV = "Se podría comprar SHV para reducir la ganancia cambiaria."
vender_SHV = "Se podría vender SHV para aprovechar la perdida cambiaria."
no_hacer_nada = "La diferencia es demasiado pequeña."

if cambio_fx_absoluto > threshold * 100:
    if cambio_fx > 0:
        analisis = comprar_SHV
    else:
        analisis = vender_SHV
else:
    analisis = no_hacer_nada
print(analisis)

# Creando el Email
##################
email_body = (
    "Hola,"
    "\n\nEste es el análisis de tipo de cambio a la fecha:"
    "\n    - El tipo de cambio a inicio de mes fue de: $"
    + str(fx_inicial)
    + "\n    - El tipo de cambio a la fecha es de: $"
    + str(fx_final)
    + "\n    - La diferencia cambiaria a la fecha es de: "
    + str(cambio_fx_redondeado)
    + "%\n"
    "\n" + str(analisis) + "\n"
    "\nAnexo el detalle del tipo de cambio para solventar obligaciones.\n\n"
    + fx_join.to_string(index=True)
    + "\n\nSaludos,"
    "\n\nPablo."
)

print(email_body)

# Enviando el Email
###################
email_address = os.environ.get("email_username")
email_password = os.environ.get("email_password")
email_from = os.environ.get("email_username")
email_smtp = os.environ.get("email_smtp_address")

# Lista de Recipients
# Usar comas entre "" cuando se usan multiples direcciones o attachments.
recipients_to = [recipient_list_to]
recipients_cc = [recipient_list_cc]
recipients_bcc = [recipient_list_bcc]
attachments = ["TipoDeCambio.png"]
subject = "Análisis de Tipo de Cambio"

# Email Address Object
msg = EmailMessage()

# Email Address Template
msg["From"] = email_from
msg["To"] = recipient_list_to
msg["Cc"] = recipient_list_cc
msg["Bcc"] = recipient_list_bcc
msg["Subject"] = subject
msg.set_content(email_body)

# Adding Email attachments:
for file in attachments:
    with open(file, "rb") as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name
    msg.add_attachment(
        file_data, maintype="image", subtype=file_type, filename=file_name
    )

# Sending the Email
# Usar("smtp.gmail.com", 465) si se envía desde gmail.
with smtplib.SMTP_SSL(email_smtp, 465) as smtp:
    smtp.login(email_address, email_password)
    smtp.send_message(msg)
    print("Email Sent")
    print(today)
