import time
from datetime import date
from model import UserModel, DateRangeModel
from controller import WebAutomationController


# Dados de exemplo
url = 'URL'
username = 'SEU USURARIO'
password = 'SUA SENHA'

# Calcula a data de início (primeiro dia do mês atual)
primeiro_dia_mes_atual = date.today().replace(day=1)
data_inicio = primeiro_dia_mes_atual.strftime('%d/%m/%Y')

# Calcula a data de fim (hoje)
data_fim = date.today().strftime('%d/%m/%Y')

# Instancia os modelos
user_model = UserModel(username, password)
date_range_model = DateRangeModel(data_inicio, data_fim)

# Instancia o controlador
controller = WebAutomationController(url, user_model, date_range_model)

try:
    controller.login()
    controller.input_date_range_and_extract()
    time.sleep(5)
    controller.select_layout_option()
    time.sleep(2)
    controller.select_output_format()
    
    
finally:
    time.sleep(900)
    print("Arquivo extraído com sucesso!")
    controller.close_driver()
