class Config:
    SECRET_KEY = 'your_secret_key_here'
    MONGO_URI = "mongodb://localhost:63894/?directConnection=true"
    MONGO_DBNAME = "chinese_virtual_teacher"
    DOC_DIRECTORY = r"C:\Users\mose\Documents\machine_learning\ChineseVirtualTeacher\books"
    MONGO_COLLECTION = "books"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
