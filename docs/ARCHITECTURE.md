ProjectGenesis

main.py
│
├── Starts Genesis
│
└── Handles conversation


ai.py
│
├── Decides what action to take
│
├── Uses Teacher
│
├── Uses KnowledgeBase
│
└── Uses Reasoner


teacher.py
│
└── Converts English → Facts


knowledge.py
│
└── Stores Facts


reasoner.py
│
└── Creates Conclusions


knowledge.json
│
└── Long-term Memory