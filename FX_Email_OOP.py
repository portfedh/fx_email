# Imports
#########
import datetime as dt
import get_fx


class SendFxEmail():

    def __init__(self):
        self.get_dates()
        self.debugg_prints()

    def get_dates(self):
        self.today = dt.date.today()  # - dt.timedelta(21)  ## Para pruebas
        self.first_day = self.today.replace(day=1)
        self.week_day = self.today.weekday()

    def get_fx_obligaciones(self):
        self.oFxObligaciones = GetFx()
        self.oFxObligaciones.get_data(
            self.oFxObligaciones.obligaciones,
            self.first_day,
            self.today,
            self.oFxObligaciones.api_token)
        self.oFxObligaciones.print_output()

    def get_fx_fix(self):
        pass

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
        print("Today is = " + str(self.today))
        print("First day of this month is = " + str(self.first_day))
        print("Today is day number: " + str(self.week_day) + "\n(Date range is 0 to 6)")


if __name__ == '__main__':

    oSendMail = SendFxEmail()