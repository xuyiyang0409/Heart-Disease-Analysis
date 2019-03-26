#!/usr/bin/python3
# Uniform controller

import backend.db_handler

if __name__ == "__main__":
    db_controller = backend.db_handler.DBHandler()
    db_controller.initialize()
    db_controller.data_import()