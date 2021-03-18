from rich import print

def banner():
    with open('design/banner.txt') as file:
        content = file.read()
        print(f"[cyan]{content}[/]")