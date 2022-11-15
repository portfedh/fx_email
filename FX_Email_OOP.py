# Imports
#########
import get_fx
import pandas as pd
import datetime as dt


class SendFxEmail():

    def __init__(self):
        self.get_dates()
        self.get_fx_obligaciones()
        self.get_fx_fix()
        self.create_future_fx_df()
        self.calculate_future_fx()
        self.debugg_prints()

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

    def get_fx_fix(self):
        self.fx_fix = get_fx.GetFx()
        self.fx_fix.get_data(
            series="SF63528",
            fechainicio=str(self.first_day),
            fechafin=str(self.today),
        )

    def create_future_fx_df(self):
        # Create an empty dataframe with column names
        self.fx_obligaciones_f = pd.DataFrame(columns=["Fecha", "Tipo de Cambio"])

        # Volver los valores de fecha un datetime y no un string
        self.datetime_series = pd.to_datetime(self.fx_obligaciones_f["Fecha"])
        self.datetime_index = pd.DatetimeIndex(self.datetime_series.values)
        self.fx_obligaciones_f = (self.fx_obligaciones_f
                            .set_index(self.datetime_index)
                            .rename_axis("Fecha", axis=1)
                            )
        self.fx_obligaciones_f.drop("Fecha", axis=1, inplace=True)
    
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
        # Assign future values
        self.fx_obligaciones_plus1 = {"Tipo de Cambio": self.fx_fix_2d}
        self.fx_obligaciones_plus2 = {"Tipo de Cambio": self.fx_fix_2d}
        self.fx_obligaciones_plus3 = {"Tipo de Cambio": self.fx_fix_2d}
        self.fx_obligaciones_plus4 = {"Tipo de Cambio": self.fx_fix_1d}
        # Create a new dataframe and append rows
        self.fx_obligaciones_f = self.fx_obligaciones_f.append(
            pd.DataFrame(self.fx_obligaciones_plus1, index=[self.day_plus1])
        )
        self.fx_obligaciones_f = self.fx_obligaciones_f.append(
            pd.DataFrame(self.fx_obligaciones_plus2, index=[self.day_plus2])
        )
        self.fx_obligaciones_f = self.fx_obligaciones_f.append(
            pd.DataFrame(self.fx_obligaciones_plus3, index=[self.day_plus3])
        )
        self.fx_obligaciones_f = self.fx_obligaciones_f.append(
            pd.DataFrame(self.fx_obligaciones_plus4, index=[self.day_plus4])
        )
        # Transform dates to datetime format
        self.fx_obligaciones_f.index = pd.to_datetime(self.fx_obligaciones_f.index)

    def calculate_f_fx_saturday(self):
        # Assign future values
        self.fx_obligaciones_plus1 = {"Tipo de Cambio": self.fx_fix_2d}
        self.fx_obligaciones_plus2 = {"Tipo de Cambio": self.fx_fix_2d}
        self. fx_obligaciones_plus3 = {"Tipo de Cambio": self.fx_fix_1d}
        # Create a new dataframe with these rows
        self.fx_obligaciones_f = self.fx_obligaciones_f.append(
            pd.DataFrame(self.fx_obligaciones_plus1, index=[self.day_plus1])
        )
        self.fx_obligaciones_f = self.fx_obligaciones_f.append(
            pd.DataFrame(self.fx_obligaciones_plus2, index=[self.day_plus2])
        )
        self.fx_obligaciones_f = self.fx_obligaciones_f.append(
            pd.DataFrame(self.fx_obligaciones_plus3, index=[self.day_plus3])
        )
        # Transform dates to datetime format
        self.fx_obligaciones_f.index = pd.to_datetime(self.fx_obligaciones_f.index)

    def calculate_f_fx_other_days(self):
        # Assign future values
        self.fx_obligaciones_plus1 = {"Tipo de Cambio": self.fx_fix_2d}
        self.fx_obligaciones_plus2 = {"Tipo de Cambio": self.fx_fix_1d}
        # Create a new dataframe with these rows
        self.fx_obligaciones_f = self.fx_obligaciones_f.append(
            pd.DataFrame(self.fx_obligaciones_plus1, index=[self.day_plus1])
        )
        self.fx_obligaciones_f = self.fx_obligaciones_f.append(
            pd.DataFrame(self.fx_obligaciones_plus2, index=[self.day_plus2])
        )
        # Transform dates to datetime format
        self.fx_obligaciones_f.index = pd.to_datetime(self.fx_obligaciones_f.index)

    def create_graph(self):
        pass

    def calculate_gainloss(self):
        pass

    def decide_what_to_do(self):
        pass

    def send_email(self):
        pass

    def debugg_prints(self):
        # get_dates()
        print("Dates in YYYY-MM-DD format.")
        print("Today is:= " + str(self.today))
        print("First day of this month is = " + str(self.first_day))
        print("Today is day number: " + str(self.week_day) + "\n(Date range is 0 to 6)")
        print("Date range is 0 to 6")
        # get_fx_obligaciones()
        self.fx_obligaciones.print_output()
        # get_fx_fix()
        self.fx_fix.print_output()
        # create_future_fx_df()
        # calculate_future_fx()
        print(str(self.fx_obligaciones_f))
        # calculate_f_fx_friday()
        # calculate_f_fx_saturday()
        # calculate_f_fx_other_days()
        # print(self.fx_obligaciones_f)


if __name__ == '__main__':
    oSendMail = SendFxEmail()