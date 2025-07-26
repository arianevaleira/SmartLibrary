import requests
import uuid
from datetime import datetime
from enum import Enum

UR = "http://localhost:8000"

class TipoUsuario(Enum):
    aluno = "aluno"
    professor = "professor"
    funcionario = "funcionario"

class StatusLivro(Enum):
    disponivel = "disponivel"
    emprestado = "emprestado"
    reservado = "reservado"
    indisponivel = "indisponivel"

def mostrar_menu_principal():
    print("\n=== Sistema de Biblioteca ===")
    print("1. Gerenciar Usuários")
    print("2. Gerenciar Livros")
    print("3. Gerenciar Armários")
    print("4. Gerenciar Salas")
    print("5. Gerenciar Empréstimos")
    print("6. Busca Avançada")
    print("0. Sair")
    return input("Escolha uma opção: ")

#mostrar_menu_principal()
def gerenciar_usuarios():
    while True:
        print("\n--- Gerenciamento de Usuários ---")
        print("1. Cadastrar novo usuário")
        print("2. Listar todos os usuários")
        print("3. Buscar usuário por ID")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            listar_usuarios()
        elif opcao == "3":
            buscar_usuario()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

def cadastrar_usuario():
    print("\n--- Cadastrar Novo Usuário ---")
    nome = input("Nome: ")
    email = input("Email: ")
    matricula = input("Matrícula: ") 
    senha = input("Senha: ")         
    print("Tipos disponíveis: aluno, professor, funcionario")
    tipo = input("Tipo: ")
    
    try:
        usuario = {
            "nome": nome,
            "email": email,
            "matricula": matricula,  
            "senha": senha,          
            "tipo": tipo,
            "uuid": str(uuid.uuid4())
        }
        response = requests.post(f"{UR}/usuarios/", json=usuario)
        if response.status_code == 200:
            print("Usuário cadastrado com sucesso!")
            print(response.json())
        else:
            print(f"Erro ao cadastrar usuário: {response.text}")
    except Exception as e:
        print(f"Erro: {e}")

def listar_usuarios():
    print("\n--- Lista de Usuários ---")
    try:
        response = requests.get(f"{UR}/usuarios/")
        if response.status_code == 200:
            usuarios = response.json()
            for usuario in usuarios:
                print(f"ID: {usuario['uuid']}")
                print(f"Nome: {usuario['nome']}")
                print(f"Email: {usuario['email']}")
                print(f"Tipo: {usuario['tipo']}")
                print("-" * 30)
        else:
            print(f"Erro ao listar usuários: {response.text}")
    except Exception as e:
        print(f"Erro: {e}")

def buscar_usuario():
    print("\n--- Buscar Usuário ---")
    user_id = input("Digite o ID do usuário: ").strip()
    
    try:
        response = requests.get(f"{UR}/usuarios/{user_id}")
        
        if response.status_code == 200:
            usuario = response.json()
            print("\n[Dados completos da API]", usuario)
            print("\nUsuário encontrado:")
            print(f"ID: {usuario.get('uuid')}")
            print(f"Nome: {usuario.get('nome')}")
            email = usuario.get('email')
            if email is not None:
                print(f"Email: {email}")
            else:
                print("Email: Não cadastrado")
            
            print(f"Tipo: {usuario.get('tipo', 'Não especificado')}")
            print(f"Matrícula: {usuario.get('matricula', 'Não cadastrada')}")
            
        elif response.status_code == 404:
            print("Usuário não encontrado.")
        else:
            print(f"Erro na API (Status {response.status_code}): {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {str(e)}")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")

def gerenciar_livros():
    while True:
        print("\n--- Gerenciamento de Livros ---")
        print("1. Cadastrar novo livro")
        print("2. Listar todos os livros")
        print("3. Buscar livro por ID")
        print("4. Atualizar livro")
        print("5. Localizar livro")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            cadastrar_livro()
        elif opcao == "2":
            listar_livros()
        elif opcao == "3":
            buscar_livro()
        elif opcao == "4":
            atualizar_livro()
        elif opcao == "5":
            localizar_livro()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

def cadastrar_livro():
    print("\n--- Cadastrar Novo Livro ---")
    titulo = input("Título: ")
    autor = input("Autor: ")
    ano_publicacao = input("Ano de publicação: ")
    editora = input("Editora: ")
    
    try:
        livro = {
            "titulo": titulo,
            "autor": autor,
            "ano_publicacao": ano_publicacao,
            "editora": editora,
            "status": "disponivel",
            "uuid": str(uuid.uuid4())
        }
        response = requests.post(f"{UR}/livros/", json=livro)
        if response.status_code == 200:
            print("Livro cadastrado com sucesso!")
            print(response.json())
        else:
            print(f"Erro ao cadastrar livro: {response.text}")
    except Exception as e:
        print(f"Erro: {e}")

def listar_livros():
    print("\n--- Lista de Livros ---")
    try:
        response = requests.get(f"{UR}/livros/")
        if response.status_code == 200:
            livros = response.json()
            for livro in livros:
                print(f"ID: {livro['uuid']}")
                print(f"Título: {livro['titulo']}")
                print(f"Autor: {livro['autor']}")
                print(f"Status: {livro['status']}")
                print("-" * 30)
        else:
            print(f"Erro ao listar livros: {response.text}")
    except Exception as e:
        print(f"Erro: {e}")

def buscar_livro():
    print("\n--- Buscar Livro ---")
    livro_id = input("Digite o ID do livro: ")
    try:
        response = requests.get(f"{UR}/livros/{livro_id}")
        if response.status_code == 200:
            livro = response.json()
            print("\nLivro encontrado:")
            print(f"ID: {livro['uuid']}")
            print(f"Título: {livro['titulo']}")
            print(f"Autor: {livro['autor']}")
            print(f"Ano: {livro['ano_publicacao']}")
            print(f"Editora: {livro['editora']}")
            print(f"Status: {livro['status']}")
        elif response.status_code == 404:
            print("Livro não encontrado.")
        else:
            print(f"Erro: {response.text}")
    except Exception as e:
        print(f"Erro: {e}")

def atualizar_livro():
    print("\n--- Atualizar Livro ---")
    livro_id = input("Digite o ID do livro a ser atualizado: ")
    
    try: 
        response = requests.get(f"{UR}/livros/{livro_id}")
        if response.status_code != 200:
            print(f"Livro não encontrado: {response.text}")
            return
        
        livro = response.json()
        print("\nDados atuais do livro:")
        print(f"Título: {livro['titulo']}")
        print(f"Autor: {livro['autor']}")
        print(f"Ano: {livro['ano_publicacao']}")
        print(f"Editora: {livro['editora']}")
        print(f"Status: {livro['status']}")
        
        print("\nDigite os novos dados (deixe em branco para manter o valor atual):")
        titulo = input(f"Título [{livro['titulo']}]: ") or livro['titulo']
        autor = input(f"Autor [{livro['autor']}]: ") or livro['autor']
        ano_publicacao = input(f"Ano [{livro['ano_publicacao']}]: ") or livro['ano_publicacao']
        editora = input(f"Editora [{livro['editora']}]: ") or livro['editora']
        
        livro_atualizado = {
            "titulo": titulo,
            "autor": autor,
            "ano_publicacao": ano_publicacao,
            "editora": editora,
            "status": livro['status'],
            "uuid": livro_id
        }
        
        response = requests.put(f"{UR}/livros/{livro_id}", json=livro_atualizado)
        if response.status_code == 200:
            print("Livro atualizado com sucesso!")
            print(response.json())
        else:
            print(f"Erro ao atualizar livro: {response.text}")
    except Exception as e:
        print(f"Erro: {e}")

def localizar_livro():
    print("\n--- Localizar Livro ---")
    livro_id = input("Digite o ID do livro: ")
    try:
        response = requests.get(f"{UR}/livros/{livro_id}/localizacao")
        if response.status_code == 200:
            localizacao = response.json()
            print("\nLocalização do livro:")
            print(f"Status: {localizacao['status']}")
            
            if localizacao['status'] == "emprestado":
                print("\nDetalhes do empréstimo:")
                print(f"Usuário: {localizacao['usuario']['nome']}")
                if localizacao.get('armario'):
                    print(f"Armário: {localizacao['armario']['nome']}")
                print(f"Data prevista para devolução: {localizacao['data_devolucao']}")
        elif response.status_code == 404:
            print("Livro não encontrado.")
        else:
            print(f"Erro: {response.text}")
    except Exception as e:
        print(f"Erro: {e}")

def gerenciar_emprestimos():
    while True:
        print("\n--- Gerenciamento de Empréstimos ---")
        print("1. Registrar novo empréstimo")
        print("2. Listar todos os empréstimos")
        print("3. Buscar empréstimo por ID")
        print("4. Devolver livro")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            registrar_emprestimo()
        elif opcao == "2":
            listar_emprestimos()
        elif opcao == "3":
            buscar_emprestimo()
        elif opcao == "4":
            devolver_livro()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

def registrar_emprestimo():
    print("\n--- Registrar Novo Empréstimo ---")
    usuario_id = input("ID do usuário: ")
    livro_id = input("ID do livro: ")
    armario_id = input("ID do armário (opcional): ") or None
    data_devolucao = input("Data de devolução prevista (YYYY-MM-DD): ")
    
    try:
        emprestimo = {
            "usuario_uuid": usuario_id,
            "livro_uuid": livro_id,
            "armario_uuid": armario_id,
            "data_emprestimo": datetime.now().strftime("%Y-%m-%d"),
            "data_devolucao_prevista": data_devolucao,
            "status": "ativo"
        }
        response = requests.post(f"{UR}/emprestimos/", json=emprestimo)
        if response.status_code == 200:
            print("Empréstimo registrado com sucesso!")
            print(response.json())
        else:
            print(f"Erro ao registrar empréstimo: {response.text}")
    except Exception as e:
        print(f"Erro: {e}")

def listar_emprestimos():
    print("\n--- Lista de Empréstimos ---")
    try:
        response = requests.get(f"{UR}/emprestimos/")
        if response.status_code == 200:
            emprestimos = response.json()
            for emp in emprestimos:
                print(f"ID: {emp['uuid']}")
                print(f"Livro ID: {emp['livro_uuid']}")
                print(f"Usuário ID: {emp['usuario_uuid']}")
                print(f"Data empréstimo: {emp['data_emprestimo']}")
                print(f"Data devolução prevista: {emp['data_devolucao_prevista']}")
                print(f"Status: {emp['status']}")
                print("-" * 30)
        else:
            print(f"Erro ao listar empréstimos: {response.text}")
    except Exception as e:
        print(f"Erro: {e}")

def buscar_emprestimo():
    print("\n--- Buscar Empréstimo ---")
    emp_id = input("Digite o ID do empréstimo: ")
    try:
        response = requests.get(f"{UR}/emprestimos/{emp_id}")
        if response.status_code == 200:
            emprestimo = response.json()
            print("\nEmpréstimo encontrado:")
            print(f"ID: {emprestimo['uuid']}")
            print(f"Livro ID: {emprestimo['livro_uuid']}")
            print(f"Usuário ID: {emprestimo['usuario_uuid']}")
            print(f"Data empréstimo: {emprestimo['data_emprestimo']}")
            print(f"Data devolução prevista: {emprestimo['data_devolucao_prevista']}")
            print(f"Status: {emprestimo['status']}")
        elif response.status_code == 404:
            print("Empréstimo não encontrado.")
        else:
            print(f"Erro: {response.text}")
    except Exception as e:
        print(f"Erro: {e}")

def devolver_livro():
    print("\n--- Devolver Livro ---")
    emp_id = input("Digite o ID do empréstimo: ")
    try:
        response = requests.put(f"{UR}/emprestimos/{emp_id}/devolver")
        if response.status_code == 200:
            print(response.json()["message"])
        else:
            print(f"Erro ao devolver livro: {response.text}")
    except Exception as e:
        print(f"Erro: {e}")

def busca_avancada():
    print("\n--- Busca Avançada ---")
    titulo = input("Título do livro (opcional): ") or None
    autor = input("Autor do livro (opcional): ") or None
    status = input("Status do livro (disponivel, emprestado, reservado, indisponivel - opcional): ") or None
    tipo_usuario = input("Tipo de usuário (aluno, professor, funcionario - opcional): ") or None
    numero_sala = input("Número da sala (opcional): ") or None
    
    params = {}
    if titulo: params["titulo"] = titulo
    if autor: params["autor"] = autor
    if status: params["status_livro"] = status
    if tipo_usuario: params["tipo_usuario"] = tipo_usuario
    if numero_sala: params["numero_sala"] = numero_sala
    
    try:
        response = requests.get(f"{UR}/busca/", params=params)
        if response.status_code == 200:
            resultados = response.json()
            print("\n=== Resultados da Busca ===")
            
            if resultados["livros"]:
                print("\nLivros encontrados:")
                for livro in resultados["livros"]:
                    print(f"ID: {livro['uuid']}")
                    print(f"Título: {livro['titulo']}")
                    print(f"Autor: {livro['autor']}")
                    print(f"Status: {livro['status']}")
                    print("-" * 30)
            
            if resultados["usuarios"]:
                print("\nUsuários encontrados:")
                for usuario in resultados["usuarios"]:
                    print(f"ID: {usuario['uuid']}")
                    print(f"Nome: {usuario['nome']}")
                    print(f"Email: {usuario['email']}")
                    print(f"Tipo: {usuario['tipo']}")
                    print("-" * 30)
            
            if resultados["salas"]:
                print("\nSalas encontradas:")
                for sala in resultados["salas"]:
                    print(f"ID: {sala['uuid']}")
                    print(f"Número: {sala['numero']}")
                    print(f"Descrição: {sala['descricao']}")
                    print("-" * 30)
            
            if not resultados["livros"] and not resultados["usuarios"] and not resultados["salas"]:
                print("Nenhum resultado encontrado.")
        else:
            print(f"Erro na busca: {response.text}")
    except Exception as e:
        print(f"Erro: {e}")

def main():
    while True:
        opcao = mostrar_menu_principal()
        
        if opcao == "1":
            gerenciar_usuarios()
        elif opcao == "2":
            gerenciar_livros()
        elif opcao == "3":
            print("Funcionalidade de armários ainda não implementada")
        elif opcao == "4":
            print("Funcionalidade de salas ainda não implementada")
        elif opcao == "5":
            gerenciar_emprestimos()
        elif opcao == "6":
            busca_avancada()
        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")
if __name__ == "__main__":
    main()