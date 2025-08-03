from fastapi import FastAPI, HTTPException, Depends
from typing import List, Optional
import uuid
from datetime import date
from enum import Enum
import sqlite3
import requests
from pydantic import BaseModel

app = FastAPI()
DATABASE_URL = "biblioteca.db"
SUAP_API_URL = "https://suap.ifrn.edu.br/api/v2"

class TipoUsuario(str, Enum):
    aluno = "aluno"
    funcionario = "funcionario"
    admin = "admin"

class StatusLivro(str, Enum):
    disponivel = "disponível"
    emprestado = "emprestado"
    reservado = "reservado"

class Usuario(BaseModel):
    uuid: Optional[str] = None
    matricula: str
    nome: str
    email: str
    senha: str
    tipo: TipoUsuario

class Livro(BaseModel):
    uuid: Optional[str] = None
    titulo: str 
    ano: int 
    autor: str
    edicao: str
    status: StatusLivro = StatusLivro.disponivel
    isbn: Optional[str] = None

class Armario(BaseModel):
    uuid: Optional[str] = None
    numero: int
    capacidade: int

class Sala(BaseModel):
    uuid: Optional[str] = None
    numero: str
    capacidade: int
    descricao: Optional[str] = None

class Emprestimo(BaseModel):
    uuid: Optional[str] = None
    usuario_uuid: str
    livro_uuid: str
    armario_uuid: Optional[str] = None
    data_emprestimo: date
    data_devolucao_prevista: date
    data_devolucao: Optional[date] = None
    status: str = "ativo"

# Database setup
def get_db():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with sqlite3.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            uuid TEXT PRIMARY KEY,
            matricula TEXT NOT NULL UNIQUE,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL
        )""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            uuid TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            ano INTEGER NOT NULL,
            autor TEXT NOT NULL,
            edicao TEXT NOT NULL,
            status TEXT NOT NULL,
            isbn TEXT
        )""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS armarios (
            uuid TEXT PRIMARY KEY,
            numero INTEGER NOT NULL UNIQUE,
            capacidade INTEGER NOT NULL
        )""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS salas (
            uuid TEXT PRIMARY KEY,
            numero TEXT NOT NULL UNIQUE,
            capacidade INTEGER NOT NULL,
            descricao TEXT
        )""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS emprestimos (
            uuid TEXT PRIMARY KEY,
            usuario_uuid TEXT NOT NULL,
            livro_uuid TEXT NOT NULL,
            armario_uuid TEXT,
            data_emprestimo TEXT NOT NULL,
            data_devolucao_prevista TEXT NOT NULL,
            data_devolucao TEXT,
            status TEXT NOT NULL,
            FOREIGN KEY (usuario_uuid) REFERENCES usuarios (uuid),
            FOREIGN KEY (livro_uuid) REFERENCES livros (uuid),
            FOREIGN KEY (armario_uuid) REFERENCES armarios (uuid)
        )""")
        
        conn.commit()

init_db()


def get_suap_user_data(matricula: str, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{SUAP_API_URL}/minhas-informacoes/meus-dados/", headers=headers)
        response.raise_for_status()
        user_data = response.json()
        
        if str(user_data.get("matricula")) != str(matricula):
            raise HTTPException(status_code=403, detail="Matrícula não corresponde ao token")
        
        tipo = TipoUsuario.aluno
        if user_data.get("tipo_vinculo") == "Servidor":
            tipo = TipoUsuario.funcionario
        
        return {
            "nome": user_data.get("nome_usual") or user_data.get("nome"),
            "matricula": matricula,
            "tipo": tipo
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Erro ao acessar SUAP: {str(e)}")


@app.post("/usuarios/", response_model=Usuario)
def criar_usuario(usuario: Usuario, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    usuario.uuid = str(uuid.uuid4())
    
    cursor.execute(
        "INSERT INTO usuarios VALUES (?, ?, ?, ?, ?, ?)",
        (usuario.uuid, usuario.matricula, usuario.nome, usuario.email, usuario.senha, usuario.tipo.value)
    )
    db.commit()
    return usuario

@app.post("/usuarios/suap/", response_model=Usuario)
def criar_usuario_suap(matricula: str, token: str, senha: str, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE matricula = ?", (matricula,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Usuário já cadastrado")
    
    suap_data = get_suap_user_data(matricula, token)
    usuario = Usuario(
        uuid=str(uuid.uuid4()),
        matricula=matricula,
        nome=suap_data["nome"],
        senha=senha,
        tipo=suap_data["tipo"]
    )
    
    cursor.execute(
        "INSERT INTO usuarios VALUES (?, ?, ?, ?, ?)",
        (usuario.uuid, usuario.matricula, usuario.nome, usuario.senha, usuario.tipo.value)
    )
    db.commit()
    return usuario

@app.get("/usuarios/", response_model=List[Usuario])
def listar_usuarios(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios")
    return [Usuario(**dict(row)) for row in cursor.fetchall()]

@app.get("/usuarios/{uuid}", response_model=Usuario)
def obter_usuario(uuid: str, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE uuid = ?", (uuid,))
    usuario = cursor.fetchone()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return Usuario(**dict(usuario))

@app.post("/livros/", response_model=Livro)
def criar_livro(livro: Livro, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    livro.uuid = str(uuid.uuid4())
    
    cursor.execute(
        "INSERT INTO livros VALUES (?, ?, ?, ?, ?, ?, ?)",
        (livro.uuid, livro.titulo, livro.ano, livro.autor, livro.edicao, livro.status.value, livro.isbn)
    )
    db.commit()
    return livro

@app.get("/livros/", response_model=List[Livro])
def listar_livros(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM livros")
    return [Livro(**dict(row)) for row in cursor.fetchall()]

@app.get("/livros/{uuid}", response_model=Livro)
def obter_livro(uuid: str, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM livros WHERE uuid = ?", (uuid,))
    livro = cursor.fetchone()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return Livro(**dict(livro))

@app.put("/livros/{uuid}", response_model=Livro)
def atualizar_livro(uuid: str, livro: Livro, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    livro.uuid = uuid
    
    cursor.execute(
        """UPDATE livros SET 
        titulo = ?, ano = ?, autor = ?, edicao = ?, status = ?, isbn = ?
        WHERE uuid = ?""",
        (livro.titulo, livro.ano, livro.autor, livro.edicao, livro.status.value, livro.isbn, uuid)
    )
    db.commit()
    return livro

@app.post("/armarios/", response_model=Armario)
def criar_armario(armario: Armario, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    armario.uuid = str(uuid.uuid4())
    
    cursor.execute(
        "INSERT INTO armarios VALUES (?, ?, ?)",
        (armario.uuid, armario.numero, armario.capacidade)
    )
    db.commit()
    return armario

@app.get("/armarios/", response_model=List[Armario])
def listar_armarios(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM armarios")
    return [Armario(**dict(row)) for row in cursor.fetchall()]

@app.post("/salas/", response_model=Sala)
def criar_sala(sala: Sala, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    sala.uuid = str(uuid.uuid4())
    
    cursor.execute(
        "INSERT INTO salas VALUES (?, ?, ?, ?)",
        (sala.uuid, sala.numero, sala.capacidade, sala.descricao)
    )
    db.commit()
    return sala

@app.get("/salas/", response_model=List[Sala])
def listar_salas(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM salas")
    return [Sala(**dict(row)) for row in cursor.fetchall()]

@app.post("/emprestimos/", response_model=Emprestimo)
def criar_emprestimo(emprestimo: Emprestimo, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    emprestimo.uuid = str(uuid.uuid4())
    
    cursor.execute("SELECT status FROM livros WHERE uuid = ?", (emprestimo.livro_uuid,))
    livro = cursor.fetchone()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    if livro["status"] != StatusLivro.disponivel.value:
        raise HTTPException(status_code=400, detail="Livro não está disponível para empréstimo")
    
    cursor.execute("SELECT uuid FROM usuarios WHERE uuid = ?", (emprestimo.usuario_uuid,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if emprestimo.armario_uuid:
        cursor.execute("SELECT uuid FROM armarios WHERE uuid = ?", (emprestimo.armario_uuid,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Armário não encontrado")
    
    cursor.execute(
        "INSERT INTO emprestimos VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (emprestimo.uuid, emprestimo.usuario_uuid, emprestimo.livro_uuid, emprestimo.armario_uuid,
         emprestimo.data_emprestimo.isoformat(), emprestimo.data_devolucao_prevista.isoformat(),
         emprestimo.data_devolucao.isoformat() if emprestimo.data_devolucao else None,
         emprestimo.status)
    )
    
    cursor.execute(
        "UPDATE livros SET status = ? WHERE uuid = ?",
        (StatusLivro.emprestado.value, emprestimo.livro_uuid)
    )
    
    db.commit()
    return emprestimo

@app.put("/emprestimos/{uuid}/devolver", response_model=Emprestimo)
def devolver_livro(uuid: str, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM emprestimos WHERE uuid = ?", (uuid,))
    emprestimo = cursor.fetchone()
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    
    if emprestimo["status"] != "ativo":
        raise HTTPException(status_code=400, detail="Empréstimo já finalizado")
    
    cursor.execute(
        """UPDATE emprestimos SET 
        status = 'finalizado', data_devolucao = ?
        WHERE uuid = ?""",
        (date.today().isoformat(), uuid)
    )
    
    cursor.execute(
        "UPDATE livros SET status = ? WHERE uuid = ?",
        (StatusLivro.disponivel.value, emprestimo["livro_uuid"])
    )
    
    db.commit()
    
    cursor.execute("SELECT * FROM emprestimos WHERE uuid = ?", (uuid,))
    return Emprestimo(**dict(cursor.fetchone()))

@app.get("/emprestimos/", response_model=List[Emprestimo])
def listar_emprestimos(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM emprestimos")
    return [Emprestimo(**dict(row)) for row in cursor.fetchall()]


@app.get("/emprestimos/{uuid}", response_model=Emprestimo)
def obter_emprestimo(uuid: str, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM emprestimos WHERE uuid = ?", (uuid,))
    emprestimo = cursor.fetchone()
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    return Emprestimo(**dict(emprestimo))

@app.get("/livros/{uuid}/localizacao")
def localizar_livro(uuid: str, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM livros WHERE uuid = ?", (uuid,))
    livro = cursor.fetchone()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    if livro["status"] == StatusLivro.emprestado.value:
        cursor.execute(
            """SELECT * FROM emprestimos 
            WHERE livro_uuid = ? AND status = 'ativo'""",
            (uuid,)
        )
        emprestimo = cursor.fetchone()
        
        if emprestimo:
            cursor.execute("SELECT * FROM usuarios WHERE uuid = ?", (emprestimo["usuario_uuid"],))
            usuario = cursor.fetchone()
            
            armario = None
            if emprestimo["armario_uuid"]:
                cursor.execute("SELECT * FROM armarios WHERE uuid = ?", (emprestimo["armario_uuid"],))
                armario = cursor.fetchone()
            
            return {
                "status": "emprestado",
                "usuario": dict(usuario) if usuario else None,
                "armario": dict(armario) if armario else None,
                "data_devolucao": emprestimo["data_devolucao_prevista"]
            }
    
    return {"status": livro["status"]}