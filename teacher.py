class Teacher:

    def parse(self, sentence):

        sentence = sentence.lower().strip()

        if sentence.endswith("."):
            sentence = sentence[:-1]

        words = sentence.split()

        "Remove a at the beginning"
        if words[0] == "a" or words[0] == "an":
            words = words[1:]
            
        "Pattern: Dog is an animal"
        if len(words) >= 4 and words[1] == "is":
            
            subject = words[0]
            relationship = "is_a"
            
            if words[2] == "a" or words[2] == "an":
                object = " ".join(words[3:])
                return subject, relationship, object
                
        "Pattern: dog has four legs"
        if len(words) >= 3 and words[1] == "has":
            
            subject = words[0]
            relationship = "has"
            object = " ".join(words[2:])

            return subject, relationship, object
            
        "Pattern: bird can fly"    
        if len(words) >= 3 and words[1] == "can":
            
            subject = words[0]
            relationship = "can"
            object = " ".join(words[2:])
            
            return subject, relationship, object

        return None