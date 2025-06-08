# Documentação do Projeto: Sistema de Biblioteca SmartLibrary

## Componentes:
- Ariane Valéria 
- Karyne Ohara 
- Riversson Paulo


## 1. Visão Geral

### Tecnologias Utilizadas
- **Python** (Linguagem principal)
- **FastAPI** (Framework para a API)
- **Uvicorn** (Servidor ASGI)
- **SQLite** (Banco de dados padrão)
- **API SUAP** (Para integração com o sistema acadêmico)  

### Descrição
Sistema completo para gerenciamento da Biblioteca, com as seguintes funcionalidades:  
- Controle de salas e espaços físicos  
- Gerenciamento de armários
- Empréstimos de livros.
- Integração com o sistema acadêmico (SUAP)

### Objetivo
Automatizar e simplificar os processos da biblioteca, tornando o acesso aos recursos mais eficiente para alunos e funcionários. 


---

## 2. Descrição Detalhada

### 2.1 Funcionalidades Principais

| Funcionalidade          | Descrição                                  |
|-------------------------|--------------------------------------------|
| **Cadastro de Salas**   | Registrar/editar salas (número, capacidade)|
| **Registrar Emprestimo**| Registrar emprestimo de Salas e Livros     |
| **Gerenciar Armários**  | Associar armários a salas (localização)    |
| **Controle de Livros**  | Título, autor, status                      |
| **Relacionamentos**     | Visualizar livros → armários → salas       |
| **Busca Avançada**      | Filtros por múltiplos critérios            |
| **Integração SUAP**     | Autenticação e dados acadêmicos            |

### 2.2 Arquitetura do Projeto

```
SmartLibrary/
├── README.md           # Documentação principal
├── models.py           # Classes e modelos de dados
├── main.py             # Aplicação FastAPI (implementado)
├── suap_integration.py # Integração com SUAP (pendente)
├── database.py         # Conexão com banco SQL (pendente)
├── templates/          # Frontend (pendente)
└── requirements.txt    # Dependências do projeto
 ```
---

## 3. Cronograma

### Etapa 1: Modelagem (20/05)
- Definir escopo do projeto 
- Modelar estrutura principal (livros, salas, armários) 
- Criar documentação inicial

### Etapa 2: API Básica (27/05)
- Desenvolver endpoints principais
- Implementar sistema de empréstimos 
- Criar busca avançada
- Testes iniciais de integração

### Etapa 3: Integrações (15/07)
- Conectar com banco de dados SQLite 
- Implementar API do SUAP para:
   - Autenticação de usuários
   - Verificação de matrículas
   - Vinculação com dados acadêmicos
- Testes de integração

### Etapa 4:  Interface e Finalização (22/07)
- Desenvolver interface web simples
- Conectar frontend com a API
- Testes finais e ajustes


---

## 4. Como Contribuir

1. Clone o repositório:
```bash
git clone https://github.com/arianevaleira/SmartLibrary.git
```

2. Configure o ambiente:
```bash
  pip install -r requirements.txt
```
3. Execute:
 ```bash
  uvicorn main:app 
```

> Acesse a API em: `http://localhost:8000/docs`  

---

**Próximos Passos**: 
``` 
    - [ ] Integrar o sistema no servidor 
    - [ ] Deixar o sistema pronto para uso cotidiano
```
