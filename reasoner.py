class Reasoner:

    def infer(self, facts):

        conclusions = []

        for fact in facts:

            if fact["relationship"] != "is_a":
                continue

            self.follow_chain(
                fact["subject"],
                fact["object"],
                facts,
                conclusions,
                set()
            )

        return conclusions


    def follow_chain(
        self,
        subject,
        current,
        facts,
        conclusions,
        visited
    ):

        if current in visited:
            return

        visited.add(current)

        for fact in facts:

            if fact["relationship"] != "is_a":
                continue

            if fact["subject"] == current:

                conclusion = {
                    "subject": subject,
                    "relationship": "is_a",
                    "object": fact["object"],
                    "source": "Genesis",
                    "confidence": 0.9,
                    "type": "inference"
                }

                if conclusion not in conclusions:
                    conclusions.append(conclusion)

                self.follow_chain(
                    subject,
                    fact["object"],
                    facts,
                    conclusions,
                    visited.copy()
                )