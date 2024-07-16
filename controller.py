import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from model import UserModel, DateRangeModel

class WebAutomationController:
    def __init__(self, url, user_model, date_range_model):
        self.url = url
        self.user_model = user_model
        self.date_range_model = date_range_model
        self.driver = webdriver.Chrome()  # Inicializa o WebDriver (Chrome neste exemplo)
        

    def login(self):
        self.driver.get(self.url)
        
        # Espera até que o modal de comunicado importante apareça
        try:
            alert_modal = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog'))
            )
            
            # Clique no botão "Continuar e Fechar"
            continue_button = alert_modal.find_element(By.CLASS_NAME, 'aceite-cookie')
            continue_button.click()
        
        except TimeoutException:
            print("O modal de comunicado importante não foi encontrado ou não apareceu a tempo.")
            # Se não encontrar o modal, continua mesmo assim
            
        # Espera até que o modal de aviso desapareça
        try:
            WebDriverWait(self.driver, 10).until_not(
                EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog'))
            )
        except TimeoutException:
            print("O modal de aviso ainda está presente ou não pôde ser fechado.")
            
            
        # Preenche o campo de usuário
        username_field = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.ID, 'usuario')))
        username_field.send_keys(self.user_model.get_username())
        
        # Preenche o campo de senha
        password_field = self.driver.find_element(By.ID, 'senha')
        password_field.send_keys(self.user_model.get_password())
        
        # Clica no botão de login
        login_button = self.driver.find_element(By.CLASS_NAME, 'btn.btn-primary')
        login_button.click()
        
        # Fechar o modal de aviso se ele estiver presente
        try:
            close_modal_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-dismiss='modal']"))
            )
            close_modal_button.click()
        except TimeoutException:
            print("O modal de aviso não apareceu ou não foi possível fechá-lo.")
        
        # Aguarda até que o menu suspenso esteja visível e clicável
        dropdown_menu = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'navbar7')))
        dropdown_menu.click()

        # Aguarda até que a opção desejada no menu suspenso esteja visível e clicável
        option_to_select = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '8.3) .. de Boletos')]")))
        option_to_select.click()

        # Aguarda até que a página de relatórios de boletos seja completamente carregada
        WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.ID, 'DataVencimento')))
        

    def input_date_range_and_extract(self):
        # Insere a data inicial
        start_date_field = self.driver.find_element(By.ID, 'DataVencimento')
        start_date_field.clear()
        start_date_field.send_keys(self.date_range_model.get_start_date())

        # Insere a data final
        end_date_field = self.driver.find_element(By.ID, 'DataVencimentoFinal')
        end_date_field.clear()
        end_date_field.send_keys(self.date_range_model.get_end_date())
        
        time.sleep(10)

    def select_layout_option(self):
        # Aguarda até que o menu de layout esteja disponível
        layout_menu = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'cmbLayoutRelatorio'))
        )
        
        # Seleciona a opção de layout (exemplo com Select)
        layout_select = Select(layout_menu)
        layout_select.select_by_value('81')  # Seleciona o layout com valor '81' (KPI_INADIMPLENCIA)
        
        # Aguardar 2 segundos após selecionar o layout
        time.sleep(5)

    def select_output_format(self):
        # Seleciona o formato de saída como Excel
        excel_radio = self.driver.find_element(By.XPATH, "//input[@name='optFormaExibicao' and @value='E']")
        excel_radio.click()

        # Clica no botão de extração
        extract_button = self.driver.find_element(By.ID, 'pbSalvar')
        extract_button.click()
        

    def close_driver(self):
        time.sleep(20)  # Aguarda 20 segundos para garantir que todas as operações sejam concluídas
        self.driver.quit()

