import os
import pytest
from selenium import webdriver
from lorem_ipsum_e2e import oauth
from lorem_ipsum_e2e import pages


@pytest.fixture()
def browser():
    _browser = webdriver.Safari()
    yield _browser
    _browser.quit()


@pytest.fixture()
def config():
    _config = {}
    import json
    with open(f"{os.path.expanduser('~')}/.cloud-projects/lorem-ipsum-e2e.json", "r") as _file:
        json = dict(json.load(_file))
        print(json)
        for k, v in json.items():
            _config[k] = v
    yield _config

@pytest.fixture()
def new_client_data(browser, config):
    root_url = 'http://localhost:5000'
    login_page = pages.Login(pages.PageContext(browser, root_url))
    client_page = pages.Client(pages.PageContext(browser, root_url))
    create_client_page = pages.CreateClient(pages.PageContext(browser, root_url))

    login_page.load().set_user('admin')
    client_page.wait_to_load().open_create_client_form()
    create_client_page.wait_to_load().set_client(config).submit()

    last_client_data_element = client_page.wait_to_load().get_last_client()
    assert len(last_client_data_element) == 1

    return client_page.get_last_client_data()