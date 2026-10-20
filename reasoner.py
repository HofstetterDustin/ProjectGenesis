class Reasoner:

    def __init__(self, entities):
        self.entities = entities
    
    def infer(self, facts):
        
        conclusions = []

        for fact in facts:

            if fact["relationship"] != "is_a":
                continue

            self.follow_chain(
                fact["subject_id"],
                fact["object_id"],
                facts,
                conclusions,
                set()
            )

        return conclusions


    def follow_chain(
        self,
        subject_id,
        current_id,
        facts,
        conclusions,
        visited
    ):

        if current_id in visited:
            return

        visited.add(current_id)

        for fact in facts:

            if fact["relationship"] != "is_a":
                continue

            if fact["subject_id"] == current_id:

                conclusion = {
                    "subject_id": subject_id,
                    "relationship": "is_a",
                    "object_id": fact["object_id"],
                    "source": "Genesis",
                    "confidence": 0.9,
                    "type": "inference"
                }

                if conclusion not in conclusions:
                    conclusions.append(conclusion)

                self.follow_chain(
                    subject_id,
                    fact["object_id"],
                    facts,
                    conclusions,
                    visited.copy()
                )
                
                
                
                
                
                
                