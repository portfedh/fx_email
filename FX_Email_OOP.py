# Imports
#########
import get_fx
import pandas as pd
import datetime as dt
import send_email as se
import matplotlib.pyplot as plt


class SendFxEmail():

    def __init__(self):
        self.get_dates()
        self.get_fx_obligaciones()
        self.get_fx_fix()
        self.calculate_future_fx()
        self.concat_df()
        self.create_graph()
        self.debugg_prints()
        self.calculate_gainloss()
        self.decide_what_to_do()
        self.build_body()
        self.send_email()

    def get_dates(self):
        self.today = dt.date.today()  # - dt.timedelta(21)  ## Para pruebas
        self.first_day = self.today.replace(day=1)
        self.week_day = self.today.weekday()  # Date range is 0-6
        self.day_plus1 = self.today + dt.timedelta(1)
        self.day_plus2 = self.today + dt.timedelta(2)
        self.day_plus3 = self.today + dt.timedelta(3)
        self.day_plus4 = self.today + dt.timedelta(4)

    def get_fx_obligaciones(self):
        self.fx_obligaciones = get_fx.GetFx()
        self.fx_obligaciones.get_data(
            series="SF60653",
            fechainicio=str(self.first_day),
            fechafin=str(self.today),
        )
        self.fx_obligaciones.index_datetime()

    def get_fx_fix(self):
        self.fx_fix = get_fx.GetFx()
        self.fx_fix.get_data(
            series="SF63528",
            fechainicio=str(self.first_day),
            fechafin=str(self.today),
        )
        self.fx_fix.index_datetime()
    
    def calculate_future_fx(self):
        # Assign Fix values
        self.fx_fix_1d = self.fx_fix.df["Tipo de Cambio"].iloc[-1]  # Fix yesterday
        self.fx_fix_2d = self.fx_fix.df["Tipo de Cambio"].iloc[-2]  # Fix 2 days ago
        # Check if today is Friday
        if self.week_day == 4:
            print('Today is Friday')
            self.calculate_f_fx_friday()
        # Check if today is Saturday
        elif self.week_day == 5:
            print('Today is Saturday')
            self.calculate_f_fx_saturday()
        # Day is Monday-Thursday or Sunday
        else:
            print('Today is Monday-Thursday or Sunday')
            self.calculate_f_fx_other_days()

    def calculate_f_fx_friday(self):
        # Create an empty dataframe with column names
        self.fx_obligaciones_f = pd.DataFrame(columns=["Fecha", "Tipo de Cambio"])
        # Assign future values
        self.fx_obligaciones_plus1 = {"Fecha": self.day_plus1, "Tipo de Cambio": self.fx_fix_2d}
        self.fx_obligaciones_plus2 = {"Fecha": self.day_plus2, "Tipo de Cambio": self.fx_fix_2d}
        self.fx_obligaciones_plus3 = {"Fecha": self.day_plus3, "Tipo de Cambio": self.fx_fix_2d}
        self.fx_obligaciones_plus4 = {"Fecha": self.day_plus4, "Tipo de Cambio": self.fx_fix_1d}
        # Append rows
        self.fx_obligaciones_f = pd.concat([self.fx_obligaciones_f, pd.DataFrame(self.fx_obligaciones_plus1, index=[self.day_plus1])])
        self.fx_obligaciones_f = pd.concat([self.fx_obligaciones_f, pd.DataFrame(self.fx_obligaciones_plus2, index=[self.day_plus2])])
        self.fx_obligaciones_f = pd.concat([self.fx_obligaciones_f, pd.DataFrame(self.fx_obligaciones_plus3, index=[self.day_plus3])])
        # Transform dates to datetime format
        self.fx_obligaciones_f.index = pd.to_datetime(self.fx_obligaciones_f.index)
        self.datetime_series = pd.to_datetime(self.fx_obligaciones_f["Fecha"])
        self.datetime_index = pd.DatetimeIndex(self.datetime_series.values)
        self.fx_obligaciones_f = (self.fx_obligaciones_f
                            .set_index(self.datetime_index)
                            .rename_axis("Fecha", axis=1)
                            )
        self.fx_obligaciones_f.drop("Fecha", axis=1, inplace=True)

    def calculate_f_fx_saturday(self):
        # Create an empty dataframe with column names
        self.fx_obligaciones_f = pd.DataFrame(columns=["Fecha", "Tipo de Cambio"])
        # Assign future values
        self.fx_obligaciones_plus1 = {"Fecha": self.day_plus1, "Tipo de Cambio": self.fx_fix_2d}
        self.fx_obligaciones_plus2 = {"Fecha": self.day_plus2, "Tipo de Cambio": self.fx_fix_2d}
        self. fx_obligaciones_plus3 = {"Fecha": self.day_plus3,"Tipo de Cambio": self.fx_fix_1d}
        # Append rows
        self.fx_obligaciones_f = pd.concat([self.fx_obligaciones_f, pd.DataFrame(self.fx_obligaciones_plus1, index=[self.day_plus1])])
        self.fx_obligaciones_f = pd.concat([self.fx_obligaciones_f, pd.DataFrame(self.fx_obligaciones_plus2, index=[self.day_plus2])])
        self.fx_obligaciones_f = pd.concat([self.fx_obligaciones_f, pd.DataFrame(self.fx_obligaciones_plus3, index=[self.day_plus3])])
        # Transform dates to datetime format
        self.fx_obligaciones_f.index = pd.to_datetime(self.fx_obligaciones_f.index)
        self.datetime_series = pd.to_datetime(self.fx_obligaciones_f["Fecha"])
        self.datetime_index = pd.DatetimeIndex(self.datetime_series.values)
        self.fx_obligaciones_f = (self.fx_obligaciones_f
                            .set_index(self.datetime_index)
                            .rename_axis("Fecha", axis=1)
                            )
        self.fx_obligaciones_f.drop("Fecha", axis=1, inplace=True)

    def calculate_f_fx_other_days(self):
        # Create an empty dataframe with column names
        self.fx_obligaciones_f = pd.DataFrame(columns=["Fecha", "Tipo de Cambio"])
        # Assign future values
        self.fx_obligaciones_plus1 = {"Fecha": self.day_plus1, "Tipo de Cambio": self.fx_fix_2d}
        self.fx_obligaciones_plus2 = {"Fecha": self.day_plus2, "Tipo de Cambio": self.fx_fix_1d}
        # Append rows
        self.fx_obligaciones_f = pd.concat([self.fx_obligaciones_f, pd.DataFrame(self.fx_obligaciones_plus1, index=[self.day_plus1])])
        self.fx_obligaciones_f = pd.concat([self.fx_obligaciones_f, pd.DataFrame(self.fx_obligaciones_plus2, index=[self.day_plus2])])
        # Transform dates to datetime format
        self.fx_obligaciones_f.index = pd.to_datetime(self.fx_obligaciones_f.index)
        self.datetime_series = pd.to_datetime(self.fx_obligaciones_f["Fecha"])
        self.datetime_index = pd.DatetimeIndex(self.datetime_series.values)
        self.fx_obligaciones_f = (self.fx_obligaciones_f
                            .set_index(self.datetime_index)
                            .rename_axis("Fecha", axis=1)
                            )
        self.fx_obligaciones_f.drop("Fecha", axis=1, inplace=True)

    def concat_df(self):
        self.fx_join = pd.concat([self.fx_obligaciones.df, self.fx_obligaciones_f], axis=0)

    def create_graph(self):
        # Creating a Figure (empty canvas)
        self.fig = plt.figure(figsize=(10, 3))

        # Adding a set of axes to the figure
        self.axes = self.fig.add_axes([
                            0.0,  # left
                            0.0,  # bottom
                            0.9,  # width
                            0.9   # height
                            ]) # (range 0 to 1)

        # Ploting on that set of axes
        self.axes.plot(
                self.fx_join["Tipo de Cambio"],
                color="red",
                linewidth=1.5,
                label="FX Obligaciones",
                marker="o",
                markersize=3,
                markerfacecolor="red",
                markeredgewidth=2,
                markeredgecolor="red",
                )
        self.axes.set_xlabel("Fecha")
        self.axes.set_ylabel("Tipo de Cambio: $ MXN / USD")
        self.axes.set_ylim(auto=bool)  # bottom=0, top=30)
        self.axes.grid(bool, which="major", axis="y")
        self.axes.set_title("Tipo de Cambio para Solventar Obligaciones",
                    fontweight="bold",
                    pad=20)
        self.axes.legend(loc=0)

        # Guardando la imagen
        self.fig.savefig("TipoDeCambio.png", bbox_inches="tight", dpi=300)

    def calculate_gainloss(self):
        # Start of month
        self.fx_inicial = self.fx_join["Tipo de Cambio"].values[0]
        print("El tipo de cambio a inicio de mes fue de: $" + str(self.fx_inicial))
        # Current day
        self.fx_final = self.fx_join["Tipo de Cambio"].values[-1]
        print("El tipo de cambio a la fecha es de: $" + str(self.fx_final))
        # Change in FX
        self.cambio_fx = ((self.fx_final / self.fx_inicial) - 1) * 100
        self.cambio_fx_redondeado = round(self.cambio_fx, 2)
        print(("La diferencia cambiaria a la fecha es de: "
            + str(self.cambio_fx_redondeado)
            + "%"
            ))

    def decide_what_to_do(self):
        self.cambio_fx_absoluto = abs(self.cambio_fx_redondeado)
        # Threshold de porcentaje de cambio de FX para comprar SHV
        self.threshold = 0.00  # --> Expresar porcentaje como decimal
        print("Threshold: " + str(self.threshold * 100) + "%")

        self.comprar_SHV = "Se podría comprar SHV para reducir la ganancia cambiaria."
        self.vender_SHV = "Se podría vender SHV para aprovechar la perdida cambiaria."
        self.no_hacer_nada = "La diferencia es demasiado pequeña."

        if self.cambio_fx_absoluto > self.threshold * 100:
            if self.cambio_fx > 0:
                self.analisis = self.comprar_SHV
            else:
                self.analisis = self.vender_SHV
        else:
            self.analisis = self.no_hacer_nada
        print(self.analisis)

    def build_body(self):
        self.email_body = (
            "Hola,"
            "\n\nEste es el análisis de tipo de cambio a la fecha:"
            "\n    - El tipo de cambio a inicio de mes fue de: $"
            + str(self.fx_inicial)
            + "\n    - El tipo de cambio a la fecha es de: $"
            + str(self.fx_final)
            + "\n    - La diferencia cambiaria a la fecha es de: "
            + str(self.cambio_fx_redondeado)
            + "%\n"
            "\n" + str(self.analisis) + "\n"
            "\nAnexo el detalle del tipo de cambio para solventar obligaciones.\n\n"
            + self.fx_join.to_string(index=True)
            + "\n\nSaludos,"
            "\n\nPablo."
        )

    def send_email(self):
        self.email = se.SendEmail()
        self.email.email_content(
            to="portfedh@gmail.com",
            cc="pablo.cruz@gmail.com",
            subject="Análisis de Tipo de Cambio",
            body=self.email_body
            )
        self.email.add_attachments(["TipoDeCambio.png"])
        self.email.send_mail()

    def debugg_prints(self):
        # get_dates()
        print("Dates in YYYY-MM-DD format.")
        print("Today is: " + str(self.today))
        print("First day of this month is: " + str(self.first_day))
        print("Today is day number: " + str(self.week_day) + " (Date range is 0 to 6)\n")
        # get_fx_obligaciones()
        print("Obligaciones df:")
        self.fx_obligaciones.print_output(with_index=True)
        # get_fx_fix()
        print("Fix df:")
        self.fx_fix.print_output(with_index=True)
        # create_future_fx_df() / calculate_future_fx()
        print("Future Obligaciones df:")
        print(str(self.fx_obligaciones_f))

        # concat_df()
        print("\n Merged Obligaciones df:")
        print(str(self.fx_join))


if __name__ == '__main__':
    oSendMail = SendFxEmail()