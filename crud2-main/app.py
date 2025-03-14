from sqlalchemy.orm import Session
from src.model.db import SessionLocal  # Importando a sessão para interagir com o banco de dados
from src.service import crud  # Importando as funções CRUD
import flet as ft  # Importando Flet para a interface gráfica

# Função para criar uma tarefa
def cadastrar_tarefa():
    db = SessionLocal()  # Cria uma sessão com o banco
    try:
        descricao = "Tarefa de exemplo"
        situacao = False  # Situação inicial da tarefa
        new_task = crud.cadastrar_tarefa(db, descricao, situacao)
        print(f"Tarefa criada: ID={new_task.ID}, Descrição={new_task.DESCRICAO}, Situação={new_task.SITUACAO}")
    finally:
        db.close()  # Fecha a sessão

# Função para listar todas as tarefas
def listar_tarefas():
    db = SessionLocal()  # Cria uma sessão com o banco
    try:
        tasks = crud.listar_tarefa(db)
        return tasks
    finally:
        db.close()  # Fecha a sessão

# Função para editar uma tarefa
def editar_tarefa(task_id, descricao, situacao):
    db = SessionLocal()  # Cria uma sessão com o banco
    try:
        updated_task = crud.editar_tarefa(db, task_id, descricao, situacao)
        return updated_task
    finally:
        db.close()  # Fecha a sessão

# Função para excluir uma tarefa
def excluir_tarefa(task_id):
    db = SessionLocal()  # Cria uma sessão com o banco
    try:
        success = crud.excluir_tarefa(db, task_id)
        return success
    finally:
        db.close()  # Fecha a sessão

# Função para buscar tarefa por ID
def listar_tarefa_por_id(task_id):
    db = SessionLocal()  # Cria uma sessão com o banco
    try:
        task = crud.listar_tarefa_id(db, task_id)
        return task
    finally:
        db.close()  # Fecha a sessão

# Função principal para a interface com Flet
def main(page: ft.Page):
    page.title = 'App de Lista de Tarefas'  # Definindo o título da página
    page.window.height = 700
    page.window.width = 700
    page.window.center()

    # Lista global para armazenar os itens de tarefa na interface
    lista_tarefas = []

    def atualizar_tarefas():
        """Atualiza a lista de tarefas na interface gráfica"""
        for task in listar_tarefas():
            nova_tarefa = ft.Row([])

            checkbox = ft.Checkbox(label=task.DESCRICAO, value=task.SITUACAO)
            btn_editar = ft.IconButton(
                icon=ft.icons.EDIT,
                on_click=lambda e, task_id=task.ID: editar_tarefa_interface(task_id)
            )
            btn_remover = ft.IconButton(
                icon=ft.icons.DELETE_OUTLINED,
                on_click=lambda e, task_id=task.ID: remover_tarefa_interface(task_id)
            )

            nova_tarefa.controls.extend([checkbox, btn_editar, btn_remover])
            page.add(nova_tarefa)
            lista_tarefas.append(nova_tarefa)

        page.update()

    def editar_tarefa_interface(task_id):
        task = listar_tarefa_por_id(task_id)
        if task:
            descricao = "Nova descrição"  # Você pode adicionar uma interface para editar a descrição
            situacao = not task.SITUACAO
            editar_tarefa(task_id, descricao, situacao)
            page.add(ft.Text(f"Tarefa {task_id} atualizada!"))
            atualizar_tarefas()

    def remover_tarefa_interface(task_id):
        if excluir_tarefa(task_id):
            page.add(ft.Text(f"Tarefa {task_id} excluída!"))
            atualizar_tarefas()

    def adicionar_tarefa(e):
        descricao = nova_tarefa.value
        if descricao:
            cadastrar_tarefa()
            atualizar_tarefas()

    # Definir o campo de texto para inserir nova tarefa
    nova_tarefa = ft.TextField(label="Nova Tarefa", width=300)
    botao_adicionar = ft.ElevatedButton("Adicionar", on_click=adicionar_tarefa)

    # Adicionando os controles principais à página
    page.add(nova_tarefa, botao_adicionar)
    atualizar_tarefas()  # Atualiza as tarefas ao carregar

# Rodando o aplicativo Flet
ft.app(target=main)
