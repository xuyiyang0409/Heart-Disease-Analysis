#!/usr/bin/python3
# Uniform controller

import backend.db_handler
from backend.api import app

if __name__ == "__main__":
    db_controller = backend.db_handler.DBHandler()
    if db_controller.initialize():
        db_controller.data_import()

    app.run(host='127.0.0.1', port=8888, debug=True)