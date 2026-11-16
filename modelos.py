
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# ---------------------------------------------------------------------------
# TABELA ASSOCIATIVA (relação N:N entre Instrutor e Aluno)
# Um instrutor acompanha vários alunos e um aluno pode ter vários instrutores.
# ---------------------------------------------------------------------------
instrutor_aluno = Table(
    "instrutor_aluno",
    Base.metadata,
    Column("instrutor_id", Integer, ForeignKey("instrutor.id"), primary_key=True),
    Column("aluno_id", Integer, ForeignKey("aluno.id"), primary_key=True),
)


class Academia(Base):
    __tablename__ = "academia"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    endereco = Column(String(200))
    telefone = Column(String(20))

    # Relação 1:N -> uma academia tem vários alunos e vários instrutores
    alunos = relationship("Aluno", back_populates="academia")
    instrutores = relationship("Instrutor", back_populates="academia")

    def __repr__(self):
        return f"Academia({self.nome})"


class Aluno(Base):
    __tablename__ = "aluno"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    data_nasc = Column(Date)
    telefone = Column(String(20))
    matricula = Column(String(20), unique=True, nullable=False)
    data_matricula = Column(Date)
    plano = Column(String(20), default="Básico")
    status = Column(String(20), default="Ativado")

    # Chave estrangeira (lado "N" da relação 1:N com Academia)
    academia_id = Column(Integer, ForeignKey("academia.id"), nullable=False)

    academia = relationship("Academia", back_populates="alunos")
    fichas = relationship("FichaDeTreino", back_populates="aluno")
    # Relação N:N com Instrutor (usa a tabela associativa)
    instrutores = relationship(
        "Instrutor", secondary=instrutor_aluno, back_populates="alunos"
    )

    def __repr__(self):
        return f"Aluno({self.nome})"


class Instrutor(Base):
    __tablename__ = "instrutor"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    data_nasc = Column(Date)
    telefone = Column(String(20))
    especialidade = Column(String(50))
    cref = Column(String(20), unique=True)
    carga_horaria = Column(Integer)  # horas por semana

    academia_id = Column(Integer, ForeignKey("academia.id"), nullable=False)

    academia = relationship("Academia", back_populates="instrutores")
    alunos = relationship(
        "Aluno", secondary=instrutor_aluno, back_populates="instrutores"
    )

    def __repr__(self):
        return f"Instrutor({self.nome})"


class FichaDeTreino(Base):
    __tablename__ = "ficha_de_treino"

    id = Column(Integer, primary_key=True)
    data_criacao = Column(Date, nullable=False)
    objetivo = Column(String(100), nullable=False)

    # Chave estrangeira (lado "N" da relação 1:N com Aluno)
    aluno_id = Column(Integer, ForeignKey("aluno.id"), nullable=False)

    aluno = relationship("Aluno", back_populates="fichas")

    def __repr__(self):
        return f"Ficha({self.objetivo})"