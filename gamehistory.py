import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

def load_games(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

def create_leaderboard(games):
    sorted_games = sorted(games, key=lambda x: x.get('ID', 0), reverse=True)
    return sorted_games

def display_gamehistory(gamehistory):
    console = Console()

    title_panel = Panel("GAME HISTORY", title=" ", border_style="bold blue", expand=True, padding=(1, 65), style="bold white")

    table = Table(title="", title_justify="center")
    table.add_column("GAME ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Player 1", justify="left", style="magenta")
    table.add_column("Player 2", justify="left", style="magenta")
    table.add_column("Winner", justify="left", style="green")

    for game in gamehistory:
        table.add_row(str(game['ID']), game['player1'], game['player2'], str(game['winner']))
    
    console.print(title_panel)
    console.print(table)
    
def gamehistory():
    file_name = 'WallWizard/games.json'
    games = load_games(file_name)  
    gamehistory = create_leaderboard(games)  
    display_gamehistory(gamehistory)  

def exit_choice():
    e = input("enter e to exit: ")
    return e
