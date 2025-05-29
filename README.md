# SmartLibrary
Biblioteca Inteligente -  Projeto da matéria de POS
# Documentação do Projeto: Sistema de Biblioteca

---

## 1. Visão Geral

### Tecnologias Utilizadas
- **Python** (Linguagem principal)
- **FastAPI** (Framework para a API)
- **Uvicorn** (Servidor ASGI)
- **SQLite** (Banco de dados padrão)  

### Descrição
Sistema completo para gerenciamento de:  
- Salas da biblioteca  
- Armários e acervo físico  
- Livros e Emprestimos 

### Objetivo
Automatizar o controle de espaços físicos e recursos literários da biblioteca.  


---

## 2. Descrição Detalhada

### 2.1 Funcionalidades Principais

| Funcionalidade          | Descrição                                  |
|-------------------------|--------------------------------------------|
| **Cadastro de Salas**   | Registrar/editar salas (número, capacidade)|
| **Registrar Emprestimo**| Registrar emprestimo de Salas e Livros    |
| **Gerenciar Armários**  | Associar armários a salas (localização)   |
| **Controle de Livros**  | Título, autor, status                    |
| **Relacionamentos**     | Visualizar livros → armários → salas      |
| **Busca Avançada**      | Filtros por múltiplos critérios           |

### 2.2 Arquitetura do Projeto

```
biblioteca/
├── 📁 core/
│   ├── models.py       # Modelos de banco de dados
│   ├── schemas.py      # Schemas Pydantic
│   └── crud.py        # Operações de banco
├── 📁 api/
│   ├── endpoints/      # Rotas da API
│   └── dependencies.py # Injeções
├── main.py             # App FastAPI
└── requirements.txt    # Tem que definir tudo ainda (aqui é so modelo)
 ```
---

## 3. Cronograma

### Etapa 1: Modelagem (20/05)
- Definir Projeto   
- Definir Funcionalidades 
- Entrega da Documentação  

### Etapa 2: API Básica (Colocar)
- Iniciar desenvolvimento 
- Definir os principais Endepoints 
- Iniciar Implementação com o banco 


### Etapa 3: Sistema Teste (Colocar)
- 
- 

### Etapa 4: Implantação (Colocar)
-
-  

---

## 4. Como Contribuir

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/biblioteca-api.git
```

2. Configure o ambiente:
```bash
  python -m venv .venv && source .venv/bin/activate
  pip install -r requirements.txt
```
3. Execute:
 ```bash
  uvicorn main:app --reload
```

> Acesse a API em: `http://localhost:8000/docs`  

---

**Próximos Passos**:  
    - [ ] Adicionar autenticação JWT  
    - [ ] Implementar frontend React  
```