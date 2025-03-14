import flet as ft
from src.service import crud  # Importando o módulo de CRUD para acessar o banco de dados
from src.model.db import SessionLocal  # Importando a sessão para conexão com o banco

class Page1:
    def __init__(self, page: ft.Page):
        self.page = page
        page.theme_mode = ft.ThemeMode.DARK

    def construir(self):
        # Obtém todas as tarefas do banco de dados
        tarefas = crud.listar_tarefa(SessionLocal())
        
        # Cria uma lista de controles (tarefa) para mostrar na interface
        tarefa_rows = []
        for tarefa in tarefas:
            # Criando uma linha para cada tarefa
            tarefa_row = ft.Row(
                [
                    ft.Text(str(tarefa.ID), width=100),  # Mostrando o ID da tarefa
                    ft.Text(tarefa.DESCRICAO, width=300),  # Mostrando a descrição
                    ft.Text("Concluída" if tarefa.SITUACAO else "Pendente", width=150),  # Mostrando o status da tarefa
                    # Botão de editar
                    ft.IconButton(
                        icon=ft.icons.EDIT,
                        tooltip="Editar tarefa",
                        on_click=lambda e, task=tarefa: self.editar_tarefa(task)  # Passando a tarefa específica para edição
                    ),
                    # Botão de deletar
                    ft.IconButton(
                        icon=ft.icons.DELETE_OUTLINED,
                        tooltip="Deletar tarefa",
                        on_click=lambda e, task=tarefa: self.remover_tarefa(task)  # Passando a tarefa específica para remoção
                    ),
                ],
                spacing=10  # Adicionando um pequeno espaço entre os controles
            )
            tarefa_rows.append(tarefa_row)
        
        # Criando a estrutura de layout com as tarefas
        return ft.Column([
            ft.ElevatedButton('Voltar', on_click=lambda _: self.page.go('/interface')),
            ft.Column(tarefa_rows)  # Adicionando todas as linhas de tarefas na tela
        ])

    def editar_tarefa(self, tarefa):
        """Função para editar a tarefa"""
        def salvar_edicao(e):
            # Exemplo de como você pode editar a tarefa
            nova_descricao = campo_edicao.value  # Obtendo o novo valor da descrição
            nova_situacao = checkbox.value  # Obtendo o valor da situação (checkbox)
            updated_task = crud.editar_tarefa(SessionLocal(), tarefa.ID, nova_descricao, nova_situacao)

            if updated_task:
                # Atualizando a linha da tarefa na interface
                for row in self.page.controls:
                    for control in row.controls:
                        if isinstance(control, ft.Row) and control.controls[0].text == str(tarefa.ID):
                            control.controls[1].text = nova_descricao  # Atualizando a descrição
                            control.controls[2].text = "Concluída" if nova_situacao else "Pendente"  # Atualizando o status
                            self.page.update()
                self.page.update()  # Atualizando a página

        # Criando a interface de edição
        campo_edicao = ft.TextField(value=tarefa.DESCRICAO, label="Editar Descrição")
        checkbox = ft.Checkbox(value=tarefa.SITUACAO, label="Concluída")

        # Criando o botão de salvar
        btn_salvar = ft.ElevatedButton(
            text="Salvar",
            on_click=salvar_edicao
        )

        # Exibindo a interface de edição
        self.page.add(ft.Column([campo_edicao, checkbox, btn_salvar]))
        self.page.update()

    def remover_tarefa(self, tarefa):
        """Função para remover a tarefa"""
        def confirmar_exclusao(e):
            # Removendo a tarefa do banco de dados
            crud.excluir_tarefa(SessionLocal(), tarefa.ID)
            # Removendo a tarefa da interface
            for row in self.page.controls:
                for control in row.controls:
                    if isinstance(control, ft.Row) and control.controls[0].text == str(tarefa.ID):
                        row.controls.remove(control)
                        self.page.update()  # Atualizando a página
                        break
            self.page.update()  # Atualizando a página após a remoção

        def cancelar_exclusao(e):
            self.page.update()  # Atualizando a página

        # Criando o diálogo de confirmação
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text(f"Tem certeza que deseja excluir a tarefa: {tarefa.DESCRICAO}?"),
            actions=[
                ft.TextButton("Sim", on_click=confirmar_exclusao),
                ft.TextButton("Não", on_click=cancelar_exclusao),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.open(dlg_modal)
        dlg_modal.visible = True  # Exibindo o diálogo
        self.page.update()  # Atualizando a página
