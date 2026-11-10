from parsers import Parser

class UserInterface:
    def __init__(self,collection):
        self.__parser = Parser(collection)

    def check_collection_info(self):
        self.__parser.run()