import time

from __init__ import *


class Ural:
    def __init__(self, login, password):
        self.driver: WebDriver = self.connect_google()
        self.wait = None
        self.login = login
        self.password = password

    @staticmethod
    def connect_google() -> Optional[Union[WebDriver, None]]:
        options: Options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--headless')
        options.add_argument('--start-maximized')
        logger.info('открытие драйвера')
        driver: WebDriver = webdriver.Chrome(options=options)
        logger.info('Подключение к странице')
        driver.get('https://ural.effex.ru/ru')
        driver.maximize_window()
        time.sleep(1)

        return driver

    def login_in(self):
        self.wait = WebDriverWait(self.driver, 10)

        # Ввод логина
        login_input = self.wait.until(EC.presence_of_element_located((By.NAME, 'login')))
        login_input.send_keys(self.login)

        # Ввод пароля
        password_input = self.wait.until(EC.presence_of_element_located((By.NAME, 'password')))
        password_input.send_keys(self.password)

        # Нажатие на кнопку "Войти"
        login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Войти"]')))
        login_button.click()

    def tractor_unit(self):
        priem_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[text()="Прием"]'))
        )
        priem_element.click()

        # Ожидание появления элемента "Автотягач" и клик на нем
        avtotyagach_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[text()="Автотягач"]'))
        )
        avtotyagach_element.click()

        time.sleep(3)


    def accommodation(self):
        add_request_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Добавить заявку"]'))
        )
        add_request_button.click()

        # Ожидание появления и клик на "Порожние списком"
        porozhnie_s_listom_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[text()=" Порожние списком"]'))
        )
        porozhnie_s_listom_link.click()

    def filling_out_the_form(self, name_port, container_numbers, size_container):
        direction_element = self.driver.find_element(By.NAME, "direction")
        direction_select = Select(direction_element)
        direction_select.select_by_value("Владивосток")

        # Найти выпадающий список
        dropdown_menu = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@aria-owns="bs-select-9"]'))
        )

        # Используйте Select для удобного взаимодействия с выпадающим списком
        select = Select(dropdown_menu)

    def main(self):
        self.login_in()
        self.tractor_unit()
        self.accommodation()
        time.sleep(5)
        self.filling_out_the_form('Владивосток', 'FCIU7601467', '40 HC')


u = Ural('denisov.m@noa-ltd.ru', 'XUWqac5o9d')
u.main()
