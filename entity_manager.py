import json


class EntityManager:

    def __init__(self):

        self.filename = "entities.json"
        self.entities = []

        self.load()


    def load(self):

        try:

            with open(self.filename, "r") as file:

                self.entities = json.load(file)

        except FileNotFoundError:

            self.entities = []


    def save(self):

        with open(self.filename, "w") as file:

            json.dump(
                self.entities,
                file,
                indent=4
            )


    def add_entity(self, name):

        name = name.lower()

        if name in self.entities:
            return

        self.entities.append(name)

        self.save()

def has_entity(self, name):

    return name.lower() in self.entities