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

    """Save knowledge to disk."""
    def save(self):
        
        with open(self.filename, "w") as file:
            json.dump(self.facts, file, indent=4)
            
    """Check if a fact already exists."""
    def contains_fact(self, subject, relationship, object, source="unknown"):
    
        for fact in self.facts:
            if (
                fact["subject"] == subject
                and fact["relationship"] == relationship
                and fact["object"] == object
                and fact["source"] == source
            ):
                return True

        return False

    """Add new knowledge."""        
    def add_fact(
        self,
        subject,
        relationship,
        object,
        source="Unknown",
        confidence=1.0,
        fact_type="learned"
    ):

        if self.contains_fact(subject, relationship, object):
            print("I already know this.")
            return
            
        fact = {
            "subject": subject,
            "relationship": relationship,
            "object": object,
            "source": source,
            "confidence": confidence,
            "type": fact_type
        }

        self.facts.append(fact)
        self.save()   

        print("I learned something new.")
    
    """Find information about a subject."""
    def find_facts(self, subject):
        
        results = []

        for fact in self.facts:
            if fact["subject"] == subject:
                results.append(fact)

        return results