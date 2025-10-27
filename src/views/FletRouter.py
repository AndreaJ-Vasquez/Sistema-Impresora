import flet as ft
from views.diagnostic_view import DiagnosticView
from question_cards import StepCard 

class Router:
    def __init__(self, page: ft.Page, ft_module=ft):
        self.page = page
        self.ft = ft_module

        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop
        self.body = ft.Container(expand=True)

        self.page.go(self.page.route)

    def route_change(self, e: ft.RouteChangeEvent):
        p = self.page
        p.views.clear()

        # Página principal (/)
        p.views.append(
            ft.View(
                route="/",
                controls=[
                    ft.AppBar(title=ft.Text("Home"), bgcolor="#0B3558", color="white"),
                    ft.Container(
                        alignment=ft.alignment.center,
                        content=ft.ElevatedButton("Ir a diagnóstico", on_click=lambda _: p.go("/diagnostic")),
                    ),
                    StepCard(
                    step_number=2,
                    title="Paper Path Inspection",
                    instruction="Visually inspect the paper path for scraps, clips, or foreign objects.",
                    detail="Check between Tray 2 Take Away and Tray 3 Take Away Sensors. Remove any debris found.",
                    question="Is the paper path clear?",
                    on_yes=lambda: p.go("/diagnostic"),
                )
                ],
            )
        )

        # Página /diagnostic
        if p.route == "/diagnostic":
            p.views.append(DiagnosticView(p))

        p.update()

    def view_pop(self, e):
        self.page.views.pop()
        self.page.go(self.page.views[-1].route)
