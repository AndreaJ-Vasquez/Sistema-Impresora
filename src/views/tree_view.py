import flet as ft
import json
from pathlib import Path


def render_step(step, depth=0):
    """Render a diagnostic step with visual indentation."""
    yes_data = step.get("yes", "N/A")
    no_data = step.get("no", "N/A")

    sub_items = []

    # Instruction
    if "instruction" in step and step["instruction"]:
        sub_items.append(ft.Text(f"🧩 {step['instruction']}", size=13, color=ft.Colors.BLACK))

    # Question
    if "question" in step and step["question"]:
        sub_items.append(
            ft.Text(f"❓ {step['question']}", size=13, italic=True, color=ft.Colors.BLACK)
        )

    # YES / NO response blocks
    yes_tile = ft.ListTile(
        leading=ft.Icon(ft.Icons.CHECK_CIRCLE, color="#065F46"),
        title=ft.Text("Yes", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
        subtitle=ft.Text(
            yes_data.get("action", "") if isinstance(yes_data, dict) else str(yes_data),
            size=12,
            color=ft.Colors.BLACK,
        ),
        dense=True,
    )

    no_tile = ft.ListTile(
        leading=ft.Icon(ft.Icons.CANCEL, color="#B91C1C"),
        title=ft.Text("No", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
        subtitle=ft.Text(
            no_data.get("action", "") if isinstance(no_data, dict) else str(no_data),
            size=12,
            color=ft.Colors.BLACK,
        ),
        dense=True,
    )

    sub_items.extend([yes_tile, no_tile])

    tile = ft.ExpansionTile(
        title=ft.Text(
            f"{step['id']}. {step['title']}",
            size=14,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK,
        ),
        controls=sub_items,
        icon_color="#0B3558",
        collapsed_icon_color="#0B3558",
    )

    return ft.Container(
        content=tile,
        margin=ft.margin.only(left=depth * 20, top=4, bottom=4),
        padding=10,
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.border_radius.all(6),
        border=ft.border.all(1, ft.Colors.BLACK),
    )


def tree_view_component():
    """Build the diagnostic flow tree view."""
    base_path = Path(__file__).resolve().parent.parent
    json_path = base_path / "error-data.json"

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    error_data = data["C4-2"]
    steps = error_data["steps"]

    rendered_steps = [render_step(step, depth=step["id"] - 1) for step in steps]

    # ✅ Usamos ListView para habilitar scroll automático vertical
    scrollable_content = ft.ListView(
        controls=rendered_steps,
        spacing=8,
        expand=True,
        auto_scroll=False,  # no baja automáticamente
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text(
                        "Paper Jam Areas A,B - Diagnostic Flow",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                    ),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=8,
                    border=ft.border.all(1, ft.Colors.BLACK),
                    padding=10,
                    margin=ft.margin.only(bottom=10),
                ),
                # Scroll real aquí 👇
                ft.Container(
                    expand=True,
                    content=scrollable_content,
                ),
            ],
            expand=True,
        ),
        expand=True,
        padding=10,
        border=ft.border.all(1, ft.Colors.BLACK),
        border_radius=8,
        bgcolor=ft.Colors.WHITE,
    )
