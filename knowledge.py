import json


class KnowledgeBase:

    def __init__(self):
        self.filename = "knowledge.json"
        self.facts = []
        self.load()

    """Load knowledge from disk."""
    def load(self):
        
        try:
            with open(self.filename, "r") as file:
                self.facts = json.load(file)
        except FileNotFoundError:
            self.facts = []
        #Find the highest existing fact ID.
        highest_id = 0
        
        for fact in self.facts:
            fact_id = fact.get("fact_id", 0)
            
            if isinstance(fact_id, int) and fact_id > highest_id: 
                highest_id = fact_id
                
        #Assign IDs to facts that do not have one.
        for fact in self.facts:
            if "fact_id" not in fact:
                highest_id += 1
                fact["fact_id"] = highest_id
                
        #Save the updated facts.
        self.save()
        
        #Prepare the next ID for new facts.
        self.next_fact_id = highest_id + 1
            
    """Save knowledge to disk."""
    def save(self):
        
        with open(self.filename, "w") as file:
            json.dump(self.facts, file, indent=4)
            
    """Check if a fact already exists."""
    def contains_fact(
        self, 
        subject_id, 
        relationship, 
        object_id, 
        source="unknown"
        ):
    
        for fact in self.facts:
            if (
                fact["subject_id"] == subject_id
                and fact["relationship"] == relationship
                and fact["object_id"] == object_id
                and fact["source"] == source
            ):
                return True

        return False

    """Add new knowledge. Related to self.memory.add_fact() in ai.py"""        
    def add_fact(
        self,
        subject_id,
        relationship,
        object_id,
        source="Unknown",
        confidence=1.0,
        fact_type="learned",
        scope="unspecified"
    ):

        if self.contains_fact(subject_id, relationship, object_id, source):
            for fact in self.facts:
                if (                
                    fact["subject_id"] == subject_id
                    and fact["relationship"] == relationship
                    and fact["object_id"] == object_id
                    and fact["source"] == source
                ):
                    if (
                        fact.get("scope", "unspecified") == "unspecified"
                        and scope != "unspecified"
                    ):
                        fact["scope"] = scope
                        self.save()
                        
            return False
        
        """Dictionary"""    
        fact = {
            "subject_id": subject_id,
            "relationship": relationship,
            "object_id": object_id,
            "source": source,
            "confidence": confidence,
            "type": fact_type,
            "scope": scope
        }

        self.facts.append(fact)
        self.save()   

        print("I added new fact. | add_fact()")
        
        return True
    
    """Find information about a subject. This is the read functionality"""
    def find_facts(self, subject_id):
        
        results = []

        for fact in self.facts:
            if fact["subject_id"] == subject_id:
                results.append(fact)

        return results
    
    """Contradiction Detection."""
    def find_conflict(self, subject_id, relationship, object_id):
        
        opposites = {
            "is_a": "is_not_a",
            "is_not_a": "is_a",
            "is": "is_not",
            "is_not": "is"
        }
        
        opposite = opposites.get(relationship)
        
        if opposite is None:
            return None
            
        for fact in self.facts:
            
            if(
                fact["subject_id"] == subject_id
                and fact["relationship"] == opposite
                and fact["object_id"] == object_id
            ):
                return fact
                
        return None
        
        
        
        
        
        
        
        