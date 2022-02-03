import json
import urllib.parse
from urllib.parse import urlparse

import requests
from requests.auth import HTTPBasicAuth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lorem_ipsum_e2e.pages import PageContext


class OAuth:
    def __init__(self, page_context: PageContext, token_url: str):
        self.page_context = page_context
        self.driver = page_context.driver
        self.url = page_context.url
        self.wait = WebDriverWait(self.driver, 10)
        self.token_url = token_url

    def get_user_profile(self, access_token: str):
        response = requests.get(f'{self.url}/api/me', headers={'Authorization': f'Bearer {access_token}'})
        print(response.content)
        assert response.status_code == 200
        return json.loads(response.content.decode('utf-8'))

    def get_access_token(self, client_id, client_secret, data):
        response = requests.post(f'{self.token_url}', auth=HTTPBasicAuth(client_id, client_secret),
                                 data=data)
        access_token = json.loads(response.content.decode('utf-8'))['access_token']
        return access_token



class PasswordFlow(OAuth):
    def __init__(self, page_context: PageContext, token_url: str, authorization_url: str):
        OAuth.__init__(self, page_context, token_url)


class AuthorizationCodeFlow(OAuth):
    def __init__(self, page_context: PageContext, token_url: str, authorization_url: str):
        OAuth.__init__(self, page_context, token_url)
        self.authorization_url = authorization_url

    def get_for_authorization_grant(self, client_id: str, scope: str):
        self.driver.get(
            f'{self.authorization_url}?response_type=code&'
            f'client_id={client_id}&'
            f'scope={scope}')
        return self

    def consent_access_to_scope(self):
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//button[text()="Submit"]')))
        self.driver.find_element(By.XPATH, '//input[@type="checkbox"]').click()
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        return self

    def wait_for_authorization_code_redirect(self):
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//strong[contains(text(),'client_id:')]")))
        return self

    def get_authorization_code(self):
        return urllib.parse.parse_qs(urlparse(self.driver.current_url).query)['code'][0]
