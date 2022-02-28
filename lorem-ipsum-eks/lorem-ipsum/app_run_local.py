import os

if __name__ == "__main__" or __name__ == 'app' and os.getenv('env') != 'test':
    import json

    print('Running local app...')
    with open(f"{os.path.expanduser('~')}/.cloud-projects/lorem-ipsum-local-integration.json", "r") as _file:
        json = dict(json.load(_file))
        print(json)
        for k, v in json.items():
            os.environ[k] = str(v)
    os.environ['env'] = 'test'
    import app

    flask_app = app.create_flask_app()
    from lorem_ipsum.search_engine import SearchEngine
    SearchEngine.start_search_engine()
    flask_app.run(port=5000, debug=False)

