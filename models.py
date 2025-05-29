from pydantic import BaseModel 
from typing import List 
from datetime import date

class Usuario(BaseModel):
    id: int
    matricula: int
    senha: str
    tipo: str 

class Livro(BaseModel):
    id: int 
    titulo: str 
    ano: int 
    autor: str
    edicao: str 


class Armario(BaseModel):
    id: int
    numero: int

class Sala(BaseModel):
    id: int
    numero: str
    capacidade: int

class Emprestimo(BaseModel):
    id: int
    usuario: Usuario
    livro: Livro
    armario: Armario
    

