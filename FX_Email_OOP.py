# Imports
#########
import datetime as dt
import get_fx


class SendFxEmail():

    def __init__(self):
        self.get_dates()
        self.get_fx_obligaciones()
        self.get_fx_fix()
        self.debugg_prints()

    def get_dates(self):
        self.today = dt.date.today()  # - dt.timedelta(21)  ## Para pruebas
        self.first_day = self.today.replace(day=1)
        self.week_day = self.today.weekday()

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

    def calculate_fx_futuro(self):
        pass

    def create_graph(self):
        pass

    def calculate_gainloss(self):
        pass

    def decide_what_to_do(self):
        pass

    def send_email(self):
        pass

    def debugg_prints(self):
        # Get_dates()
        print("Dates in YYYY-MM-DD format.")
        print("Today is:= " + str(self.today))
        print("First day of this month is = " + str(self.first_day))
        print("Today is day number: " + str(self.week_day) + "\n(Date range is 0 to 6)")
        print("Date range is 0 to 6")
        # get_fx_obligaciones()
        self.fx_obligaciones.print_output()
        self.fx_fix.print_output()


if __name__ == '__main__':
    oSendMail = SendFxEmail()