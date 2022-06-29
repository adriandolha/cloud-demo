from lorem_ipsum_e2e import oauth
from lorem_ipsum_e2e import pages


class TestAuthentication:
    def test_authorization_code_flow(self, config, browser, new_client_data):
        root_url = 'http://localhost:5000'
        client_id = new_client_data["client_id"]
        client_secret = new_client_data["client_secret"]
        authorization_code_flow = oauth.AuthorizationCodeFlow(pages.PageContext(browser, root_url),
                                                              token_url=f'{root_url}/oauth/token',
                                                              authorization_url=f'{root_url}/oauth/authorize')
        authorization_code_flow.get_for_authorization_grant(client_id, scope='profile'). \
            consent_access_to_scope(). \
            wait_for_authorization_code_redirect()

        access_token = authorization_code_flow.get_access_token(client_id=client_id,
                                                                client_secret=client_secret,
                                                                data={
                                                                    'grant_type': 'authorization_code',
                                                                    'scope': 'profile',
                                                                    'code': authorization_code_flow.get_authorization_code()
                                                                })
        assert authorization_code_flow.get_user_profile(access_token)['username'] == 'admin'

    def test_password_flow(self, config, browser, new_client_data):
        root_url = 'http://localhost:5000'
        client_id = new_client_data["client_id"]
        client_secret = new_client_data["client_secret"]

        _oauth = oauth.OAuth(pages.PageContext(browser, root_url), token_url=f'{root_url}/oauth/token')
        access_token = _oauth.get_access_token(client_id=client_id,
                                               client_secret=client_secret,
                                               data={
                                                   'username': 'admin',
                                                   'password': 'valid',
                                                   'grant_type': 'password',
                                                   'scope': 'profile'
                                               })
        assert _oauth.get_user_profile(access_token)['username'] == 'admin'
