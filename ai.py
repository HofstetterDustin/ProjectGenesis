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
        self.memory.update_fact_scopes(self.entities.entities)
        self.teacher = Teacher()
        
    def process(self, sentence):

        sentence = sentence.strip()
        question = sentence.lower()
        #Question pattern: Is/Are [subject] a/an [category]?
        if question.startswith("is ") or question.startswith("are "):
            words = question.rstrip("?").split()
            if words[0] == "is":
                subject_start = 1
            else:
                subject_start = 1
            #Locate the article separating subject and category.
            for index in range(subject_start + 1, len(words)):
                if words[index] in ("a", "an"):
                    subject = " ".join(words[subject_start:index])
                    object_name = " ".join(words[index + 1:])
                    if subject and object_name:
                        return self.answer_yes_no(
                            subject,
                            "is_a",
                            object_name
                        )
            return "I don't know how to interpret that question."
        # Question pattern: What do we know about [subject]?
        if question.startswith("why is "):
            claim = sentence[7:].rstrip("?").strip()
            return self.explain(claim)
            
        # Question pattern: What do we know about [subject]?
        prefix = "what do we know about "
        
        if question.startswith(prefix):
            subject = sentence[len(prefix):].rstrip("?").strip().lower()
            
            if subject.startswith("a "):
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
        #Identify other common question formats.
        question_words = (
            "is", "are", "am", "do", "does", "did", "can", "could", "will", "would", "should", "has", "have", "had", "who", "what", "where", "when", "how", "which"
        )
        first_word = question.split()[0] if question.split() else ""
        #Precent unsupported questions from becoming stored knowledge.
        if sentence.endswith("?") or first_word in question_words:
            return (
                "I recognize this as a question, "
                "but I don't know how to answer it yet. "
                "I did not save it as knowledge."
            )

        # Otherwise, treat the input as something to learn.
        return self.teach(sentence)

    #Yes/No/I don't know ability to answer questions.
    def answer_yes_no(self, subject, relationship, object_name):
        subject_id = self.entities.get_entity_id(subject)
        object_id = self.entities.get_entity_id(object_name)
        #Check whether both entities exist.
        if subject_id is None or object_id is None:
            return "I don't know."
        #Check directly stored knowledge.
        if self.memory.check_fact(subject_id, relationship, object_id):
            return "Yes."
        #Check for a directly stored contradiction.
        opposite_relationships = {
            "is_a": "is_not_a",
            "is_not_a" : "is_a" ,
            "can" : "can_not" ,
            "can_not" : "can"
        }
        opposite = opposite_relationships.get(relationship)
        if opposite and self.memory.check_fact(
            subject_id, opposite, object_id
        ):
            return "No."
        #Check conclusions produced by the reasoner.
        inferred = self.reasoner.infer(self.memory.facts)
        for fact in inferred:
            if(
                fact["subject_id"] == subject_id
                and fact["relationship"] == relationship
                and fact["object_id"] == object_id
            ):
                return "Yes."
        return "I don't know."
        
    def ask(self, subject):

        subject_id = self.entities.get_entity_id(subject)
        
        if subject_id is None:
            return "I don't know, no _id. | ask() ai.py"
            
        #Contains the facts associated with the subject
        facts = self.memory.find_facts(subject_id)
        
        #Contains the complete collection of stored facts for trace relationships between entities.
        all_facts = self.memory.facts
        
        #Gives the reasoner the stored facts & receives a separate collection of conclusions.
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
            scope = fact.get("scope", "unspecified")
            
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
                entity == self.entities.get_entity(subject)
                if entity and entity.get("entity_class") == "individual":
                    sentence = f"{subject.capitalize()} has {object_name}."
                else:
                    sentence = f"A {subject} has {object_name}."
            
            elif relationship == "has_property":
                entity = self.entities.get_entity(subject)
                if entity and entity.get("entity_class") == "individual":
                    sentence = f"{subject.capitalize()} is {object_name}."
                elif scope == "category_possible":
                    sentence = f"A {subject} may be {object_name}."
                else:
                    sentence = f"A {subject} is {object_name}."
                
            elif relationship == "has_not":
                entity = self.entities.get_entity(subject)
                if entity and entity.get("entity_class") == "individual":
                    sentence = f"{subject.capitalize()} has not {object_name}."
                else:
                    sentence = f"A {subject} has not {object_name}."
                
            elif relationship == "can":
                entity = self.entities.get_entity(subject)
                if entity and entity.get("entity_class") == "individual":
                    sentence = f"{subject.capitalize()} can {object_name}."
                else:
                    sentence = f"A {subject} can {object_name}."    
                
            elif relationship == "can_not":
                entity = self.entities.get_entity(subject)
                if entity and entity.get("entity_class") == "individual":
                    sentence = f"{subject.capitalize()} cannot {object_name}."
                else:
                    sentence = f"A {subject} cannot {object_name}."

            elif relationship == "is_not_a":
                article = "an" if object_name[0].lower() in "aeiou" else "a"
                entity = self.entities.get_entity(subject)
                if entity and entity.get("entity_class") == "individual":
                    sentence = f"{subject.capitalize()} is not {article} {object_name}."
                else:
                    sentence = f"A {subject} is not {article} {object_name}."
            else:
                sentence = f"{subject} {relationship} {object_name}."

            answers.append(
                f"{sentence} "
                f"(Source: {source}, "
                f"Confidence: {confidence*100:.0f}%, "
                f"Reliability: {reliability*100:.0f}%, "
                f"Evidence: {evidence*100:.0f}%, "
                f"Scope: {scope})"
            )

        return "\n\n".join(answers)
        
    def explain(self, claim):
        
        words = claim.lower().strip().split()
        
        # Remove an article before the subject, such as "a" or "an".
        if words and words[0] in ("a", "an"):
            words = words[1:]
            
        #Recognize claims such as "Rex an animal".
        if len(words) < 2:
            return "I cannot explain that claim yet."
            
        subject = words[0]
        object_name = " ".join(words[1:])
        
        subject_id = self.entities.get_entity_id(subject)
        object_id = self.entities.get_entity_id(object_name)
        
        if subject_id is None or object_id is None:
            return "I don't know enough to explain that claim."
        
        #Find the inferred conclusion.
        all_facts = self.memory.facts
        inferred = self.reasoner.infer(all_facts)
        
        conclusion = None
        
        for fact in inferred:
            if (
                fact["subject_id"] == subject_id
                and fact["relationship"] == "is_a"
                and fact["object_id"] == object_id
            ):
                conclusion = fact
                break
                
        if conclusion is None:
            return "I cannot find an inferred conclusion supporting that claim."
            
        # Retrieve the original facts supporting the conclusion.
        supporting_ids = conclusion.get("because", [])
        supporting_facts = []
        
        for fact_id in supporting_ids:
            for fact in all_facts:
                if fact.get("fact_id") == fact_id:
                    supporting_facts.append(fact)
                    break
                    
        if not supporting_facts:
            return "I found the conclusion, but not its supporting facts."
            
        # Format the supporting facts for the user.
        explanation = []
        
        for fact in supporting_facts:
            fact_subject = self.entities.get_entity_name(fact["subject_id"])
            fact_object = self.entities.get_entity_name(fact["object_id"])
            
            if fact["relationship"] == "is_a":
                article = "an" if fact_object[0].lower() in "aeiou" else "a"
                
                if self.entities.get_entity(fact_subject).get("entity_class") == "individual":
                    sentence = f"{fact_subject.capitalize()} is {article} {fact_object}."
                else:
                    subject_article = "an" if fact_subject[0].lower() in "aeiou" else "a"
                    sentence = f"{subject_article.capitalize()} {fact_subject} is {article} {fact_object}."
            else:
                sentence = f"{fact_subject} {fact['relationship']} {fact_object}."
                
            explanation.append(
                f"{sentence} (Fact ID: {fact['fact_id']}, Source: {fact.get('source', 'Unknown')})"
            )
            
        explanation.append(
            f"Therefore, PG26 infers that {subject} is {object_name}."
        )
        
        return "\n\n".join(explanation)
                    
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
        
        elif relationship in ("can", "can_not"):
            entity = self.entities.get_entity(subject)
            
            if entity and entity.get("entity_class") == "category":
                scope = "category_capability"
            elif entity and entity.get("entity_class") == "individual":
                scope = "individual_capability"
            else:
                scope = "unspecified"
                
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
        
        
        
        