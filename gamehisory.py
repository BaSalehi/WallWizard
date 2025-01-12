import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

def load_users(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

def create_leaderboard(games):
    sorted_games = sorted(games, key=lambda x: x.get('ID', 0), reverse=True)
    return sorted_games