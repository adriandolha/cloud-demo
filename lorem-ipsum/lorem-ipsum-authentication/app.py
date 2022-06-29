import os

from lorem_ipsum_auth.app import create_flask_app

if __name__ == "__main__" or __name__ == 'app' and os.getenv('env') != 'test':
    app = create_flask_app()
