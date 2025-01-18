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
    khode_leaderboard.add_column("PLAY TIME", justify="right", style="cyan")

    for index, user in enumerate(leaderboard):
        tafazol = user['wins'] - user['losses'] 
        khode_leaderboard.add_row(str(index + 1), user['username'], str(tafazol), str(user['wins']), str(user['losses']), str(user['play_time']))

    
    console.print(onvan)
    console.print(khode_leaderboard)
    
def leaderboard_main():
    file_name = 'users.json'  
    users = load_users(file_name)  
    leaderboard = create_leaderboard(users)  
    display_leaderboard(leaderboard)  


def exit_choice():
    e = input("enter e to exit: ")
    return e