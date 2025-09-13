import os
import sys
import win32com.client  # type: ignore

APP_NAME = "公式转换工具"


def get_paths():
    desktop = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")
    start_menu = os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs")
    return desktop, start_menu


def create_shortcut(target: str, args: str, icon: str, link_path: str):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(link_path)
    shortcut.TargetPath = target
    shortcut.Arguments = args
    shortcut.WorkingDirectory = os.path.dirname(target)
    if os.path.isfile(icon):
        shortcut.IconLocation = icon
    shortcut.Save()


def main():
    pythonw = sys.executable.replace("python.exe", "pythonw.exe")
    if not os.path.exists(pythonw):
        pythonw = sys.executable  # fallback
    project_dir = os.path.dirname(os.path.abspath(__file__))
    entry = os.path.join(project_dir, "main.py")
    icon_path = os.path.join(project_dir, "app.ico")  # optional

    desktop, start_menu = get_paths()
    desktop_link = os.path.join(desktop, f"{APP_NAME}.lnk")
    start_link = os.path.join(start_menu, f"{APP_NAME}.lnk")

    args = f'"{entry}"'
    create_shortcut(pythonw, args, icon_path, desktop_link)
    create_shortcut(pythonw, args, icon_path, start_link)
    print("已创建快捷方式：")
    print(desktop_link)
    print(start_link)


if __name__ == "__main__":
    main()
