from peewee import *
import os

arq = 'universidade.db'
db = SqliteDatabase(arq)

class BaseModel(Model):
    class Meta:
        database = db

class Aluno(BaseModel):
    matricula = IntegerField()
    nome = CharField()
    idade = IntegerField()

    def __str__(self):
        return self.nome + ' (' + str(self.matricula) + ' ) de ' + str(self.idade)

class Disciplina(BaseModel):
    cod_disciplina = IntegerField()
    den_disciplina = CharField()

    def __str__(self):
        return self.den_disciplina

class Turma(BaseModel):
    cod_turma = IntegerField()
    alunos = ManyToManyField(Aluno)
    disciplina = ForeignKeyField(Disciplina)

    def __str__(self):
        return str(self.cod_turma) + ' ' + str(self.alunos) + ' ' + str(self.disciplina)

class Titulacao(BaseModel):
    id_titulacao = IntegerField()
    den_titulacao = CharField()

    def __str__(self):
        return self.den_titulacao

class Professor(BaseModel):
    cod_professor = IntegerField()
    nome_professor = CharField()
    disciplinas = ManyToManyField(Disciplina)
    titulo = ForeignKeyField(Titulacao)

    def __str__(self):
        return self.nome_professor + " tem " + str(self.titulo) + ' leciona ' + str(self.disciplinas)

class Campus(BaseModel):
    cod_campus = IntegerField()
    nome_campus = CharField()
    endereco = CharField()

    def __str__(self):
        return self.nome_campus + ' localizado em ' + self.endereco

class SalaDeAula(BaseModel):
    cod_sala = IntegerField()
    campus = ForeignKeyField(Campus)
    disciplinas = ManyToManyField(Disciplina)

    def __str__(self):
        return 'Localizada no Campus ' + str(self.campus) + ' e ' + str(self.disciplinas) + ' são lecionadas lá.'
         
class Servidor(BaseModel):
    cpf_servidor = IntegerField()
    nome_servidor = CharField()
    idade = IntegerField()
    cargo = CharField()
    campus = ForeignKeyField(Campus)

    def __str__(self):
        return self.nome_servidor + ' tem ' + str(self.idade) + ' é ' + self.cargo + ' no campus ' + str(self.campus) 

class Curso(BaseModel):
    id_curso = IntegerField()
    den_curso = CharField()
    disciplinas = ManyToManyField(Disciplina)

    def __str__(self):
        return 'O curso de ' + self.den_curso + ' tem ' + str(self.disciplinas) + ' como disciplinas.'

class CoordenacaoCurso(BaseModel):
    curso = ForeignKeyField(Curso)
    professor = ForeignKeyField(Professor)
    
    def __str__(self):
        return str(self.professor) + ' é coordenador(a) do curso de ' + str(curso)

if __name__ == "__main__":
    
    if os.path.exists(arq):
        os.remove(arq)
    
    try:
        db.connect()
        db.create_tables([Aluno,
                          Disciplina,
                          Turma,
                          Turma.alunos.get_through_model(),
                          Titulacao,
                          Professor,
                          Professor.disciplinas.get_through_model(),
                          Campus,
                          SalaDeAula,
                          SalaDeAula.disciplinas.get_through_model(),
                          Servidor,
                          Curso,
                          Curso.disciplinas.get_through_model(),
                          CoordenacaoCurso])
    
    except OperationalError as e:
        print('erros: ' + str(e))


    leandro = Aluno.create(matricula=123, nome='Leandro', idade=18)
    julia = Aluno.create(matricula=321, nome='Júlia', idade=18)

    programacaoII = Disciplina.create(cod_disciplina=789, den_disciplina='Programação II')

    info_302 = Turma.create(cod_turma=302, disciplina=programacaoII)
    info_302.alunos.add(leandro)
    info_302.alunos.add(julia)

    mestrado = Titulacao.create(id_titulacao=1, den_titulacao='Mestrado')

    hylson = Professor.create(cod_professor=12312, nome_professor='Hylson', titulo=mestrado)
    hylson.disciplinas.add(programacaoII)

    ifc_blumenau = Campus.create(cod_campus=1111, nome_campus='IFC Campus de Blumenau', endereco='R. Bernardino José de Oliveira, 81 - Badenfurt, Blumenau - SC, 89070-270')
    
    sala_C08 = SalaDeAula.create(cod_sala=165, campus=ifc_blumenau)
    sala_C08.disciplinas.add(programacaoII)

    luiz = Servidor.create(cpf_servidor=7587, nome_servidor='Luiz do SISAE', idade=28, cargo="Assistente de Alunos", campus=ifc_blumenau)

    informatica = Curso.create(id_curso=45648, den_curso='Técnico em Informática')
    informatica.disciplinas.add(informatica)

    coordenacao_informatica = CoordenacaoCurso.create(curso=informatica, professor=hylson)

    print(info_302)
    print('')
    print(sala_C08)
    print('')
    print(luiz)
    print('')
    print(informatica)