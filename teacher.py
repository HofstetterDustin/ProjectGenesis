class Teacher:

    def parse(self, sentence):

        sentence = sentence.lower().strip()

        if sentence.endswith("."):
            sentence = sentence[:-1]

        words = sentence.split()
        
        if not words:
            return None
            
        # Pattern: subject | relationship = IS/IS_NOT | object
        if "is" in words:
            is_index = words.index("is")
            
            #Pattern: subject IS_NOT a/an something
            if (
                is_index + 2 < len(words)
                and words[is_index +1] == "not"
                and is_index +3 < len(words)
                and words[is_index + 2] in ("a", "an")
            ):
                subject = " ".join(words[:is_index])
                relationship = "is_not_a"
                object = " ".join(words[is_index +3:])
                
                if subject and object:
                    return subject, relationship, object
            
            #Pattern: subject IS a/an something
            if (
                is_index +1 < len(words)
                and is_index +1 < len(words)
                and words[is_index +1] in ("a", "an")
                and is_index +2 < len(words)
            ):
                subject = " ".join(words[:is_index])
                relationship = "is_a"
                object = " ".join(words[is_index +2:])
                
                if subject and object:
                    return subject, relationship, object
                    
        #Pattern: subject | relationship = HAS/HAS_NOT | object
        if "has" in words:
            has_index = words.index("has")
            
            subject = " ".join(words[:has_index])
            
            #Pattern: subject HAS NOT a/an something
            if (
                has_index +1 < len(words)
                and words[has_index +1] == "not"
            ):    
                relationship = "has_not"
                object = " ".join(words[has_index +2:])
            else:
                relationship = "has"
                object = " ".join(words[has_index + 1:])
                
            if subject and object:
                return subject, relationship, object
                    
                
            # Pattern: subject HAS something
            if "has" in words:
                has_index = words.index("has")
                
                subject = " ".join(words[:has_index])
                relationship = "has_a"
                object = " ".join(words[has_index + 1:])

                if subject and object:
                    return subject, "has", object
                    
        #Pattern: subject | relationship = CAN/CAN_NOT | object
        if "can" in words:
            can_index = words.index("can")
            
            subject = " ".join(words[:can_index])

            #Pattern: subject CAN_NOT do something
            if (
                can_index + 1 < len(words)
                and words[can_index +1] == "not"
            ):
                relationship = "can_not"
                object = " ".join(words[can_index + 2:])
            else:
                relationship = "can"
                object = " ".join(words[can_index + 1:])
                
            if subject and object:
                return subject, relationship, object
            
        #Pattern: subject IS a descriptive property
        if "is" in words:
            is_index = words.index("is")
            
            subject = " ".join(words[:is_index])
            property_value = " ".join(words[is_index + 1:])
            
            if (
                subject
                and property_value
                and property_value not in ("a", "an")
            ):
                relationship = "has_property"
                object = property_value
                
                return subject, relationship, object