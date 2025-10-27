import flet as ft

def StepCard(step_number: int, title: str, instruction: str, detail: str, question: str, on_yes=None, on_no=None):
    """Componente simple reutilizable estilo 'Paper Path Inspection'"""

    return ft.Card(
        content=ft.Container(
            padding=20,
            bgcolor="white",
            border_radius=10,
            content=ft.Column(
                spacing=15,
                controls=[
                    # Encabezado
                    ft.Row(
                        [
                            ft.Container(
                                width=28,
                                height=28,
                                bgcolor="#0B3558",
                                border_radius=20,
                                alignment=ft.alignment.center,
                                content=ft.Text(str(step_number), color="white", size=14, weight=ft.FontWeight.BOLD),
                            ),
                            ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
                        ]
                    ),
                    # Instruction
                    ft.Text("Instruction:", weight=ft.FontWeight.BOLD, size=13),
                    ft.Text(instruction, size=13),
                    # Caja de detalle
                    ft.Container(
                        border=ft.border.all(1, "#D0D7DE"),
                        border_radius=8,
                        padding=10,
                        content=ft.Row(
                            spacing=10,
                            controls=[
                                ft.Icon(ft.Icons.INFO_OUTLINE, color="#6B7280"),
                                ft.Text(detail, size=12, color="#475569"),
                            ],
                        ),
                    ),
                    ft.Divider(height=20, color="#E5E7EB"),
                    # Pregunta
                    ft.Text(question, weight=ft.FontWeight.BOLD, size=14),
                    # Botones Yes / No
                    ft.Row(
                        adaptive=True,
                        expand=True,
                        spacing=10,
                        controls=[
                            ft.Button(
                                elevation=2,
                                expand=True,
                                on_click=lambda e: on_yes() if on_yes else None,
                                bgcolor="#0B3558",
                                content=ft.Text("Yes", color="white", weight=ft.FontWeight.BOLD),
                            ),
                            ft.Button(
                                elevation=2,
                                expand=True,
                                on_click=lambda e: on_no() if on_no else None,
                                content=ft.Text("No", color="#475569", weight=ft.FontWeight.BOLD),
                            ),
                        ],
                    ),
                ],
            ),
        ),
    )