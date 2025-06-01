# Chinese Virtual Teacher
Virtual assistant with RAG capabilities to help chinese students learn more efficiently. The system grounds itself with HSK1-3 textbook content when setting questions, presenting examples with the same flavour and level of difficulty as the HSK textbook.


**The project makes use of the following technologies**
- flask framework
- mongodb database
- google genai
- all-MiniLM-L6-v2 model


## Capabilities
- vector search
- AI recommendations
- Generate sample questions,
- Create study plan for student according to hsk level

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/M-kip/ChineseVirtualTeacher
   cd ChineseVirtualTeacher
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```
   flask --app run init-db
   ```

4. Run the development server:
   ```
   flask --app run run --debug
   ```

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
├── models/
│   ├── __init__.py
│   └──db.py
│   └──load_docs.py
│   └──vector_search.py
├── .env
├── requirements.txt
├── run.py
└── README.md
```

## License

MIT License. See LICENSE file for details.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## Credits

Built with:
- Django
- MongoDB Database
- Google generativeAI
- sentence-transformers/all-MiniLM-L6-v2
