import json


class SourceManager:

    def __init__(self):
        self.filename = "sources.json"
        self.sources = []
        self.load()


    def load(self):

        try:
            with open(self.filename, "r") as file:
                self.sources = json.load(file)

        except FileNotFoundError:
            self.sources = []


    def get_source(self, name):

        for source in self.sources:

            if source["name"].lower() == name.lower():
                return source

        return None