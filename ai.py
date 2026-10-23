from knowledge import KnowledgeBase
from teacher import Teacher
from reasoner import Reasoner
from source_manager import SourceManager
from evidence import Evidence
from entity_manager import EntityManager

class AI:

    def __init__(self):
        self.sources = SourceManager()
        self.evidence = Evidence()
        self.current_source = "Dustin"
        self.entities = EntityManager()
        self.reasoner = Reasoner(self.entities)
        self.memory = KnowledgeBase()
        self.teacher = Teacher()
        
    def process(self, sentence):

        sentence = sentence.strip()
        question = sentence.lower()

        # Question pattern: What do we know about [subject]?
        prefix = "what do we know about "
        
        if question.startswith(prefix):
            subject = sentence[len(prefix):].rstrip("?").strip().lower()
            if question.startswith("a "):
                subject = subject[2:]
            elif subject.startswith("an "):
                subject = subject[3:]
            
            return self.ask(subject)
        
        # Question pattern: What is [subject]?
        if question.startswith("what is"):
            subject = (
                sentence[8:]
                .replace("?", "")
                .strip()
                .lower()
            )
            # Remove the article at the beginning.
            if subject.startswith("a "):
                subject = subject[2:]
                
            elif subject.startswith("an "):
                subject = subject[3:]
                
            return self.ask(subject)

        # Otherwise, treat the input as something to learn.
        return self.teach(sentence)

    def ask(self, subject):

        subject_id = self.entities.get_entity_id(subject)
        
        if subject_id is None:
            return "I don't know, no _id. | ask() ai.py"
            
        #contains the facts associated with the subject
        facts = self.memory.find_facts(subject_id)
        
        #contains the complete collection of stored facts for trace relationships between entities.
        all_facts = self.memory.facts
        
        #gives the reasoner the stored facts & receives a separate collection of conclusions.
        inferred = self.reasoner.infer(all_facts)
        
        facts.extend(
            [
                fact
                for fact in inferred
                if fact["subject_id"] == subject_id
            ]
        )

        if not facts:
            return "I don't know, no facts. (ai.py)"

        answers = []

        for fact in facts:
            
            subject_id = fact["subject_id"]
            relationship = fact["relationship"]
            object_id = fact["object_id"]
                        
            subject = self.entities.get_entity_name(subject_id)
            object_name = self.entities.get_entity_name(object_id)

            source = fact.get("source", "Unknown")
            confidence = fact.get("confidence", 0)
            
            #retrieves the source's reliability and calculates the evidence score.
            source_info = self.sources.get_source(source)
            if source_info:
                reliability = source_info["reliability"]
            else:
                reliability = 0.0
            evidence = self.evidence.calculate(
                confidence,
                reliability
            )
            
            if relationship == "is_a":
                article = "an" if object_name[0].lower() in "aeiou" else "a"
                entity = self.entities.get_entity(subject)
                if entity and entity.get("entity_class") == "individual":
                    sentence = f"{subject.capitalize()} is {article} {object_name}."
                else:
                    sentence = f"A {subject} is {article} {object_name}."
                
            elif relationship == "has":
                sentence = f"A {subject} has {object_name}."
            
            elif relationship == "has_property":
                entity = self.entities.get_entity(subject)
                if entity and entity.get("entity_class") == "individual":
                    sentence = f"{subject.capitalize()} is {object_name}."
                else:
                    sentence = f"A {subject} is {object_name}."
                
            elif relationship == "has_not":
                sentence = f"A {subject} has not {object_name}."
                
            elif relationship == "can":
                sentence = f"A {subject} can {object_name}."    

            elif relationship == "can_not":
                sentence = f"A {subject} cannot {object_name}."

            elif relationship == "is_not_a":
                article = "an" if object_name[0].lower() in "aeiou" else "a"
                sentence = f"A {subject} is not {article} {object_name}."

            else:
                sentence = f"{subject} {relationship} {object_name}."

            scope = fact.get("scope", "unspecified")
            
            answers.append(
                f"{sentence} "
                f"(Source: {source}, "
                f"Confidence: {confidence*100:.0f}%, "
                f"Reliability: {reliability*100:.0f}%, "
                f"Evidence: {evidence*100:.0f}%, "
                f"Scope: {scope})"
            )

        return "\n\n".join(answers)

    def teach(self, sentence):

        fact = self.teacher.parse(sentence)

        if fact is None:
            return "I don't understand. | teach() ai.py"

        subject, relationship, object = fact
        
        #Determin entity classification from the original sentence.
        words = sentence.lower().strip().rstrip(".").split()
        
        # Ensure both entities exist before classifying them.
        self.entities.add_entity(subject)
        self.entities.add_entity(object)
        
        if relationship == "is_a":
            
            is_index = words.index("is")
            subject_words = words[:is_index]
            
            if subject_words and subject_words[0] in ("a", "an"):
                self.entities.set_entity_class(subject, "category")
            else:
                self.entities.set_entity_class(subject, "individual")
                
            self.entities.set_entity_class(object, "category")
        
        # Determin the scope of the fact.
        if relationship == "is_a":
            scope = "category_membership"
        
        elif relationship == "has_property":
            entity = self.entities.get_entity(subject)
            
            if entity and entity.get("entity_class") == "category":
                scope = "category_possible"
            else:
                scope = "individual"
        
        else:
            scope = "unspecified"
        
        subject_id = self.entities.get_entity_id(subject)
        object_id = self.entities.get_entity_id(object)
        
        conflict = self.memory.find_conflict(
            subject_id,
            relationship,
            object_id
        )
        
        if conflict:
            
            existing_subject = self.entities.get_entity_name(
                conflict["subject_id"]
            )
                
            existing_object = self.entities.get_entity_name(
                conflict["object_id"]
            )
                
            return (
                "I found conflicting knowledge.(ai.py L100)\n"
                f"Existing: {existing_subject} "
                f"{conflict['relationship']} "
                f"{existing_object}\n"
                f"Source: {conflict['source']}"
            )
            
       

        """print(self.entities.get_entity_name(1))
        print(self.entities.get_entity_name(2))"""
        
        added = self.memory.add_fact(
            subject_id,
            relationship,
            object_id,
            source=self.current_source,
            confidence=1.0,
            fact_type="learned",
            scope=scope
        )
        
        if added:
            return "I learned something new." 
            
        return "I already know this."
        
        
        
        