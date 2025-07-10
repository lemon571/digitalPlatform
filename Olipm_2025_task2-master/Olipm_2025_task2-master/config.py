class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:admin@db:5432/education_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER = {
        'title': 'Education API',
        'uiversion': 3
    }
