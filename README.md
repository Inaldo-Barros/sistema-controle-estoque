# Sistema de Controle de Estoque e Vendas 📦🛒

Um sistema moderno, leve e intuitivo para gerenciamento de estoque e registro de vendas, desenvolvido em **Python** utilizando a biblioteca **CustomTkinter** para a interface gráfica (com suporte a temas claro e escuro do sistema) e **SQLite** como banco de dados local.

## 🚀 Funcionalidades

O sistema foi estruturado de forma modular e conta com as seguintes ferramentas:

* **📊 Dashboard Informativo:** Apresenta métricas em tempo real, incluindo o total de produtos cadastrados, quantidade total de itens no estoque geral, alertas de produtos com estoque baixo e um painel com os detalhes da última movimentação realizada.
* **➕ Cadastro de Produtos:** Permite registrar novos itens informando o Nome, Quantidade Inicial, Limite de Estoque Mínimo (para alertas) e Preço de Venda.
* **🔍 Pesquisa Inteligente:** Busca rápida de produtos por nome com listagem dinâmica, permitindo a visualização rápida de informações e a exclusão direta de itens do banco de dados.
* **📥 Entrada de Estoque:** Atualização rápida do saldo de um produto existente através do preenchimento do ID do produto e da quantidade a ser adicionada.
* **📋 Relatório Geral de Estoque:** Exibição de todos os produtos cadastrados de forma organizada em uma lista rolável, destacando automaticamente em **vermelho** os itens que atingiram ou estão abaixo do estoque mínimo definido.
* **💰 Registro de Vendas (Saída):** Processamento de saídas de mercadorias com validação automática de estoque (impede a venda caso a quantidade solicitada seja maior do que a disponível).
* **📜 Histórico de Movimentações:** Relatório completo e cronológico de todas as entradas (destacadas em verde) e saídas/vendas (destacadas em laranja) efetuadas no sistema.

## 🛠️ Tecnologias Utilizadas

* **Language:** [Python 3.x](https://www.python.org/)
* **GUI Library:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (Interface moderna e responsiva)
* **Database:** SQLite (Banco de dados local integrado, dispensando configurações complexas de servidores)

## 📁 Estrutura do Projeto

O projeto adota uma arquitetura limpa separando a lógica de negócios da interface gráfica:

* `app.py`: Contém a construção de toda a interface visual, navegação entre telas, gerenciamento de frames dinâmicos e validação das entradas do usuário.
* `banco.py`: Camada de persistência responsável pela conexão com o banco `estoque.db`, criação automatizada das tabelas e funções especializadas para consultas e manipulação de dados (CRUD).
* `.gitignore`: Arquivo de configuração para evitar o envio de arquivos temporários do Python (`__pycache__`) e da base de dados local de testes (`estoque.db`) para o repositório.

## 🔧 Como Executar o Projeto

### Pré-requisitos
Certifique-se de ter o Python instalado em sua máquina. Você também precisará instalar a biblioteca `customtkinter`.

