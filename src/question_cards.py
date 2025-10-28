import flet as ft

def StepCard(step_number: int, title: str, instruction: str, detail: str, question: str, on_yes=None, on_no=None):
    """Componente mejorada con alto contraste visual"""

    return ft.Card(
        elevation=4,
        content=ft.Container(
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.BLACK),
            content=ft.Column(
                spacing=15,
                controls=[
                    # Encabezado
                    ft.Row(
                        [
                            ft.Container(
                                width=32,
                                height=32,
                                bgcolor="#0A2240",  # Azul oscuro más intenso
                                border_radius=20,
                                alignment=ft.alignment.center,
                                content=ft.Text(
                                    str(step_number),
                                    color=ft.Colors.WHITE,
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ),
                            ft.Text(
                                title,
                                size=19,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK,
                            ),
                        ]
                    ),
                    # Instruction
                    ft.Text(
                        "Instrucción:",
                        weight=ft.FontWeight.BOLD,
                        size=14,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(instruction, size=13, color=ft.Colors.BLACK),
                    # Caja de detalle
                    ft.Container(
                        border=ft.border.all(1, ft.Colors.BLACK),
                        border_radius=8,
                        padding=10,
                        bgcolor="#F8FAFC",  # Fondo ligeramente gris-azulado
                        content=ft.Row(
                            spacing=10,
                            controls=[
                                ft.Icon(ft.Icons.INFO, color="#0A2240", size=20),
                                ft.Text(detail, size=13, color=ft.Colors.BLACK),
                            ],
                        ),
                    ),
                    ft.Divider(height=20, color="#000000"),
                    # Pregunta
                    ft.Text(
                        question,
                        weight=ft.FontWeight.BOLD,
                        size=15,
                        color=ft.Colors.BLACK,
                    ),
                    # Botones Yes / No
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        spacing=10,
                        controls=[
                            ft.ElevatedButton(
                                text="Si",
                                icon=ft.Icons.CHECK_CIRCLE,
                                bgcolor="#0A2240",
                                color=ft.Colors.WHITE,
                                height=45,
                                expand=True,
                                on_click=lambda e: on_yes() if on_yes else None,
                            ),
                            ft.ElevatedButton(
                                text="No",
                                icon=ft.Icons.CANCEL,
                                bgcolor="#B91C1C",  # Rojo intenso
                                color=ft.Colors.WHITE,
                                height=45,
                                expand=True,
                                on_click=lambda e: on_no() if on_no else None,
                            ),
                        ],
                    ),
                ],
            ),
        ),
    )
