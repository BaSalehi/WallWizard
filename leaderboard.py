import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

def load_users(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

def create_leaderboard(users):
    sorted_users = sorted(users, key=lambda x: x.get('score', 0), reverse=True)
    return sorted_users[:3]

def display_leaderboard(leaderboard):
    console = Console()

    onvan = Panel("LEADERBOARD", title=" ", border_style="bold blue", expand=True, padding=(1, 65), style="bold white")

    khode_leaderboard = Table(title="", title_justify="center")
    khode_leaderboard.add_column("RANK", justify="center", style="cyan", no_wrap=True)
    khode_leaderboard.add_column("USERNAME", justify="left", style="royal_blue1")
    khode_leaderboard.add_column("tafazol", justify="right", style="spring_green4")  
    khode_leaderboard.add_column("WINS", justify="right", style="bright_magenta")
    khode_leaderboard.add_column("LOSSES", justify="right", style="red")
    khode_leaderboard.add_column("TIME PLAY", justify="right", style="cyan")

    for index, user in enumerate(leaderboard):
        tafazol = user['win'] - user['lose'] 
        khode_leaderboard.add_row(str(index + 1), user['username'], str(tafazol), str(user['win']), str(user['lose']), str(user['timeplay']))

    
    console.print(onvan)
    console.print(khode_leaderboard)