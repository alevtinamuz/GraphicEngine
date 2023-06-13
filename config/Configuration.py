from typing import Union
from lib.Exceptions.ConfigurationExceptions import *


class Configuration:
    def __init__(self, filepath: str = None):
        if filepath is None or filepath == '':
            self.filepath = None
            file = open("config/GlobalVariables.py", "r")
        else:
            self.filepath = filepath
            file = open(self.filepath, "r")
        self.configuration = dict()

        for item in file.readlines():
            self.configuration[item.split(': ')[0]] = (item.split(': ')[1]).split('\n')[0]

        file.close()

    def set_variable(self, var: str, value: Union[any, None]) -> None:
        self.configuration.update({var: value})

    def get_variable(self, var: str) -> any:
        return self.configuration.get(var)

    def execute_file(self, filepath: str):
        file = open(filepath, "r")
        for item in file.readlines():
            self.configuration[item.split(': ')[0]] = (item.split(': ')[1]).split('\n')[0]
        file.close()

    def save(self, filepath: str):
        if filepath is None:
            filepath = self.filepath
        if filepath is None:
            raise ConfigurationExceptions(ConfigurationExceptions.FILE_DOES_NOT_EXIST)
        file = open(filepath, "w")
        for key in self.configuration.keys():
            file.write(f"{key}: {self.configuration[key]}\n")
        file.close()

    def __getitem__(self, var: str):
        return self.get_variable(var)

    def __setitem__(self, var: str, value: Union[any, None]):
        self.set_variable(var, value)