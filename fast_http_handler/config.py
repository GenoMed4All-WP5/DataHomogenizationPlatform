import os

basedir = os.path.abspath(os.path.dirname(__file__))

httphandlers = [
    {
        "class": "extensions.Genomed4All.fast_http_handler.genomed4all_api",
        "url": "/api/datasets"
    }
]
