import unittest,re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

class RegTest(unittest.TestCase):
    def setUp(self):
        # Запуск в режиме headless - окно браузера не будет показываться на экране
        #options = Options()
        #options.headless = True
        #self.driver = webdriver.Firefox(options=options)
        self.driver = webdriver.Firefox()
        self.site_url = "https://example.com/" #ввести адрес сайта для регистрации пользователя
    
    def test_succesful_user_registration(self):
        """Проверка регистрации нового пользователя"""
        
        #Создаем новую вкладку и заходим на mail.tm (временный email)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.driver.get('https://mail.tm/')
        self.driver.window_handles[0]
        
        #Подтягиваем email и пароль       
        self.driver.find_element_by_id('accounts-menu').click()
        new_mail = self.driver.find_element_by_xpath('//*[@id="accounts-list"]/div/div[1]/p[2]').text
        new_pass = self.driver.find_element_by_class_name('account-blur').text
        
        #Проверяем данные email
        try:
            self.assertGreater(len(new_mail), 0)
        except TypeError:
            print('\nВременный Email не получен')
            raise 
        else:
            print('\nВременный Email получен: ', new_mail)       

        #Проверяем данные пароля
        try:
            self.assertGreater(len(new_pass), 0)
        except TypeError:
            print('\nВременный Пароль не получен')
            raise 
        else:
            print('Временный Пароль получен: ', new_pass)       
     
        #Открываем вторую вкладку для регистрации
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(self.site_url)

        #Проверяем наличие кнопки "Вход" и кликаем на неё
        try:
            self.driver.find_element_by_class_name('widget-button__ButtonText-sc-7ezmr3-4.kGpZKe').click()
        except NoSuchElementException:
            print('\nКнопка "Вход" на главной не найдена')
            raise
        else:
            print('Кнопка "Вход" на главной найдена и на неё нажали')

        #Проверяем появление модального окна авторизации
        try:
            self.driver.find_element_by_id('form-entry')
        except NoSuchElementException:
            print('\nМодальное окно авторизации не найдено')
            raise
        else:
            print('Модальное окно авторизации найдено')

        #Проверяем наличие кнопки "Регистрация" и кликаем на неё
        try:
            self.driver.find_element_by_class_name('link__View-sc-1ydrjtx-0.koEghb').click()
        except NoSuchElementException:
            print('\nКнопка "Регистрация" в модальном окне не найдена')
            raise
        else:
            print('Кнопка "Регистрация" в модальном окне найдена и на неё нажали')

        #Проверяем переключение из "Вход" на "Регистрация"
        try:
            self.driver.find_element_by_class_name('button-action__View-sc-1xgnbfo-0.cCelhz')
        except NoSuchElementException:
            print('\nФорма Регистрации не открылась')
            raise
        else:
            print('Форма Регистрации открылась')

        #Проверяем наличие поля ввода Email для регистрации и отправляем в нее временный Email        
        try:
            self.driver.find_element_by_xpath('//*[@id="form-entry"]/div/form/fieldset[1]/label/div[2]/input')

        except NoSuchElementException:
            print('\nПоле ввода Email для регистрации не найдено')
            raise
        else:
            self.driver.find_element_by_xpath('//*[@id="form-entry"]/div/form/fieldset[1]/label/div[2]/input').send_keys(new_mail)
            print('Поле ввода Email для регистрации найдено и заполенено: ', new_mail)
        
        #Проверяем наличие поля ввода пароля для регистрации кликаем и отправляем в нее пароль        
        try:
            self.driver.find_element_by_xpath('//*[@id="form-entry"]/div/form/fieldset[2]/label/div[2]/input').click()
        except NoSuchElementException:
            print('\nПоле ввода пароля для регистрации не найдено')
            raise
        else:
            self.driver.find_element_by_xpath('//*[@id="form-entry"]/div/form/fieldset[2]/label/div[2]/input').send_keys(new_pass)
            print('Поле ввода пароля для регистрации найдено и заполенено: ', new_pass)
       
        #Проверяем правильность заполенных полей для регистрации и нажимаем "Зарегистрироваться"
        try:
            self.driver.find_element_by_class_name('buttonLoader__View-hkgzw7-0.iWHvdP')
        except NoSuchElementException:
            print('\nПоля для регистрации заполнены не верно')
            raise
        else:
            print('Поля для регистрации заполнены верно')
        
        #Проверяем наличие кнопки "Зарегистрироваться" и кликаем на неё
        try:
            self.driver.find_element_by_class_name('buttonLoader__View-hkgzw7-0.iWHvdP').click()
        except NoSuchElementException:
            print('\nКнопка "Зарегистрироваться" не найдена')
            raise
        else:
            print('Кнопка "Зарегистрироваться" найдена и на неё нажали')

        #Проверяем наличия поля ввода кода подтверждения
        try:
            self.driver.find_element_by_xpath('//*[@id="form-entry"]/div/form/fieldset/label/div[2]/input')
        except NoSuchElementException:
            print('\nПоле проверки кода не найдено')
            raise
        else:
            print('Поле проверки кода найдено')            

        #Переход на первую вкладку с временной почтой  увеличиваем время ожидания появления элементов    
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.get("https://mail.tm/")
        self.driver.implicitly_wait(60)
        
        #Проверяем получение письма с кодом подтверждения
        try:
            self.driver.find_element_by_css_selector('div.truncate:nth-child(2)') 
        except NoSuchElementException:
            print('\nПисьмо с кодом не пришло')
            raise
        else:
            msg = self.driver.find_element_by_css_selector('div.truncate:nth-child(2)').text
            ver_code = re.search(r'\d{6}',msg) #выдергиваем из текста письма код
            print('Письмо пришло. Код: ', ver_code[0])
            self.driver.implicitly_wait(5) #уменьшаем время ожидания появления элементов

        #Переход на вторую вкладку с сайтом регистрации в браузере
        self.driver.switch_to.window(self.driver.window_handles[1])

        #Отправляем в поле ввода код потверждения
        try:
            self.driver.find_element_by_xpath('//*[@id="form-entry"]/div/form/fieldset/label/div[2]/input')
        except NoSuchElementException:
            print('\nПоле проверки кода не найдено')
            raise
        else:
            self.driver.find_element_by_xpath('//*[@id="form-entry"]/div/form/fieldset/label/div[2]/input').send_keys(ver_code[0])
            print('Код вставлен в поле ввода')
     
        #Поиск и нажатие на кнопку подвердить регистрацию
        try:
            self.driver.find_element_by_xpath('//*[@id="form-entry"]/div/form/div[3]/button')
        except NoSuchElementException:
            print('\nКнопка завершения регистрации не найдена')
            raise
        else:
            self.driver.find_element_by_xpath('//*[@id="form-entry"]/div/form/div[3]/button').click()
            print('Кнопка проверки кода найдена и неё нажали')

        #Открытие модального окна скачанивания приложения на сайте
        try:           
            self.driver.find_element_by_css_selector('.cYwsvr')
        except NoSuchElementException:
            print('\nМодальное окно скачивания приложения не найдено')
            raise
        else:
            print('Модальное окно "Скачать приложение" открыто')

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
