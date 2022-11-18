import fx_email

object_1 = fx_email.SendFxEmail()
object_1.get_fx_obligaciones(start=object_1.first_day_month, end=object_1.today)
object_1.get_fx_fix(start=object_1.first_day_month, end=object_1.today)
object_1.calculate_future_fx()
object_1.concat_df()
object_1.create_graph("TipoDeCambioMes.png")
object_1.debugg_prints()
object_1.calculate_gainloss()
object_1.decide_what_to_do()
object_1.build_body()

object_2 = fx_email.SendFxEmail()
object_2.get_fx_obligaciones(start=object_1.first_day_year, end=object_1.today)
object_2.get_fx_fix(start=object_1.first_day_year, end=object_1.today)
object_2.calculate_future_fx()
object_2.concat_df()
object_2.create_graph(filename="TipoDeCambioYtd.png", lineW=1.5, dot=0)
object_2.create_graph(filename="TipoDeCambioYtdAbs.png", ymin=0, lineW=1.5, dot=0)

object_1.send_email(
    TO="portfedh@gmail.com",
    CC="pablo.cruz@gmail.com",
    SUBJECT="Análisis de Tipo de Cambio",
    attchments=["TipoDeCambioMes.png", "TipoDeCambioYTD.png", "TipoDeCambioYtdAbs.png"],
)