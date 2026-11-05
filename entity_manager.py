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

        name = name.lower().strip()
        
        #Remove a leading article.
        if name.startswith("a "):
            name = name[2:]
            
        elif name.startswith("an "):
            name = name[3:]

        if self.has_entity(name):
            return

        entity = {
            "id": max(
                [entity["id"] for entity in self.entities],
                default=0
            ) + 1,
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

        name = name.lower().strip()

        for entity in self.entities:
            
            entity_name = entity["name"].lower().strip()

            if entity_name == name:
                return entity

        return None
    
    def get_entity_id(self, name):

        name = name.lower().strip()
        
        #Remove a leading article.
        if name.startswith("a "):
            name = name[2:]
            
        elif name.startswith("an "):
            name = name[3:]
            
        for entity in self.entities:
            
            entity_name = entity["name"].lower().strip()
            
            if entity_name.startswith("a "):
                entity_name = entity_name[2:]
                
            elif entity_name.startswith("an "):
                entity_name = entity_name[3:]
            
            if entity_name == name:
                return entity["id"]

        return None
     
    def set_entity_class(self, name, entity_class):
        
        entity_id = self.get_entity_id(name)
        
        if entity_id is None:
            return False
            
        for entity in self.entities:
            if entity["id"] == entity_id:
                current_class = entity.get("entity_class", "unknown")
                
                #Do not overwrite an existing classification.
                if current_class not in ("unknown", entity_class):
                    return False
                    
                entity["entity_class"] = entity_class
                self.save()
                return True
                
        return False
     
    def get_entity_name(self,entity_id):
        
        for entity in self.entities:
            
            if entity["id"] == entity_id:
                return entity["name"]
                
        return None        
    
    
    
    
    
    
    
    
    