from fastapi import FastAPI, HTTPException
from typing import List, Optional
import uuid
from datetime import date
from models import Usuario, Livro, Armario, Sala, Emprestimo, TipoUsuario, StatusLivro

app = FastAPI()

#Banco de Bincadeira
livros_db: List[Livro] = []
usuarios_db: List[Usuario] = []
armarios_db: List[Armario] = []
salas_db: List[Sala] = []
emprestimos_db: List[Emprestimo] = []


@app.post('/usuarios/', response_model=Usuario)
def cadastrar_usuario(usuario: Usuario):
    usuario.uuid = str(uuid.uuid4())
    usuarios_db.append(usuario)
    return usuario

@app.get('/usuarios/', response_model=List[Usuario])
def listar_usuarios():
    return usuarios_db

@app.get('/usuarios/{uuid}', response_model=Usuario)
def obter_usuario(uuid: str):
    for usuario in usuarios_db:
        if usuario.uuid == uuid:
            return usuario
    raise HTTPException(status_code=404, detail="Usuário não encontrado")


@app.post('/livros/', response_model=Livro)
def cadastrar_livro(livro: Livro):
    livro.uuid = str(uuid.uuid4())
    livro.status = StatusLivro.disponivel
    livros_db.append(livro)
    return livro

@app.get('/livros/', response_model=List[Livro])
def listar_livros():
    return livros_db

@app.get('/livros/{uuid}', response_model=Livro)
def obter_livro(uuid: str):
    for livro in livros_db:
        if livro.uuid == uuid:
            return livro
    raise HTTPException(status_code=404, detail="Livro não encontrado")

@app.put('/livros/{uuid}', response_model=Livro)
def atualizar_livro(uuid: str, livro_atualizado: Livro):
    for index, livro in enumerate(livros_db):
        if livro.uuid == uuid:
            livro_atualizado.uuid = uuid 
            livros_db[index] = livro_atualizado
            return livro_atualizado
    raise HTTPException(status_code=404, detail="Livro não encontrado")

@app.post('/armarios/', response_model=Armario)
def cadastrar_armario(armario: Armario):
    armario.uuid = str(uuid.uuid4())
    armarios_db.append(armario)
    return armario

@app.get('/armarios/', response_model=List[Armario])
def listar_armarios():
    return armarios_db

@app.get('/armarios/{uuid}', response_model=Armario)
def obter_armario(uuid: str):
    for armario in armarios_db:
        if armario.uuid == uuid:
            return armario
    raise HTTPException(status_code=404, detail="Armário não encontrado")


@app.post('/salas/', response_model=Sala)
def cadastrar_sala(sala: Sala):
    sala.uuid = str(uuid.uuid4())
    salas_db.append(sala)
    return sala

@app.get('/salas/', response_model=List[Sala])
def listar_salas():
    return salas_db

@app.get('/salas/{uuid}', response_model=Sala)
def obter_sala(uuid: str):
    for sala in salas_db:
        if sala.uuid == uuid:
            return sala
    raise HTTPException(status_code=404, detail="Sala não encontrada")

@app.post('/emprestimos/', response_model=Emprestimo)
def registrar_emprestimo(emprestimo: Emprestimo):
    usuario_existe = any(u.uuid == emprestimo.usuario_uuid for u in usuarios_db)
    if not usuario_existe:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
    livro_existe = next((l for l in livros_db if l.uuid == emprestimo.livro_uuid), None)
    if not livro_existe:
        raise HTTPException(status_code=400, detail="Livro não encontrado")
    if emprestimo.armario_uuid:
        armario_existe = any(a.uuid == emprestimo.armario_uuid for a in armarios_db)
        if not armario_existe:
            raise HTTPException(status_code=400, detail="Armário não encontrado")
    livro_existe.status = StatusLivro.emprestado
    emprestimo.uuid = str(uuid.uuid4())
    emprestimos_db.append(emprestimo)
    return emprestimo

@app.get('/emprestimos/', response_model=List[Emprestimo])
def listar_emprestimos():
    return emprestimos_db

@app.get('/emprestimos/{uuid}', response_model=Emprestimo)
def obter_emprestimo(uuid: str):
    for emprestimo in emprestimos_db:
        if emprestimo.uuid == uuid:
            return emprestimo
    raise HTTPException(status_code=404, detail="Empréstimo não encontrado")

@app.put('/emprestimos/{uuid}/devolver')
def devolver_livro(uuid: str):
    emprestimo = next((e for e in emprestimos_db if e.uuid == uuid), None)
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    
 
    emprestimo.status = "finalizado"
    emprestimo.data_devolucao = date.today()

    livro = next((l for l in livros_db if l.uuid == emprestimo.livro_uuid), None)
    if livro:
        livro.status = StatusLivro.disponivel
    
    return {"message": "Livro devolvido com sucesso"}


@app.get('/livros/{uuid}/localizacao')
def localizar_livro(uuid: str):
    livro = next((l for l in livros_db if l.uuid == uuid), None)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    if livro.status == StatusLivro.emprestado:
        emprestimo = next((e for e in emprestimos_db 
                         if e.livro_uuid == uuid and e.status == "ativo"), None)
        if emprestimo:
            usuario = next((u for u in usuarios_db if u.uuid == emprestimo.usuario_uuid), None)
            armario = next((a for a in armarios_db if a.uuid == emprestimo.armario_uuid), None) if emprestimo.armario_uuid else None
            
            return {
                "status": "emprestado",
                "usuario": usuario,
                "armario": armario,
                "data_devolucao": emprestimo.data_devolucao_prevista
            }
    
    return {"status": livro.status.value}


@app.get('/busca/')
def busca_avancada(
    titulo: Optional[str] = None,
    autor: Optional[str] = None,
    status_livro: Optional[StatusLivro] = None,
    tipo_usuario: Optional[TipoUsuario] = None,
    numero_sala: Optional[str] = None
):
    resultados = {
        "livros": livros_db,
        "usuarios": usuarios_db,
        "salas": salas_db
    }
    if titulo:
        resultados["livros"] = [l for l in resultados["livros"] if titulo.lower() in l.titulo.lower()]
    
    if autor:
        resultados["livros"] = [l for l in resultados["livros"] if autor.lower() in l.autor.lower()]
    
    if status_livro:
        resultados["livros"] = [l for l in resultados["livros"] if l.status == status_livro]
    
    if tipo_usuario:
        resultados["usuarios"] = [u for u in resultados["usuarios"] if u.tipo == tipo_usuario]
    
    if numero_sala:
        resultados["salas"] = [s for s in resultados["salas"] if numero_sala in s.numero]
    
    return resultados
