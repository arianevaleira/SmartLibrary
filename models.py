from pydantic import BaseModel 
from typing import List, Optional
from datetime import date
from enum import Enum

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
    senha:str
    email: str 
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