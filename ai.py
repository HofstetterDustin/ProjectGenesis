from knowledge import KnowledgeBase
from teacher import Teacher
from reasoner import Reasoner
from source_manager import SourceManager
from evidence import Evidence
from entity_manager import EntityManager

class AI:

    def __init__(self):
        self.memory = KnowledgeBase()
        self.teacher = Teacher()
        self.reasoner = Reasoner()
        self.sources = SourceManager()
        self.evidence = Evidence()
        self.current_source = "Dustin"
        self.entities = EntityManager()
        
    def process(self, sentence):

        sentence = sentence.strip()

        # Question?
        if sentence.lower().startswith("what is"):

            subject = (
                sentence[7:]
                .replace("?", "")
                .strip()
                .lower()
            )

            return self.ask(subject)

        # Otherwise...
        return self.teach(sentence)

    def ask(self, subject):

        facts = self.memory.find_facts(subject)
        
        all_facts = self.memory.facts
        
        inferred = self.reasoner.infer(all_facts)
        
        facts.extend(
            [
                fact
                for fact in inferred
                if fact["subject"] == subject
            ]
        )

        if not facts:
            return "I don't know. (ai.py L48)"

        answers = []

        for fact in facts:

            subject = fact["subject"]
            relationship = fact["relationship"]
            obj = fact["object"]

            source = fact.get("source", "Unknown")
            confidence = fact.get("confidence", 0)
            
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
                article = "an" if obj[0].lower() in "aeiou" else "a"
                sentence = f"A {subject} is {article} {obj}."
                
            elif relationship == "has":
                sentence = f"A {subject} has {obj}."
                
            elif relationship == "can":
                sentence = f"A {subject} can {obj}."    

            elif relationship == "is_not_a":
                article = "an" if obj[0].lower() in "aeiou" else "a"
                sentence = f"A {subject} is {article} {obj}."

            else:
                sentence = f"{subject} {relationship} {obj}."

            answers.append(
                f"{sentence} "
                f"(Source: {source}, "
                f"Confidence: {confidence*100:.0f}%, "
                f"Reliability: {reliability*100:.0f}%, "
                f"Evidence: {evidence*100:.0f}%)"
            )

        return "\n".join(answers)

    def teach(self, sentence):

        fact = self.teacher.parse(sentence)

        if fact is None:
            return "I don't understand. (ai.py L87)"

        subject, relationship, obj = fact
        
        conflict = self.memory.find_conflict(
            subject,
            relationship,
            obj
        )
        
        if conflict:
            
            return (
                "I found conflicting knowledge.(ai.py L100)\n"
                f"Existing: {conflict['subject']} "
                f"{conflict['relationship']} "
                f"{conflict['object']}\n"
                f"Source: {conflict['source']}"
            )
        self.entities.add_entity(subject)
        self.entities.add_entity(obj)
        
        self.memory.add_fact(
            subject,
            relationship,
            obj,
            source=self.current_source,
            confidence=1.0,
            fact_type="learned"
        )

        return "I learned something new. (ai.py L107-L116)"