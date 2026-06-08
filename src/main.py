import asyncio
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

def count_hidden_files(disk: str) -> int:
    try:
        ps_cmd = [
            "powershell",
            "-Command",
            f"$count=0; Get-ChildItem -Path '{disk}:\\*' -Recurse -Force -ErrorAction SilentlyContinue | ForEach-Object {{ if ($_.Attributes -band [System.IO.FileAttributes]::Hidden -or $_.Attributes -band [System.IO.FileAttributes]::System) {{ $count++ }} }}; Write-Output $count"
        ]
        pr = subprocess.Popen(ps_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
        stdout, _ = pr.communicate()
        return int(stdout.decode().strip())
    except:
        return -1

def scan(disk: str) -> dict:
    try:
        pr = subprocess.Popen(
            ["ATTRIB", "/d", "/s", "-r", "-h", "-s", f"{disk}:*"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        stdout, stderr = pr.communicate()
        if pr.returncode == 0:
            return {"success": True, "message": "Operación completada exitosamente", "error": None}
        else:
            return {"success": False, "message": "", "error": stderr.decode()}
    except FileNotFoundError:
        return {"success": False, "message": "", "error": "ATTRIB no encontrado en el sistema"}
    except PermissionError:
        return {"success": False, "message": "", "error": "Permiso denegado. Ejecutar como Administrador"}
    except Exception as e:
        return {"success": False, "message": "", "error": str(e)}

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
        try:
            unidad = drive_dropdown.value
            if not unidad:
                return

            output.controls.clear()
            output.controls.append(ft.Row(
                [ft.Text(f"Procesando unidad {unidad}:\\...")],
                alignment=ft.MainAxisAlignment.CENTER,
            ))
            output.controls.append(ft.Image(img("Magnifying Glass Tilted Right.webp"),width=180,height=180))
            page.update()

            hidden_before = await asyncio.to_thread(count_hidden_files, unidad)
            result = await asyncio.to_thread(scan, unidad)
            hidden_after = await asyncio.to_thread(count_hidden_files, unidad) if result["success"] else -1

            output.controls.clear()

            if result["success"]:
                count = hidden_before - hidden_after if hidden_before >= 0 and hidden_after >= 0 else -1
                output.controls.append(ft.Row(
                    [ft.Text("✓  ", color=ft.Colors.GREEN, size=28)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ))
                output.controls.append(ft.Row(
                    [ft.Text(result["message"], color=ft.Colors.GREEN)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ))
                if count >= 0:
                    output.controls.append(ft.Row(
                        [ft.Text(f"Archivos recuperados: {count}", weight=ft.FontWeight.BOLD)],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ))
            else:
                output.controls.append(ft.Row(
                    [ft.Text("✗  ", color=ft.Colors.RED, size=28)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ))
                output.controls.append(ft.Row(
                    [ft.Text(f"Error: {result['error']}", color=ft.Colors.RED)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ))
        except Exception as ex:
            output.controls.clear()
            output.controls.append(ft.Text(f"Error inesperado: {ex}", color=ft.Colors.RED))

        page.update()

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
        ft.Text(f'Made with ❤️ by @al3x5dev', color=ft.Colors.GREY_500)
    )


ft.run(main)
