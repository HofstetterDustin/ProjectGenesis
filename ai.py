from knowledge import KnowledgeBase
from teacher import Teacher
from reasoner import Reasoner

class AI:

    def __init__(self):
        self.memory = KnowledgeBase()
        self.teacher = Teacher()
        self.reasoner = Reasoner()

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
            return "I don't know."

        answers = []

        for fact in facts:

            subject = fact["subject"]
            relationship = fact["relationship"]
            obj = fact["object"]

            source = fact.get("source", "Unknown")
            confidence = fact.get("confidence", 0)
            
            if relationship == "is_a":
                sentence = f"A {subject} is a {obj}."
                
            elif relationship == "has":
                sentence = f"A {subject} has {obj}."
                
            elif relationship == "can":
                sentence = f"A {subject} can {obj}."    

            elif relationship == "is_not_a":
                sentence = f"A {subject} is not a {obj}."

            else:
                sentence = f"{subject} {relationship} {obj}."

            answers.append(
                f"{sentence} (Source: {source}, Confidence: {confidence*100:.0f}%)"
            )

        return "\n".join(answers)

    def teach(self, sentence):

        fact = self.teacher.parse(sentence)

        if fact is None:
            return "I don't understand."

        subject, relationship, obj = fact

        self.memory.add_fact(
            subject,
            relationship,
            obj,
            source="Dustin",
            confidence=1.0,
            fact_type="learned"
        )

        return "I learned something new."