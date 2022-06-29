from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PageContext:
    def __init__(self, driver: WebDriver, url: str):
        self.url = url
        self.driver = driver


class RootPage:
    def __init__(self, page_context: PageContext):
        self.page_context = page_context
        self.driver = page_context.driver
        self.url = page_context.url
        self.wait = WebDriverWait(self.driver, 10)

    def load(self):
        self.driver.get(self.url)
        return self


class Login(RootPage):
    def __init__(self, page_context: PageContext):
        RootPage.__init__(self, page_context)

    def set_user(self, username):
        elem = self.driver.find_element(By.NAME, 'username')  # Find the search box
        elem.send_keys(username + Keys.RETURN)


class CreateClient(RootPage):
    def __init__(self, page_context: PageContext):
        RootPage.__init__(self, page_context)

    def wait_to_load(self):
        self.wait.until(EC.element_to_be_clickable((By.NAME, 'client_name')))
        return self

    def set_client(self, data):
        self.driver.find_element(By.NAME, "client_name").send_keys(data.get('client_name'))
        self.driver.find_element(By.NAME, "client_uri").send_keys(data.get('client_uri'))
        self.driver.find_element(By.NAME, "scope").send_keys(data.get('scope'))
        self.driver.find_element(By.NAME, "redirect_uri").send_keys(data.get('redirect_uri'))
        grant_types = data.get('grant_type')
        self.driver.find_element(By.NAME, "grant_type").send_keys(
            grant_types[0] + Keys.ENTER + grant_types[1])
        self.driver.find_element(By.NAME, "response_type").send_keys(data.get('response_type'))
        return self

    def submit(self):
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        return self


class Client(RootPage):
    def __init__(self, page_context: PageContext):
        RootPage.__init__(self, page_context)

    def wait_to_load(self):
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Create Client')))
        return self

    def open_create_client_form(self):
        self.driver.find_element(By.LINK_TEXT, 'Create Client').click()
        return self

    def get_last_client(self):
        return self.driver.find_elements(By.XPATH, "//pre[last()]")

    def get_last_client_data(self):
        client_data_dict = {}

        for client_data in [line.split(':') for line in
                            self.get_last_client()[0].text.split('\n')]:
            if len(client_data) == 2:
                client_data_dict[client_data[0].strip()] = client_data[1].strip()
        return client_data_dict
