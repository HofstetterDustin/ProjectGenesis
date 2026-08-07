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

        if self.has_entity(name):
            return

        entity = {
            "id": len(self.entities) + 1,
            "name": name,
            "entity_class": "unknown",
            "aliases": [],
            "attributes": {},
            "metadata": {}
        }
        self.entities.append(entity)    

        self.save()

    def has_entity(self, name):

        name = name.lower()
        
        for entity in self.entities:
            
            if entity["name"] == name:
                return True
                
        return False

    def get_entity(self, name):

        name = name.lower()

        for entity in self.entities:

            if entity["name"] == name:
                return entity

        return None
    
    def get_entity_id(self, name):

        entity = self.get_entity(name)

        if entity:
            return entity["id"]

        return None
        
    def get_entity_name(self,entity_id):
        
        for entity in self.entities:
            
            if entity["id"] == entity_id:
                return entity["name"]
                
        return None        
    
    
    
    
    
    
    
    
    