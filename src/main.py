import flet as ft
import os, string, subprocess

APP_NAME = 'Unhide v1'

def img(img:str)->str:
    return os.path.join(os.path.dirname(__file__), "assets", img)

def get_available_drives():
    drives = []
    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"
        if os.path.exists(drive):
            if letter != "C":
                drives.append(letter)
    return drives  # ej. ['C', 'D', 'E']

async def main(page: ft.Page):
    page.title = APP_NAME
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.random())
    
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.window.width = 400
    page.window.height = 560

    page.window.icon = img("favicon.ico")

    page.window.resizable=False
    page.window.maximizable = False

    page.update()
    await page.window.center()







    async def iniciar_click(e):
        unidad = drive_dropdown.value
        

        output.controls.clear()
        output.controls.append(ft.Row(
            [ft.Text(f"Procesando unidad {unidad}:\\...")],
            alignment=ft.MainAxisAlignment.CENTER,
        ))
        output.controls.append(ft.Image(img("Magnifying Glass Tilted Right.webp"),width=180,height=180))
        page.update()

        """
        proc = subprocess.Popen(
            ["ATTRIB", "/d", "/s", "-r", "-h", "-s", f"{unidad}:\\*"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        for line in proc.stdout:
            log_output.controls.append(ft.Text(line.strip(), size=12))
            page.update()

        proc.wait()

        if proc.returncode == 0:
            log_output.controls.append(ft.Text("Proceso finalizado exitosamente.", weight=ft.FontWeight.BOLD))
        else:
            log_output.controls.append(ft.Text("Ha ocurrido un error.", color=ft.Colors.RED))
        page.update()

        btn.disabled=True
        page.update()
        """

    def habilitar_btn():
        btn.disabled=False
        page.update()



    # PREPARA DROPDOWN
    drives = get_available_drives()
    drive_dropdown = ft.Dropdown(
        label="Escanear unidad",
        options=[ft.dropdown.Option(d) for d in drives],
        width=300,
        on_select=lambda e: habilitar_btn()
    )

    # PREPARA BTN
    btn = ft.Button("🔍 ESCANEAR",on_click=iniciar_click,disabled=True)

    output = ft.ListView(expand=True, spacing=5, height=200)


    page.add(
        ft.Row(
            expand=True,
            controls=[
                ft.Column(
                    [
                        ft.Image(img('logo.png'),width=100,height=100),
                        drive_dropdown,
                        btn,
                        ft.Container(height=6),
                        output
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                    spacing=18
                )
        ]),
        ft.Text(f'Made whit ❤️ by @al3x5dev', color=ft.Colors.GREY_500)
    )


ft.run(main)
