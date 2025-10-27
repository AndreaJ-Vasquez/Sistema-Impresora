import flet as ft
from views.diagnostic_view import DiagnosticView

class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop
        self.page.go(self.page.route)

    def route_change(self, e: ft.RouteChangeEvent):
        p = self.page
        p.views.clear()

        # Pantalla principal
        if p.route == "/":
            p.views.append(
                ft.View(
                    route="/",
                    controls=[
                        ft.AppBar(title=ft.Text("Asistente de Diagnóstico"), bgcolor="#0B3558", color="white"),
                        ft.Container(
                            alignment=ft.alignment.center,
                            padding=40,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=25,
                                controls=[
                                    ft.Text(
                                        "Bienvenido al Sistema Experto de Diagnóstico",
                                        size=22,
                                        weight=ft.FontWeight.BOLD,
                                        color="#0B3558",
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    ft.Text(
                                        "Este asistente te guiará paso a paso para resolver errores comunes en la impresora.",
                                        size=14,
                                        color="#55708F",
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    ft.ElevatedButton(
                                        "Iniciar diagnóstico",
                                        icon=ft.Icons.PLAY_ARROW,
                                        bgcolor="#0B3558",
                                        color="white",
                                        on_click=lambda _: p.go("/diagnostic"),
                                    ),
                           
                                ],
                            ),
                        ),
                    ],
                )
            )

        # Pantalla de diagnóstico
        elif p.route == "/diagnostic":
            p.views.append(DiagnosticView(p))

        p.update()

    def view_pop(self, e):
        self.page.views.pop()
        self.page.go(self.page.views[-1].route)
