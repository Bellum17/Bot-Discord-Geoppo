import matplotlib.pyplot as plt
import os
import json
from datetime import datetime, timedelta

def log_message_activity(guild_id):
    """Incrémente le compteur de messages pour le serveur chaque jour."""
    stats_file = os.path.join("data", f"stats_{guild_id}.json")
    today = datetime.now().strftime("%Y-%m-%d")
    stats = {}
    if os.path.exists(stats_file):
        with open(stats_file, "r") as f:
            stats = json.load(f)
    stats[today] = stats.get(today, 0) + 1
    with open(stats_file, "w") as f:
        json.dump(stats, f)

def generate_stats_graph(guild_id):
    """Génère un graphique du nombre de messages par jour pour le serveur."""
    stats_file = os.path.join("data", f"stats_{guild_id}.json")
    if not os.path.exists(stats_file):
        return None
    with open(stats_file, "r") as f:
        stats = json.load(f)
    dates = sorted(stats.keys())
    values = [stats[d] for d in dates]
    plt.figure(figsize=(10, 5))
    plt.plot(dates, values, marker='o')
    plt.title('Messages par jour')
    plt.xlabel('Date')
    plt.ylabel('Nombre de messages')
    plt.xticks(rotation=45)
    plt.tight_layout()
    graph_path = os.path.join("data", f"stats_graph_{guild_id}.png")
    plt.savefig(graph_path)
    plt.close()
    return graph_path
