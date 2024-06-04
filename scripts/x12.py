from __init__ import *

import warnings


# warnings.simplefilter('ignore')


class X12:
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
        driver.get('https://x12.p-cod.com/skatclient/')
        driver.maximize_window()
        time.sleep(1)

        return driver

    def login_in(self):
        logger.info('Получение элемента')
        self.wait = WebDriverWait(self.driver, 10)
        login_input = self.wait.until(EC.presence_of_element_located((By.ID, 'Login')))
        password_input = self.wait.until(EC.presence_of_element_located((By.ID, 'Pass')))
        login_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'loginButton')))

        # Вводим логин и пароль
        logger.info('Ввод логина и пароля')
        login_input.send_keys(self.login)
        password_input.send_keys(self.password)

        # Нажимаем кнопку "Войти"
        login_button.click()

        # Ожидаем, пока страница загрузится (может потребоваться уточнение)
        # self.wait.until(EC.title_contains('Ожидаемый заголовок страницы'))

    def accommodation(self):
        logger.info('Выбор элемента "Размещения"')
        razmesheniya_link = self.wait.until(EC.element_to_be_clickable((By.ID, 'mainmenu:requestsin')))
        razmesheniya_link.click()

        # Ожидаем, пока страница загрузится (может потребоваться уточнение)
        # self.wait.until(EC.title_contains('Ожидаемый заголовок страницы'))

    def create_placement(self):
        logger.info('Выбор элемента "Принять контейнер на терминал"')
        accept_container_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'requestsin:СlientRequestsInTable:j_id247')))
        accept_container_button.click()

    def get_all_type_containers(self, container_size):
        logger.info('Получение всех опций "Тип контейнера"')
        container_type_select = Select(
            self.driver.find_element(By.ID, 'requestinadd:СlientRequestInPositionsTable:0:somtype'))
        all_options = container_type_select.options
        result = [x.text for x in container_type_select.options]
        logger.info(f'Выбор элемента "Тип контейнера" и ввод значения: {container_size}')
        for option in all_options:
            if option.text == container_size:
                option.click()
                break
        return result

    def filling_out_the_form(self, date_finish, container_number):
        logger.info('Выбор элемента "Дата" и ввод даты')
        date_input = self.wait.until(EC.presence_of_element_located((By.ID, 'requestinadd:requestinaddbean_date2')))
        date_input.clear()  # Очищаем поле от предыдущей даты, если она там была
        date_input.send_keys(date_finish)

        logger.info('Выбор элемента "Номер контейнера" и ввод номера')
        container_number_input = self.wait.until(
            EC.presence_of_element_located((By.ID, 'requestinadd:СlientRequestInPositionsTable:0:j_id476')))
        container_number_input.clear()  # Очищаем поле от предыдущего номера, если он там был
        container_number_input.send_keys(container_number)

        logger.info('Выбор элемента "Сохранить"')
        save_button = self.wait.until(EC.element_to_be_clickable((By.ID, 'requestinadd:j_id615')))
        save_button.click()

    def check_order(self):
        expected_value = "Заявка успешно создана."
        try:
            textarea_locator = (By.ID, 'requestinadd:j_id611')
            textarea = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(textarea_locator)
            )

            # Получение значения атрибута value
            actual_value = textarea.get_attribute("value")
            if not actual_value:
                try:
                    textarea_locator = (By.ID, 'requestinadd:j_id610')
                    textarea = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(textarea_locator)
                    )

                    # Получение значения атрибута value
                    actual_value = textarea.get_attribute("value")

                    # Ожидаемое сообщение об ошибке
                except Exception as ex:
                    ...
        except Exception as e:
            ...

        if actual_value == expected_value:
            print(expected_value)
        else:
            print(f"Ошибка при создание заявки: {actual_value}")

    def main(self, date, container_size, container_number):
        self.login_in()
        time.sleep(2)
        self.accommodation()
        time.sleep(2)
        self.create_placement()
        time.sleep(2)
        self.get_all_type_containers(container_size)
        time.sleep(1)
        self.filling_out_the_form(date, container_number)
        time.sleep(1)
        self.check_order()


x = X12('denisov.m@nova-star.org', 'qwerty7787')
x.main('20.03.2024', '40HC', 'FCI7601467')
