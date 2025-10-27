import flet as ft
from question_cards import StepCard
from views.FletRouter import Router

def main(page: ft.Page):
    Router(page)
    def yes_action():
        page.go("/diagnostic")

    def no_action():
        page.snack_bar = ft.SnackBar(ft.Text("You clicked No!"))
        page.snack_bar.open = True
        page.update()

    card = StepCard(
        step_number=2,
        title="Paper Path Inspection",
        instruction="Visually inspect the paper path for scraps, clips, or foreign objects.",
        detail="Check between Tray 2 Take Away and Tray 3 Take Away Sensors. Remove any debris found.",
        question="Is the paper path clear?",
        on_yes=yes_action,
        on_no=no_action,
    )

    page.add(ft.Container(padding=20, content=card))

ft.app(main, view=ft.AppView.WEB_BROWSER)
