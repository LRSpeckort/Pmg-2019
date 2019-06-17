from peewee import *
import os

db = SqliteDatabase('aluno.db')

class Aluno(Model):
    nome = CharField()
    idade = IntegerField() 

    class Meta():
        database = db

if __name__ == "__main__":
    arq = 'aluno.db'

    if os.path.exists(arq):
        os.remove(arq)

    try:
        db.connect()
        db.create_tables([Aluno])
    except OperationalError as e:
        print('Error')
    
