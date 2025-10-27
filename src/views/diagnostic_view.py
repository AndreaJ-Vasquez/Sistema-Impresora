import flet as ft
from question_cards import StepCard
import json
import os

def DiagnosticView(page: ft.Page):
    base_path = os.path.dirname(__file__)
    json_path = os.path.join(base_path, "..", "error-data.json")
    json_path = os.path.abspath(json_path)
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    case = data["C4-2"]
    
    page.title = case["name"]
    page.bgcolor = "#F5FAFF"
    
    card_holder = ft.Container(padding=20)
    show_menu = {"value": True} 
    
    def get_step(step_id):
        for s in case.get("steps", []):
            if s["id"] == step_id:
                return s
        return None
    
    def show_action_result(action_data):
        # Muestra el resultado de una acción requerida
        action_text = action_data.get("action", "Action completed")
        note_text = action_data.get("note", "")
        next_step_id = action_data.get("next_step", 0)
        
        result_content = ft.Column(
            spacing=15,
            controls=[
                ft.Container(
                    bgcolor="#FFF4E6",
                    border_radius=10,
                    padding=15,
                    border=ft.border.all(2, "#F59E0B"),
                    content=ft.Column(
                        spacing=10,
                        controls=[
                            ft.Row(
                                spacing=10,
                                controls=[
                                    ft.Icon(ft.Icons.BUILD_CIRCLE, color="#F59E0B", size=28),
                                    ft.Text("Action Required", size=16, weight=ft.FontWeight.BOLD, color="#92400E")
                                ]
                            ),
                            ft.Divider(height=1, color="#FCD34D"),
                            ft.Text(action_text, size=14, color="#78350F", weight=ft.FontWeight.W_500),
                        ] + ([ft.Container(
                            bgcolor="#FEF3C7",
                            border_radius=8,
                            padding=10,
                            content=ft.Row(
                                spacing=8,
                                controls=[
                                    ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, color="#D97706", size=18),
                                    ft.Text(note_text, size=12, color="#92400E", italic=True, expand=True)
                                ]
                            )
                        )] if note_text else [])
                    )
                ),
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.ElevatedButton(
                            "Continue",
                            icon=ft.Icons.ARROW_FORWARD,
                            bgcolor="#0B3558",
                            color="white",
                            height=45,
                            expand=True,
                            on_click=lambda e: show_step(next_step_id)
                        ),
                        ft.OutlinedButton(
                            "Back to Menu",
                            icon=ft.Icons.HOME,
                            height=45,
                            on_click=lambda e: show_steps_menu()
                        )
                    ]
                )
            ]
        )
        
        card_holder.content = ft.Container(padding=20, content=result_content)
        page.update()
    
    def show_completion_message():
        #Muestra el mensaje final cuando el diagnóstico está completo
        card_holder.content = ft.Container(
            alignment=ft.alignment.center,
            padding=30,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color="#10B981", size=64),
                    ft.Text(
                        case.get("success_message", "✅ Diagnostic complete."),
                        size=18,
                        color="#0B3558",
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Divider(height=20, color="transparent"),
                    ft.Container(
                        bgcolor="#F0FDF4",
                        border_radius=10,
                        padding=20,
                        border=ft.border.all(2, "#10B981"),
                        content=ft.Column(
                            spacing=15,
                            controls=[
                                ft.Text("Final Checklist:", size=16, weight=ft.FontWeight.BOLD, color="#0B3558"),
                                *[
                                    ft.Row(
                                        spacing=10,
                                        controls=[
                                            ft.Icon(ft.Icons.CHECK_BOX, color="#10B981", size=20),
                                            ft.Text(item, size=13, color="#475569", expand=True)
                                        ]
                                    )
                                    for item in case.get("final_checklist", [])
                                ]
                            ]
                        )
                    ),
                    ft.Divider(height=20, color="transparent"),
                    ft.ElevatedButton(
                        "Back to Menu",
                        icon=ft.Icons.HOME,
                        bgcolor="#0B3558",
                        color="white",
                        height=45,
                        on_click=lambda e: show_steps_menu()
                    )
                ]
            )
        )
        page.update()
    
    def handle_response(response_data):
        #Manejo de res yes y no
        if "action" in response_data:
            show_action_result(response_data)
        else:
            next_step_id = response_data.get("next_step", 0)
            show_step(next_step_id)
    
    def show_step(step_id):
        #Mostrar el paso
        if step_id == 0:
            show_completion_message()
            return
        
        step = get_step(step_id)
        if not step:
            show_completion_message()
            return
        
        show_menu["value"] = False
        
        detail_text = step.get("details", "")
        
        if "procedure" in step:
            procedure_steps = "\n\nProcedure:\n" + "\n".join(
                [f"{i+1}. {proc}" for i, proc in enumerate(step["procedure"])]
            )
            detail_text += procedure_steps
        
        if "expected_result" in step:
            detail_text += f"\n\n✓ Expected Result: {step['expected_result']}"
        
        # StepCard con botón de regresar al menú
        step_card = StepCard(
            step_number=step["id"],
            title=step["title"],
            instruction=step["instruction"],
            detail=detail_text,
            question=step.get("question", ""),
            on_yes=lambda: handle_response(step.get("yes", {})),
            on_no=lambda: handle_response(step.get("no", {})),
        )
        
        card_holder.content = ft.Column(
            spacing=15,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.TextButton(
                            "← Back to Menu",
                            icon=ft.Icons.HOME_OUTLINED,
                            on_click=lambda e: show_steps_menu()
                        )
                    ]
                ),
                step_card
            ]
        )
        page.update()
    
    def create_step_card_preview(step):
        """Crea una tarjeta de vista previa para el menú"""
        return ft.Container(
            bgcolor="white",
            border_radius=10,
            border=ft.border.all(1, "#D0D7DE"),
            padding=15,
            ink=True,
            on_click=lambda e: show_step(step["id"]),
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.Container(
                                bgcolor="#0B3558",
                                border_radius=8,
                                padding=8,
                                width=40,
                                height=40,
                                content=ft.Text(
                                    str(step["id"]),
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color="white",
                                    text_align=ft.TextAlign.CENTER
                                )
                            ),
                            ft.Column(
                                spacing=4,
                                expand=True,
                                controls=[
                                    ft.Text(
                                        step["title"],
                                        size=15,
                                        weight=ft.FontWeight.BOLD,
                                        color="#0B3558"
                                    ),
                                    ft.Text(
                                        step["instruction"][:80] + "..." if len(step["instruction"]) > 80 else step["instruction"],
                                        size=12,
                                        color="#64748B"
                                    )
                                ]
                            ),
                            ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=16, color="#94A3B8")
                        ]
                    )
                ]
            )
        )
    
    def show_steps_menu():
        """Muestra el menú de selección de pasos"""
        show_menu["value"] = True
        
        steps_list = ft.Column(
            spacing=12,
            controls=[create_step_card_preview(step) for step in case["steps"]]
        )
        
        card_holder.content = ft.Column(
            spacing=20,
            controls=[
                ft.Container(
                    bgcolor="#EFF6FF",
                    border_radius=10,
                    padding=15,
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Text(
                                "Select Starting Point",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color="#0B3558"
                            ),
                            ft.Text(
                                "Choose the diagnostic step that best matches your current situation:",
                                size=13,
                                color="#475569"
                            )
                        ]
                    )
                ),
                steps_list
            ]
        )
        page.update()
    
    view = ft.View(
        route="/diagnostic",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Container(
                bgcolor="white",
                padding=15,
                border_radius=10,
                border=ft.border.all(1, "#D0D7DE"),
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.Text(case["name"], size=22, weight=ft.FontWeight.BOLD, color="#0B3558"),
                        ft.Row(
                            spacing=8,
                            controls=[
                                _chip(case["category"]),
                                _chip(case["severity"]),
                                _chip(case["estimated_repair_time"]),
                            ],
                        ),
                        ft.Container(height=1),
                        card_holder
                    ]
                )
            )
        ],
    )
    
    # Iniciar con el menú de selección
    show_steps_menu()
    
    return view

def _chip(text: str) -> ft.Container:
    return ft.Container(
        bgcolor="#E5EAF0",
        border_radius=999,
        padding=ft.padding.symmetric(10, 5),
        content=ft.Text(text, size=12, color="#475569"),
    )