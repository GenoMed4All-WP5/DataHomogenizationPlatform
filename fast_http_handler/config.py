import os

basedir = os.path.abspath(os.path.dirname(__file__))

httphandlers = [
    {
        "class": "extensions.DataHomogenizationPlatform.fast_http_handler.homogenizationPlatformAPI",
        "url": "/test/data"
    }]


