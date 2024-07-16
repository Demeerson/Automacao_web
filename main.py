import time
from datetime import date
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from model import UserModel, DateRangeModel
from controller import WebAutomationController


# Dados de exemplo
url = 'https://saturno.hinova.com.br/sga/sgav4_grupo_golplus/v5/login.php'
username = 'DEMERSON FERREIRA'
password = 'Abril0204#'

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
    
    # # Captura o link dinâmico da nova página
    # # Suponha que o botão de extração abre a nova página em uma nova aba
    # current_window = controller.driver.current_window_handle
    # new_window = None
    # for window_handle in controller.driver.window_handles:
    #     if window_handle != current_window:
    #         new_window = window_handle
    #         break

    # if new_window:
    #     controller.driver.switch_to.window(new_window)
    #     nova_pagina_url = controller.driver.current_url
    #     controller.driver.close()  # Fechar a nova aba após capturar o URL
    #     controller.driver.switch_to.window(current_window)

    #     # Aqui você pode iniciar o processo do scrapy para extrair os dados da página
    #     process = CrawlerProcess(get_project_settings())
    #     process.crawl(MySpider, start_urls=[nova_pagina_url])
    #     process.start()
    
finally:
    time.sleep(900)
    print("Arquivo extraído com sucesso!")
    controller.close_driver()
