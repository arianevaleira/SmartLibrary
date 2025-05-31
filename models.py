from pydantic import BaseModel 
from typing import List 
from datetime import date

class Usuario(BaseModel):
    uuid: int
    matricula: int
    senha: str
    tipo: str 

class Livro(BaseModel):
    uuid: int 
    titulo: str 
    ano: int 
    autor: str
    edicao: str 


class Armario(BaseModel):
    uuid: int
    numero: int

class Sala(BaseModel):
    uuid: int
    numero: str
    capacidade: int

class Emprestimo(BaseModel):
    uuid: int
    usuario: Usuario
    livro: Livro
    armario: Armario
    

