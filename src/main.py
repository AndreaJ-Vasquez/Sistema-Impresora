import flet as ft
from views.FletRouter import Router

def main(page: ft.Page):
    Router(page)

ft.app(main, view=ft.AppView.WEB_BROWSER)
