from fastapi import FastAPI, HTTPException
from typing import List
import uuid
from datetime import date
from models import Usuario, Livro, Armario, Sala, Emprestimo

app = FastAPI() 

#Criar os endpointes 
livro:list[Livro] = [] 
usuaio:list[Usuario] = []
armario:list[Armario] = []