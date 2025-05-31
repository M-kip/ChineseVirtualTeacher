# ChineseVirtualTeacher
Virtual assistant with RAG capabilities to help chinese students learn more efficiently. The system grounds itself with HSK1-3 textbook content when setting questions, presenting examples with the same flavour and level of difficulty as the HSK textbook.
The project makes use of the following technologies
- flask framework
- mongodb database
- google genai
- 
Capabilities
- vector search
- AI recommendations
- Generate sample questions,
- Create study plan for student according to hsk level

## PROJECT STRUCTURE
```your_project/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── recipe_service.py
│   ├── templates/
│   │   └── index.html
│   ├── static/
│   └── config.py
├── migrations/
├── tests/
│   └── test_basic.py
├── .env
├── requirements.txt
├── run.py
└── README.md```
