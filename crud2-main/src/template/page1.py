import flet as ft
from src.service import crud  # Importando o módulo de CRUD para acessar o banco de dados
from src.model.db import SessionLocal  # Importando a sessão para conexão com o banco

class Page1:
    def __init__(self, page: ft.Page):
        self.page = page

    def construir(self):
        # Obtém todas as tarefas do banco de dados
        tarefas = crud.listar_tarefa(SessionLocal())
        # Lista de colunas do DataTable
        columns = [ 
            ft.DataColumn(ft.Text("Descrição")),
            ft.DataColumn(ft.Text("Status")),
            ft.DataColumn(ft.Text("Ações")),
        ]
        
        # Lista de linhas para o DataTable
        rows = []
        for tarefa in tarefas:
            # Para cada tarefa, criamos uma linha no DataTable
            rows.append(
                ft. DataRow(
                    cells=[
                        ft.DataCell(ft.Text(tarefa.DESCRICAO)),
                        ft.DataCell(ft.Text("Concluída" if tarefa.SITUACAO else "Pendente")),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.icons.EDIT,
                                        tooltip="Editar tarefa",
                                        on_click=lambda e, task=tarefa: self.editar_tarefa(task)  # Passando a tarefa específica para edição
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.DELETE_OUTLINED,
                                        tooltip="Deletar tarefa",
                                        on_click=lambda e, task=tarefa: self.remover_tarefa(task)  # Passando a tarefa específica para remoção
                                    ),
                                ],
                            ), 
                        ), 
                    ] , 
                ) , 
            ) ,
        
        # Cria a tabela de tarefas
        data_table = ft.DataTable(
            column_spacing=200,
            columns=columns,
            rows=rows,
             
        )
        
        # Retorna o layout com o DataTable e o botão de voltar
        return ft.ResponsiveRow(
            [
                ft.Column(
                    [
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK_IOS,
                            tooltip="Voltar",
                            on_click=lambda _: self.page.go("/interface"),
                        ),
                        data_table,
                    ]
                )
            ]
        )
    
    def remover_tarefa(self, tarefa):
        def confirmar_exclusao(e):
            # Remove a tarefa do banco de dados
            crud.excluir_tarefa(SessionLocal(), tarefa.ID)  # Função que exclui a tarefa do banco de dados

            # Atualiza a listagem na interface, removendo a tarefa da página
            self.page.controls.clear()  # Limpa todos os controles da página (incluindo a listagem atual)
            self.page.add(self.construir())  # Recarrega a lista de tarefas após a exclusão
            self.page.close(dlg_modal)
            self.page.update()  # Atualiza a página

        def cancelar_exclusao(e):
            self.page.close(dlg_modal)  # Fecha o diálogo de confirmação
            self.page.update()  # Atualiza a página para refletir o fechamento do diálogo

        # Criando o diálogo de confirmação
        dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Por favor, confirme"),
        content=ft.Text("Você tem certeza que deseja excluir esta tarefa?"),
        actions=[
            ft.TextButton("Sim", on_click=confirmar_exclusao),  # Botão para confirmar
            ft.TextButton("Não", on_click=cancelar_exclusao),  # Botão para cancelar
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

        # Adicionando o diálogo à página
        self.page.open(dlg_modal)
        dlg_modal.visible = True  # Torna o diálogo visível
        self.page.update()  # Atualiza a página para refletir a exibição do diálogo



    def editar_tarefa(self, tarefa):
        # Função que será chamada ao clicar no botão de editar

        # Função para salvar a tarefa editada
        def salvar_edicao(e):
            # Atualiza os dados da tarefa com os novos valores
            descricao = descricao_text.value
            situacao = situacao_switch.value  # Valor do switch (Pendente ou Concluída)

            # Agora passamos os argumentos corretos para a função editar_tarefa
            updated_tarefa = crud.editar_tarefa(SessionLocal(), tarefa.ID, descricao, situacao)

            if updated_tarefa:
                # Fechar a caixa de diálogo
                self.page.close(dlg_modal)

                # Atualiza a interface para refletir as alterações
                self.page.controls.clear()  # Limpa os controles da página
                self.page.add(self.construir())  # Recarrega a lista de tarefas com a tarefa atualizada
                self.page.update()
            else:
                print("Erro ao editar a tarefa")

        # Função para cancelar a edição
        def cancelar_edicao(e):
            # Fecha a caixa de diálogo sem fazer alterações
            self.page.close(dlg_modal)
            self.page.update()

        # Cria os controles do formulário de edição
        descricao_text = ft.TextField(value=tarefa.DESCRICAO, label="Descrição", autofocus=True)
        situacao_switch = ft.Switch(label="Concluída", value=tarefa.SITUACAO)

        # Criando o diálogo de edição
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Tarefa"),
            content=ft.Column([
                descricao_text,
                situacao_switch,
            ]),
            actions=[
                ft.TextButton("Salvar", on_click=salvar_edicao),  # Botão para salvar as alterações
                ft.TextButton("Cancelar", on_click=cancelar_edicao),  # Botão para cancelar
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Adicionando o diálogo à página
        self.page.open(dlg_modal)
        dlg_modal.visible = True  # Torna o diálogo visível
        self.page.update()  # Atualiza a página para refletir a exibição do diálogo
