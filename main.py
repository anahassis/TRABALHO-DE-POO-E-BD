"""
main.py
Cria o banco, insere os dados de exemplo e executa as 3 consultas.

Para instalar a biblioteca:  pip install sqlalchemy
Para executar:               python main.py
(main.py e modelos.py precisam estar na mesma pasta)
"""

from datetime import date

from sqlalchemy import create_engine, select, func, desc
from sqlalchemy.orm import sessionmaker

from modelos import Base, Academia, Aluno, Instrutor, FichaDeTreino

# ---------------------------------------------------------------------------
# Criando a conexão e as tabelas
# ---------------------------------------------------------------------------
engine = create_engine('sqlite:///academia.db')

# Apaga e recria as tabelas: assim podemos executar de novo sem duplicar registros
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# ---------------------------------------------------------------------------
# Populando as tabelas
# ---------------------------------------------------------------------------

# Academias
academia1 = Academia(nome='Academia Forma Fit', endereco='Rua das Flores, 100', telefone='(31) 3333-1111')
academia2 = Academia(nome='Academia Corpo em Ação', endereco='Av. Brasil, 500', telefone='(31) 3333-2222')

# Instrutores: cada um aponta para UMA academia (1:N)
carlos = Instrutor(nome='Carlos Mendes', cpf='111.111.111-11', especialidade='Musculação',
                   cref='CREF-001', academia=academia1)
juliana = Instrutor(nome='Juliana Prado', cpf='222.222.222-22', especialidade='Funcional',
                    cref='CREF-002', academia=academia1)
rafael = Instrutor(nome='Rafael Souza', cpf='333.333.333-33', especialidade='Emagrecimento',
                   cref='CREF-003', academia=academia2)

# Alunos: cada um aponta para UMA academia (1:N) e recebe uma LISTA de instrutores (N:N)
ana = Aluno(nome='Ana Costa', cpf='444.444.444-44', matricula='M001', plano='Avançado',
            academia=academia1, instrutores=[carlos])
bruno = Aluno(nome='Bruno Lima', cpf='555.555.555-55', matricula='M002', plano='Básico',
              academia=academia1, instrutores=[carlos, juliana])   # dois instrutores
carla = Aluno(nome='Carla Rocha', cpf='666.666.666-66', matricula='M003', plano='Médio',
              academia=academia1, instrutores=[carlos])
diego = Aluno(nome='Diego Alves', cpf='777.777.777-77', matricula='M004', plano='Médio',
              academia=academia2, instrutores=[rafael])

# Fichas de treino: cada uma aponta para UM aluno (1:N)
fichas = [
    FichaDeTreino(data_criacao=date(2026, 1, 12), objetivo='Hipertrofia', aluno=ana),
    FichaDeTreino(data_criacao=date(2026, 6, 1), objetivo='Definição muscular', aluno=ana),
    FichaDeTreino(data_criacao=date(2026, 2, 8), objetivo='Condicionamento físico', aluno=bruno),
    FichaDeTreino(data_criacao=date(2026, 4, 5), objetivo='Emagrecimento', aluno=diego),
]

session.add_all([academia1, academia2, carlos, juliana, rafael, ana, bruno, carla, diego])
session.add_all(fichas)
session.commit()

# ---------------------------------------------------------------------------
# Consulta 1: fichas de treino da aluna Ana Costa (JOIN 1:N com filtro)
# ---------------------------------------------------------------------------
print('Consulta 1: fichas de treino da Ana Costa')
query = (
    select(FichaDeTreino.objetivo, FichaDeTreino.data_criacao)
    .join(FichaDeTreino.aluno)
    .where(Aluno.nome == 'Ana Costa')
)
for linha in session.execute(query):
    print(linha.data_criacao, '-', linha.objetivo)

# ---------------------------------------------------------------------------
# Consulta 2: alunos do instrutor Carlos Mendes (JOIN N:N com filtro)
# ---------------------------------------------------------------------------
print('\nConsulta 2: alunos do instrutor Carlos Mendes')
query = (
    select(Aluno.nome)
    .join(Aluno.instrutores)
    .where(Instrutor.nome == 'Carlos Mendes')
)
for linha in session.execute(query):
    print(linha.nome)

# ---------------------------------------------------------------------------
# Consulta 3: quantidade de alunos em cada academia, da maior para a menor
# (JOIN 1:N com agrupamento)
# ---------------------------------------------------------------------------
print('\nConsulta 3: quantidade de alunos por academia')
query = (
    select(Academia.nome, func.count(Aluno.id).label('qtd'))
    .join(Academia.alunos)
    .group_by(Academia.nome)
    .order_by(desc('qtd'))
)
for linha in session.execute(query):
    print(linha.nome, '->', linha.qtd)

session.close()