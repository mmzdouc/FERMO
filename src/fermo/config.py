""" Flask configurations """

DEBUG = True
FLASK_ENV = 'development'
UPLOAD_FOLDER = 'src/fermo/uploads/'  # temporary until database is implemented
ALLOWED_EXTENSION = {'json', 'mgf', 'csv'}
# todo: secret key should be individual for every session
SECRET_KEY = "b'\x8e$V\xe220F|\xafLuw\x1d\xa9hKH`G\xd9\xb0\xea_R'"
