def save_all_json_to_postgres():
    """Sauvegarde tous les fichiers JSON dans PostgreSQL via backup_json_to_postgres.py."""
    try:
        os.system(f"python3 backup_json_to_postgres.py")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde PostgreSQL : {e}")

def restore_all_json_from_postgres():
    """Restaure tous les fichiers JSON depuis PostgreSQL via restore_json_from_postgres.py."""
    try:
        os.system(f"python3 restore_json_from_postgres.py")
    except Exception as e:
        print(f"Erreur lors de la restauration PostgreSQL : {e}")
import os
import sys
import json
import time

import discord
from discord.ext import commands
from discord import app_commands
import json
xp_system_status_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "xp_system_status.json")
def load_xp_system_status():
    if os.path.exists(xp_system_status_path):
        with open(xp_system_status_path, 'r') as f:
            return json.load(f)
    return {"servers": {}}

def save_xp_system_status(status):
    with open(xp_system_status_path, 'w') as f:
        json.dump(status, f, indent=4)

xp_system_status = load_xp_system_status()
import time
import datetime
import asyncio
import typing
import random
import sys
import atexit
import signal
import aiohttp
import io
import textwrap
import re
import geopandas as gpd
import numpy as np
from shapely.ops import unary_union
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from PIL import Image, ImageDraw, ImageFont # type: ignore
from dotenv import load_dotenv
from discord.ext.tasks import loop

# Chargement des variables d'environnement
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("ERREUR: DISCORD_TOKEN n'est pas défini dans le fichier .env")
    print("Créez un fichier .env avec DISCORD_TOKEN=votre_token_discord")
    sys.exit(1)

# Configuration du répertoire de base et des constantes
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMBED_COLOR = 0xefe7c5
IMAGE_URL = "https://zupimages.net/up/21/03/vl8j.png"
MONNAIE_EMOJI = "<:Monnaie:1412039375063355473>"
INVISIBLE_CHAR = "⠀"
HELP_THUMBNAIL_URL = "https://cdn.discordapp.com/attachments/1411865291041931327/1422937730177826827/c4959984-ba58-486b-a7c3-a17b231b80a9.png?ex=68de7d87&is=68dd2c07&hm=78336c03ba0fbcfd847d2e7a4e14307b2ecc964b97be95648fbc2a1a9884da9c&"
HELP_HEADER_IMAGE_URL = "https://cdn.discordapp.com/attachments/1412872314525192233/1422963949682561096/Capture_decran_2025-10-01_a_17.10.31.png?ex=68de95f2&is=68dd4472&hm=75f6f6e77beb2dc7d09e85cf105a6dbd10570f08794388287ebdcf21e3645f2e&"
HELP_HEADER_SEPARATOR = "-# ─────────────────────────────"
WELCOME_ROLE_ID = 1393340583665209514
WELCOME_CHANNEL_ID = 1416882330576097310
WELCOME_PUBLIC_MESSAGE = (
    "### <:PX_Festif:1423426894019297381> Bienvenue à toi ! {mention}\n"
    "> ▪︎ Ce serveur est actuellement en cours de refonte et rouvrira très prochainement, dans les semaines à venir, voire dans les prochains jours. Si tu as besoin de renseignements, le salon <#1393318935692312787> a été mis à jour depuis et le staff reste à ta disposition pour répondre à tes questions. En attendant, nous t’invitons à faire connaissance avec les autres membres et à patienter sereinement jusqu’à la réouverture du rôleplay !"
)
WELCOME_DM_MESSAGE = (
    "### <:PX_Festif:1423426894019297381> Bienvenue à toi !\n"
    "> ▪︎ Ce serveur est actuellement en cours de refonte et rouvrira très prochainement, dans les semaines à venir, voire dans les prochains jours. Si tu as besoin de renseignements, le salon <#1393318935692312787> a été mis à jour depuis et le staff reste à ta disposition pour répondre à tes questions. En attendant, nous t’invitons à faire connaissance avec les autres membres et à patienter sereinement jusqu’à la réouverture du rôleplay !\n\n"
    "-# Envoyé depuis le serveur 𝐏𝐀𝐗 𝐑𝐔𝐈𝐍𝐀𝐄."
)
HELP_VIEW_TOP_URL = "https://cdn.discordapp.com/attachments/1411865291041931327/1423095868201898055/72de43e34dc04d4fab20473c798afb67.png?ex=68df10ce&is=68ddbf4e&hm=c5e6e9bd6f73f6945f05404d28df207d47156a1ac42acaf66293422bb30bd33d&"
HELP_VIEW_BOTTOM_URL = "https://cdn.discordapp.com/attachments/1411865291041931327/1423095868470460496/0e19006685eb40119c16b69826b91c56.png?ex=68df10ce&is=68ddbf4e&hm=9fb6ed54561624910b84ea69eabad8695230219daaa72ad44dbe097f11278023&"

# === Configuration générale du bot ===
PRIMARY_GUILD_ID = 1393301496283795640
PERMANENT_STATUS_TEXT = "Gestionne les Nations"

# Chemins des fichiers de données
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

BALANCE_FILE = os.path.join(DATA_DIR, "balances.json")
LOG_FILE = os.path.join(DATA_DIR, "log_channel.json")
MESSAGE_LOG_FILE = os.path.join(DATA_DIR, "message_log_channel.json")
LOANS_FILE = os.path.join(DATA_DIR, "loans.json")
PIB_FILE = os.path.join(DATA_DIR, "pib.json")
BALANCE_BACKUP_FILE = os.path.join(DATA_DIR, "balances_backup.json")
TRANSACTION_LOG_FILE = os.path.join(DATA_DIR, "transactions.json")
PAYS_LOG_FILE = os.path.join(DATA_DIR, "pays_log_channel.json")
PAYS_IMAGES_FILE = os.path.join(DATA_DIR, "pays_images.json")
MUTE_LOG_FILE = os.path.join(DATA_DIR, "mute_log_channel.json")

# === XP/LEVEL SYSTEM ===
LVL_FILE = os.path.join(DATA_DIR, "levels.json")
LVL_LOG_CHANNEL_FILE = os.path.join(DATA_DIR, "lvl_log_channel.json")

def load_levels():
    if not os.path.exists(LVL_FILE):
        with open(LVL_FILE, "w") as f:
            json.dump({}, f)
    try:
        with open(LVL_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement des niveaux: {e}")
        return {}

def save_levels(data):
    try:
        with open(LVL_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des niveaux: {e}")

def load_lvl_log_channel():
    if not os.path.exists(LVL_LOG_CHANNEL_FILE):
        with open(LVL_LOG_CHANNEL_FILE, "w") as f:
            json.dump({}, f)
    try:
        with open(LVL_LOG_CHANNEL_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement du salon de log lvl: {e}")
        return {}

def save_lvl_log_channel(data):
    try:
        with open(LVL_LOG_CHANNEL_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du salon de log lvl: {e}")

levels = load_levels()
lvl_log_channel_data = load_lvl_log_channel()

def xp_for_level(level):
    if level > 100:
        return None
    if level <= 1:
        return 10
    elif level == 2:
        return 20
    else:
        return 2 * xp_for_level(level - 1)

def get_progress_bar(xp, level):
    total = xp_for_level(level)
    percent = int((xp / total) * 100) if total > 0 else 0
    filled = percent // 10
    if percent == 0:
        bar = "<:Barre2_Vide:1417667900596027522>"
    else:
        bar = "<:Barre2_Rempli:1417667907508244581>"
    for i in range(1, 10):
        if i <= filled:
            bar += "<:Barre1_Rempli:1417667903905595583>"
        else:
            bar += "<:Barre1_Vide:1417667899153186928>"
    if percent == 100:
        bar += "<:Barre3_Rempli:1417667906027913226>"
    else:
        bar += "<:Barre3_Vide:1417667902471147520>"
    return f"{bar} — {percent}%"

# Configuration PIB
PIB_DEFAULT = 0

# Variables globales pour le suivi de l'état du bot
BOT_START_TIME = time.time()
BOT_DISCONNECT_HANDLED = False

# Configuration des intents Discord
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# Définition d'une classe pour la pagination
class PaginationView(discord.ui.View):
    """Une vue pour la pagination des embeds avec boutons."""
    
    def __init__(self, pages, author_id, timeout=60):
        super().__init__(timeout=timeout)
        self.pages = pages
        self.author_id = author_id
        self.current_page = 0
    
    @discord.ui.button(label="◀️", style=discord.ButtonStyle.secondary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Page précédente."""
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Vous n'êtes pas autorisé à utiliser ces boutons.", ephemeral=True)
            return

        self.current_page = max(0, self.current_page - 1)
        await interaction.response.edit_message(embed=self.pages[self.current_page])
    
    @discord.ui.button(label="▶️", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Page suivante."""
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Vous n'êtes pas autorisé à utiliser ces boutons.", ephemeral=True)
            return

        self.current_page = min(len(self.pages) - 1, self.current_page + 1)
        await interaction.response.edit_message(embed=self.pages[self.current_page])

# Définition de la classe du bot
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Suppression de toutes les commandes distantes puis resynchronisation globale
        print("Synchronisation globale des commandes slash...")
        try:
            cmds = await self.tree.sync()
            print(f"Commandes globales synchronisées ({len(cmds)}) : {[c.name for c in cmds]}")
        except Exception as e:
            print(f"Erreur lors de la synchronisation globale : {e}")
        
        # Démarrer les tâches planifiées
        auto_save_economy.start()
        verify_and_fix_balances.start()
        
        print("Bot prêt et tâches planifiées démarrées.")

# Création de l'instance du bot

bot = MyBot()


async def apply_permanent_presence(client: commands.Bot) -> None:
    """Applique le statut permanent configuré pour le bot."""
    try:
        activity = discord.CustomActivity(name=PERMANENT_STATUS_TEXT)
        await client.change_presence(status=discord.Status.online, activity=activity)
    except Exception as exc:
        # Discord refuse parfois les statuts personnalisés pour les bots ; on journalise pour diagnostic.
        print(f"[DEBUG] Impossible de définir l'activité personnalisée : {exc}")
        await client.change_presence(status=discord.Status.online)


# === COMMANDE POUR ENREGISTRER LES IDS DES MEMBRES ===

# === COMMANDE DE SUPPRESSION DE MESSAGES ===
@bot.tree.command(name="purge", description="Supprime un nombre de messages dans ce salon (max 1000)")
@app_commands.checks.has_permissions(manage_messages=True)
async def purge(interaction: discord.Interaction, nombre: int):
    await interaction.response.defer(ephemeral=True)
    if nombre < 1 or nombre > 1000:
        await interaction.followup.send("Le nombre doit être entre 1 et 1000.", ephemeral=True)
        return
    channel = interaction.channel
    try:
        deleted = await channel.purge(limit=nombre)
        await interaction.followup.send(f"{len(deleted)} messages supprimés.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"Erreur lors de la suppression : {e}", ephemeral=True)

@bot.event
async def on_guild_join(guild: discord.Guild):
    await apply_permanent_presence(bot)
    try:
        await bot.tree.sync(guild=discord.Object(id=guild.id))
        print(f"[INFO] Commandes synchronisées pour la guild {guild.name} ({guild.id})")
    except Exception as exc:
        print(f"[WARN] Échec de synchronisation sur la guild {guild.id} : {exc}")


# Variables globales pour les données
balances = {}
log_channel_data = {}
# Variables globales pour les données
balances = {}
log_channel_data = {}
message_log_channel_data = {}
loans = []
pib_data = {}
pays_log_channel_data = {}
pays_images = {}
mute_log_channel_data = {}

# Chargement des balances et autres données après la définition de la fonction
# (L'appel à load_all_data() est déplacé après la définition de la fonction)
def format_number(number):
    """Formate un nombre pour l'affichage avec séparateurs de milliers."""
    if isinstance(number, int):
        return f"{number:,}".replace(",", " ")
    return str(number)

# ===== FONCTIONS DE GESTION DES DONNÉES =====

# Fonction pour charger toutes les données
def load_all_data():
    """Charge toutes les données nécessaires au démarrage."""
    global balances, log_channel_data, message_log_channel_data, loans, pib_data, pays_log_channel_data, pays_images, mute_log_channel_data
    
    # Chargement de toutes les données
    balances.update(load_balances())
    log_channel_data.update(load_log_channel())
    message_log_channel_data.update(load_message_log_channel())
    loans.extend(load_loans())
    pib_data.update(load_pib())
    pays_log_channel_data.update(load_pays_log_channel())
    pays_images.update(load_pays_images())
## Fonction de chargement du canal de statut supprimée (obsolète)

def load_pays_images():
    """Charge les images des pays depuis le fichier."""
    if not os.path.exists(PAYS_IMAGES_FILE):
        with open(PAYS_IMAGES_FILE, "w") as f:
            json.dump({}, f)
    try:
        with open(PAYS_IMAGES_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement des images de pays: {e}")
        return {}

def save_pays_images(data):
    """Sauvegarde les images des pays dans le fichier."""
    try:
        with open(PAYS_IMAGES_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des images de pays: {e}")



def load_balances():
    """Charge les données des balances depuis le fichier."""
    balances_data = {}
    
    # Essayer de charger le fichier principal
    try:
        if os.path.exists(BALANCE_FILE):
            with open(BALANCE_FILE, "r") as f:
                balances_data = json.load(f)
                print(f"Balances chargées depuis {BALANCE_FILE}: {len(balances_data)} entrées")
    except Exception as e:
        print(f"Erreur lors du chargement des balances principales: {e}")
    
    # Si le fichier principal est vide ou corrompu, essayer le backup
    if not balances_data and os.path.exists(BALANCE_BACKUP_FILE):
        try:
            with open(BALANCE_BACKUP_FILE, "r") as f:
                balances_data = json.load(f)
                print(f"Balances restaurées depuis la sauvegarde: {len(balances_data)} entrées")
        except Exception as e:
            print(f"Erreur lors du chargement de la sauvegarde des balances: {e}")
    
    # Si aucun fichier n'existe, créer un fichier vide
    if not balances_data:
        balances_data = {}
        print("Création d'un nouveau fichier de balances")
    
    # Créer les fichiers s'ils n'existent pas
    if not os.path.exists(BALANCE_FILE):
        with open(BALANCE_FILE, "w") as f:
            json.dump(balances_data, f)
    if not os.path.exists(BALANCE_BACKUP_FILE):
        with open(BALANCE_BACKUP_FILE, "w") as f:
            json.dump(balances_data, f)
    
    return balances_data

def save_balances(balances_data):
    """Sauvegarde les balances dans le fichier."""
    # Sauvegarde principale
    try:
        with open(BALANCE_FILE, "w") as f:
            json.dump(balances_data, f)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des balances: {e}")
    
    # Sauvegarde de secours (moins fréquente pour éviter l'usure du disque)
    if random.random() < 0.2:  # 20% de chance de faire un backup
        try:
            with open(BALANCE_BACKUP_FILE, "w") as f:
                json.dump(balances_data, f)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de secours des balances: {e}")

def load_log_channel():
    """Charge les données du canal de log."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump({}, f)
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement des logs: {e}")
        return {}

def save_log_channel(data):
    """Sauvegarde les données du canal de log."""
    try:
        with open(LOG_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des logs: {e}")

def load_message_log_channel():
    """Charge les données du canal de log des messages."""
    if not os.path.exists(MESSAGE_LOG_FILE):
        with open(MESSAGE_LOG_FILE, "w") as f:
            json.dump({}, f)
    try:
        with open(MESSAGE_LOG_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement des logs de messages: {e}")
        return {}

def save_message_log_channel(data):
    """Sauvegarde les données du canal de log des messages."""
    try:
        with open(MESSAGE_LOG_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des logs de messages: {e}")

def load_loans():
    """Charge les données des prêts."""
    if not os.path.exists(LOANS_FILE):
        with open(LOANS_FILE, "w") as f:
            json.dump([], f)
    try:
        with open(LOANS_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement des prêts: {e}")
        return []

def save_loans(loans_data):
    """Sauvegarde les données des prêts."""
    try:
        with open(LOANS_FILE, "w") as f:
            json.dump(loans_data, f)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des prêts: {e}")

def load_pib():
    """Charge les données du PIB."""
    if not os.path.exists(PIB_FILE):
        return {}  # Ne crée pas le fichier, retourne juste un dict vide
    try:
        with open(PIB_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement du PIB: {e}")
        return {}

def save_pib(pib_data):
    """Sauvegarde les données du PIB et synchronise avec PostgreSQL."""
    try:
        # Si le dictionnaire est vide, supprimer le fichier
        if not pib_data:
            if os.path.exists(PIB_FILE):
                os.remove(PIB_FILE)
                print("Fichier pib.json supprimé car aucun pays n'a de PIB.")
        else:
            # Créer le fichier seulement s'il y a des données
            with open(PIB_FILE, "w") as f:
                json.dump(pib_data, f, indent=2)
        save_all_json_to_postgres()
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du PIB: {e}")

def load_pays_log_channel():
    """Charge les données du canal de log des pays."""
    if not os.path.exists(PAYS_LOG_FILE):
        with open(PAYS_LOG_FILE, "w") as f:
            json.dump({}, f)
    try:
        with open(PAYS_LOG_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement du canal de log des pays: {e}")
        return {}

def save_pays_log_channel(data):
    """Sauvegarde les données du canal de log des pays."""
    try:
        with open(PAYS_LOG_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du canal de log des pays: {e}")

## Fonction de sauvegarde du canal de statut supprimée (obsolète)

def log_transaction(from_id, to_id, amount, transaction_type, guild_id):
    """
    Journalise une transaction dans l'historique, sans modifier les balances.
    Les balances sont déjà modifiées par les commandes correspondantes.
    """
    transaction = {
        "from_id": from_id,
        "to_id": to_id,
        "amount": amount,
        "timestamp": int(time.time()),
        "type": transaction_type,
        "guild_id": guild_id
    }
    
    # Charger les transactions existantes
    transactions = []
    if os.path.exists(TRANSACTION_LOG_FILE):
        try:
            with open(TRANSACTION_LOG_FILE, "r") as f:
                transactions = json.load(f)
        except json.JSONDecodeError:
            transactions = []
    
    # Ajouter la nouvelle transaction
    transactions.append(transaction)
    
    # Limiter l'historique à 1000 transactions
    if len(transactions) > 1000:
        transactions = transactions[-1000:]
    
    # Sauvegarder les transactions
    try:
        with open(TRANSACTION_LOG_FILE, "w") as f:
            json.dump(transactions, f)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de la transaction: {e}")
    
    # Ne PAS modifier les balances ici, car elles sont déjà modifiées par les commandes

# ===== FONCTION DE LOG =====

# Fonction pour envoyer un log au format embed
async def send_log(guild, message=None, embed=None):
    """
    Envoie un message dans le salon de log économique du serveur.
    Prend soit un message texte simple, soit un embed déjà formaté.
    """
    log_channel_id = log_channel_data.get(str(guild.id))
    if log_channel_id:
        channel = guild.get_channel(int(log_channel_id))
        if channel:
            try:
                # Si un embed est déjà fourni, l'utiliser directement
                if embed:
                    await channel.send(embed=embed)
                # Sinon créer un embed à partir du message texte
                elif message:
                    log_embed = discord.Embed(
                        description=f"{message}{INVISIBLE_CHAR}",
                        color=EMBED_COLOR,
                        timestamp=datetime.datetime.now()
                    )
                    await channel.send(embed=log_embed)
            except Exception as e:
                print(f"Erreur lors de l'envoi du log: {e}")

# Fonction pour envoyer un log de pays
async def send_pays_log(guild, embed):
    """Envoie un embed dans le salon de log des pays du serveur."""
    pays_log_channel_id = pays_log_channel_data.get(str(guild.id))
    if pays_log_channel_id:
        channel = guild.get_channel(int(pays_log_channel_id))
        if channel:
            try:
                await channel.send(embed=embed)
            except Exception as e:
                print(f"Erreur lors de l'envoi du log de pays: {e}")

# Fonction pour envoyer un log de mute
async def send_mute_log(guild, embed):
    """Envoie un embed dans le salon de log des sanctions mute/unmute du serveur."""
    mute_log_channel_id = mute_log_channel_data.get(str(guild.id))
    if mute_log_channel_id:
        channel = guild.get_channel(int(mute_log_channel_id))
        if channel:
            try:
                await channel.send(embed=embed)
            except Exception as e:
                print(f"Erreur lors de l'envoi du log mute: {e}")

# ===== TÂCHES PLANIFIÉES =====

@loop(minutes=10)
async def auto_save_economy():
    """Sauvegarde automatique de l'économie."""
    try:
        print("Sauvegarde automatique de l'économie...")
        save_balances(balances)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde automatique: {e}")

@loop(hours=12)
async def verify_and_fix_balances():
    """Vérifie et corrige les balances périodiquement."""
    try:
        print("Vérification périodique des balances...")
        
        # Recherche des montants anormalement élevés
        abnormal_balances = {}
        for role_id, amount in balances.items():
            if len(role_id) >= 18 and amount > 3000000000:  # Plus de 3 milliards est suspect
                corrected_amount = amount // 3
                abnormal_balances[role_id] = (amount, corrected_amount)
                balances[role_id] = corrected_amount
        
        if abnormal_balances:
            print(f"CORRECTION PÉRIODIQUE: {len(abnormal_balances)} soldes anormalement élevés ont été corrigés")
            for role_id, (old_amount, new_amount) in abnormal_balances.items():
                print(f"  - ID {role_id}: {old_amount} -> {new_amount}")
            save_balances(balances)
            
    except Exception as e:
        print(f"Erreur lors de la vérification périodique des balances: {e}")

# ===== GESTIONNAIRES DE SIGNAUX =====

def signal_handler(sig, frame):
    """Gestionnaire de signal pour la fermeture propre."""
    print(f"Signal {sig} reçu, fermeture en cours...")
    
    # Sauvegarde des données importantes
    try:
        save_balances(balances)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde finale: {e}")
    
    # Attendre un peu pour permettre la sauvegarde des données
    time.sleep(1)
    
    # Forcer la sortie sans attendre d'opérations asynchrones
    sys.exit(0)

def exit_handler():
    """Gestionnaire pour atexit."""
    global BOT_DISCONNECT_HANDLED
    if not BOT_DISCONNECT_HANDLED:
        print("Fermeture du bot en cours...")
        BOT_DISCONNECT_HANDLED = True
        
        # Sauvegarde des données importantes
        try:
            save_balances(balances)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde finale: {e}")

def verify_economy_data(bot):
    """Vérifie l'intégrité des données économiques au démarrage."""
    print("Vérification des données économiques...")
    
    # Vérifier les balances négatives
    negative_balances = {}
    for entity_id, amount in balances.items():
        if amount < 0:
            negative_balances[entity_id] = amount
            # Correction automatique
            balances[entity_id] = 0
    
    if negative_balances:
        print(f"AVERTISSEMENT: {len(negative_balances)} soldes négatifs ont été corrigés")
        save_balances(balances)
    
    # Correction des montants anormalement élevés
    abnormal_balances = {}
    for role_id, amount in balances.items():
        # Vérifier si c'est un rôle et non un utilisateur (les IDs de rôle ont généralement 18-19 chiffres)
        if len(role_id) >= 18 and amount > 3000000000:  # Plus de 3 milliards est suspect
            # Calcul de la valeur normale (divisé par 3 car semble être triplé)
            corrected_amount = amount // 3
            abnormal_balances[role_id] = (amount, corrected_amount)
            balances[role_id] = corrected_amount
            print(f"Correction de balance pour ID {role_id}: {amount} -> {corrected_amount}")
    
    if abnormal_balances:
        print(f"AVERTISSEMENT: {len(abnormal_balances)} soldes anormalement élevés ont été corrigés")
        save_balances(balances)
    
    print("Vérification des données économiques terminée")

def verify_and_fix_budgets():
    """Vérifie et corrige les budgets au démarrage du bot."""
    print("Vérification des budgets...")
    
    # Identifier les budgets problématiques (trop élevés)
    problematic_budgets = []
    for user_id, amount in balances.items():
        # Si le budget est supérieur à 2 milliards, c'est probablement une erreur
        if amount > 2000000000:
            problematic_budgets.append((user_id, amount))
    
    # Corriger les budgets problématiques
    for user_id, amount in problematic_budgets:
        print(f"Budget anormal détecté - ID: {user_id}, Montant: {amount}")
        
    print(f"Vérification terminée: {len(problematic_budgets)} budgets anormaux détectés")

# ===== ÉVÉNEMENTS DU BOT =====

@bot.event
async def on_message_delete(message):
    """Journalise les messages supprimés."""
    if message.guild is None:  # Ignore DM messages
        return
    # Ignore si le message vient d'un salon de logs
    log_channels = []
    log_channel_id = log_channel_data.get(str(message.guild.id))
    msg_log_channel_id = message_log_channel_data.get(str(message.guild.id))
    if log_channel_id:
        log_channels.append(int(log_channel_id))
    if msg_log_channel_id:
        log_channels.append(int(msg_log_channel_id))
    if message.channel.id in log_channels:
        return
    channel = None
    msg_log_channel_id = message_log_channel_data.get(str(message.guild.id))
    if msg_log_channel_id:
        channel = message.guild.get_channel(int(msg_log_channel_id))
    if channel:
        try:
            embed = discord.Embed(
                title="Message supprimé",
                description=f"**Auteur :** {message.author.mention}\n**Salon :** {message.channel.mention}\n**Contenu :**\n{message.content}",
                color=discord.Color.red()
            )
            await channel.send(embed=embed)
        except Exception as e:
            print(f"Erreur lors de la journalisation d'un message supprimé: {e}")

@bot.event
async def on_message_edit(before, after):
    """Journalise les messages modifiés."""
    if before.guild is None:  # Ignore DM messages
        return
    if before.author.bot:
        return
    log_channels = []
    log_channel_id = log_channel_data.get(str(before.guild.id))
    msg_log_channel_id = message_log_channel_data.get(str(before.guild.id))
    if log_channel_id:
        log_channels.append(int(log_channel_id))
    if msg_log_channel_id:
        log_channels.append(int(msg_log_channel_id))
    if before.channel.id in log_channels:
        return
    # Fonction utilitaire pour obtenir le salon de log des messages
    def get_message_log_channel(guild):
        msg_log_channel_id = message_log_channel_data.get(str(guild.id))
        if msg_log_channel_id:
            return guild.get_channel(int(msg_log_channel_id))
        return None

    channel = get_message_log_channel(before.guild)
    if channel:
        try:
            embed = discord.Embed(
                title="Message modifié",
                description=f"**Auteur :** {before.author.mention}\n**Salon :** {before.channel.mention}\n**Avant :**\n{before.content}\n**Après :**\n{after.content}",
                color=discord.Color.orange()
            )
            await channel.send(embed=embed)
        except Exception as e:
            print(f"Erreur lors de la journalisation d'un message modifié: {e}")

@bot.event
async def on_command_error(ctx, error):
    """Gère les erreurs de commandes."""
    print(f"Erreur de commande: {error}")

@bot.event
async def on_error(event, *args, **kwargs):
    """Gère les erreurs d'événements."""
    print(f"Erreur dans l'événement {event}: {sys.exc_info()[0]}")

# Ajout de l'événement on_message pour l'XP
xp_system_active = False  # Obsolète, remplacé par xp_system_status

@bot.event
async def on_message(message):
    global levels, xp_system_status
    if message.author.bot or not message.guild:
        return
    guild_id = str(message.guild.id)
    if not xp_system_status["servers"].get(guild_id, False):
        await bot.process_commands(message)
        return
    user_id = str(message.author.id)
    if user_id not in levels:
        levels[user_id] = {"xp": 0, "level": 1}
    # Calcul XP : 1 XP de base + 1 XP tous les 10 caractères
    char_count = len(message.content)
    # Bonus XP par grade acquis
    palier_roles = {
        10: 1417893183903502468,
        20: 1417893555376230570,
        30: 1417893729066291391,
        40: 1417893878136176680,
        50: 1417894464122261555,
        60: 1417894846844244139,
        70: 1417895041862733986,
        80: 1417895157553958922,
        90: 1417895282443812884,
        100: 1417895415273099404
    }
    member = message.guild.get_member(message.author.id)
    bonus_grade = 0
    if member:
        for i, role_id in enumerate(palier_roles.values(), start=1):
            if discord.utils.get(member.roles, id=role_id):
                bonus_grade += i
    # Rôle spécial
    special_role_id = 1393303261519417385
    has_special = member and discord.utils.get(member.roles, id=special_role_id)
    xp_chair = char_count // 10  # XP chair (1 XP tous les 10 caractères)
    if has_special:
        xp_gain = 5 + (char_count // 15) * 2 + xp_chair
    else:
        xp_gain = 1 + xp_chair + bonus_grade
    levels[user_id]["xp"] += xp_gain
    xp = levels[user_id]["xp"]
    level = levels[user_id]["level"]
    next_level_xp = xp_for_level(level)
    save_levels(levels)
    try:
        save_all_json_to_postgres()
    except Exception as e:
        print(f"[ERROR] Sauvegarde PostgreSQL après message : {e}")
    if xp >= next_level_xp:
        levels[user_id]["level"] += 1
        levels[user_id]["xp"] = xp - next_level_xp
        save_levels(levels)
        try:
            save_all_json_to_postgres()
        except Exception as e:
            print(f"[ERROR] Sauvegarde PostgreSQL après message : {e}")
        # Gestion des rôles de palier
        palier_roles = {
            10: 1417893183903502468,
            20: 1417893555376230570,
            30: 1417893729066291391,
            40: 1417893878136176680,
            50: 1417894464122261555,
            60: 1417894846844244139,
            70: 1417895041862733986,
            80: 1417895157553958922,
            90: 1417895282443812884,
            100: 1417895415273099404
        }
        palier = (levels[user_id]["level"] // 10) * 10
        member = message.guild.get_member(message.author.id)
        # Ajout du nouveau rôle de palier si atteint
        if palier in palier_roles and member and levels[user_id]["level"] % 10 == 0:
                new_role = message.guild.get_role(palier_roles[palier])
                if new_role:
                    await member.add_roles(new_role)
                    # Retrait de l'ancien rôle de palier
                    old_palier = palier - 10
                    if old_palier in palier_roles:
                        old_role = message.guild.get_role(palier_roles[old_palier])
                        if old_role:
                            await member.remove_roles(old_role)
                    # Log d'attribution du rôle (embed stylisé)
                    lvl_channel_id = lvl_log_channel_data.get(guild_id)
                    if lvl_channel_id:
                        channel = message.guild.get_channel(int(lvl_channel_id))
                        if channel:
                            await channel.send(f"> − {member.mention}")
                            embed = discord.Embed(
                                description=(
                                    "⠀\n"
                                    f"> ## {message.author.mention} a obtenu le grade de {new_role.mention} au **niveau {levels[user_id]['level']} !** 🎉\n"
                                    "⠀"
                                ),
                                color=0x162e50
                            )
                            embed.set_image(url="https://cdn.discordapp.com/attachments/1412872314525192233/1417983114390536363/PAX_RUINAE_5.gif?ex=68cc772f&is=68cb25af&hm=f095b505d44febce0e7a8cbf52fea9ac14c79aacaa17762ec66cb4d22ccc6b4d&")
                            await channel.send(embed=embed)
        # Log passage de niveau (embed stylisé)
        lvl_channel_id = lvl_log_channel_data.get(guild_id)
        if lvl_channel_id:
            channel = message.guild.get_channel(int(lvl_channel_id))
            if channel:
                await channel.send(f"> − {message.author.mention}")
                embed = discord.Embed(
                    description=(
                        "⠀\n"
                        f"> ## {message.author.mention} est passé au **niveau {levels[user_id]['level']} !** 🎉\n"
                        "⠀"
                    ),
                    color=0x162e50
                )
                embed.set_image(url="https://cdn.discordapp.com/attachments/1412872314525192233/1417983114390536363/PAX_RUINAE_5.gif?ex=68cc772f&is=68cb25af&hm=f095b505d44febce0e7a8cbf52fea9ac14c79aacaa17762ec66cb4d22ccc6b4d&")
                await channel.send(embed=embed)
# Commande pour ajouter de l'XP à un membre

# ===== COMMANDES DE BASE =====

@bot.tree.command(name="setlogeconomy", description="Définit le salon de logs pour l'économie")
@app_commands.checks.has_permissions(administrator=True)
async def setlogeconomy(interaction: discord.Interaction, channel: discord.TextChannel):
    log_channel_data[str(interaction.guild.id)] = channel.id
    save_log_channel(log_channel_data)
    embed = discord.Embed(
        description=f"> Salon de logs défini sur {channel.mention}.{INVISIBLE_CHAR}",
        color=EMBED_COLOR
    )
    embed.set_image(url=IMAGE_URL)
    await interaction.response.send_message(embed=embed, ephemeral=True)


# Fonction utilitaire pour convertir les majuscules en caractères spéciaux
def is_valid_image_url(url):
    """Vérifie si l'URL pointe vers une image valide."""
    if not url:
        return False
    # ...existing code...
    # Traitement XP, économie, etc. (déjà présent)
    # Synchronisation automatique PostgreSQL à chaque message
    try:
        save_all_json_to_postgres()
    except Exception as e:
        print(f"[ERROR] Sauvegarde PostgreSQL après message : {e}")
    # ...existing code...
    # Vérification simple des extensions d'image communes
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
    url_lower = url.lower()
    
    # Vérifier si l'URL se termine par une extension d'image
    for ext in image_extensions:
        if url_lower.endswith(ext):
            return True
    
    # Vérifier si c'est une URL d'hébergement d'images connue
    image_hosts = ['imgur.com', 'i.imgur.com', 'zupimages.net', 'tenor.com', 
                   'media.discordapp.net', 'cdn.discordapp.com']
    
    for host in image_hosts:
        if host in url_lower:
            return True
    
    # URLs qui contiennent des paramètres mais sont des images
    if re.search(r'\.(jpg|jpeg|png|gif|webp|bmp)(\?|#)', url_lower):
        return True
    
    return False

def convert_to_bold_letters(text):
    """Convertit les lettres majuscules en caractères gras spéciaux."""
    bold_letters = {
        'A': '𝗔', 'B': '𝗕', 'C': '𝗖', 'D': '𝗗', 'E': '𝗘', 'F': '𝗙', 'G': '𝗚', 'H': '𝗛', 'I': '𝗜',
        'J': '𝗝', 'K': '𝗞', 'L': '𝗟', 'M': '𝗠', 'N': '𝗡', 'O': '𝗢', 'P': '𝗣', 'Q': '𝗤', 'R': '𝗥',
        'S': '𝗦', 'T': '𝗧', 'U': '𝗨', 'V': '𝗩', 'W': '𝗪', 'X': '𝗫', 'Y': '𝗬', 'Z': '𝗭'
    }
    
    result = ""
    for char in text:
        if char.isupper() and char in bold_letters:
            result += bold_letters[char]
        else:
            result += char
    
    return result

# Pour la commande creer_pays, ajouter ces rôles à la gestion
@bot.tree.command(name="creer_pays", description="Crée un nouveau pays avec son rôle et son salon")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(
    nom="Nom du pays",
    budget="Budget initial du pays",
    pib="PIB du pays (valeur informative)",
    continent="Continent auquel appartient le pays",
    categorie="Catégorie où créer le salon du pays",
    dirigeant="Utilisateur qui sera le dirigeant du pays",
    drapeau_salon="Emoji à ajouter au début du nom du pays (facultatif)",
    drapeau_perso="Emoji personnalisé du pays pour les messages et l'icône du rôle (facultatif)",
    couleur="Code couleur hexadécimal pour le rôle (ex: #FF0000 pour rouge, facultatif)",
    image="URL d'une image représentant le pays (facultatif)",
    nom_salon_secret="Nom du salon secret à créer (facultatif)",
    categorie_secret="Catégorie où créer le salon secret (facultatif)",
    economie="Type d'économie du pays (facultatif)",
    regime_politique="Régime politique du pays (facultatif)",
    gouvernement="Forme de gouvernement du pays (facultatif)"
)
@app_commands.choices(continent=[
    discord.app_commands.Choice(name="Europe", value="1413995502785138799"),
    discord.app_commands.Choice(name="Afrique", value="1413995608922128394"),
    discord.app_commands.Choice(name="Amérique", value="1413995735732457473"),
    discord.app_commands.Choice(name="Asie", value="1413995874304004157"),
    discord.app_commands.Choice(name="Océanie", value="1413996176956461086")
])
@app_commands.choices(economie=[
    discord.app_commands.Choice(name="Économie ultra-libérale", value="1417234199353622569"),
    discord.app_commands.Choice(name="Économie libérale", value="1417234220115431434"),
    discord.app_commands.Choice(name="Économie mixte", value="1417234887508754584"),
    discord.app_commands.Choice(name="Socialisme de marché", value="1417234944832442621"),
    discord.app_commands.Choice(name="Économie planifiée", value="1417234931146555433"),
    discord.app_commands.Choice(name="Économie dirigiste", value="1417235038168289290"),
    discord.app_commands.Choice(name="Économie corporatiste", value="1417235052814794853")
])
@app_commands.choices(regime_politique=[
    discord.app_commands.Choice(name="Démocratie", value="1417251476782448843"),
    discord.app_commands.Choice(name="Autoritarisme", value="1417251480573968525"),
    discord.app_commands.Choice(name="Totalitarisme", value="1417251556776218654"),
    discord.app_commands.Choice(name="Monarchie", value="1417251565068226691"),
    discord.app_commands.Choice(name="Oligarchie", value="1417251568327200828"),
    discord.app_commands.Choice(name="Théocratie", value="1417251571661537320"),
    discord.app_commands.Choice(name="Technocratie", value="1417251574568456232"),
    discord.app_commands.Choice(name="Régime populaire", value="1417251577714053170"),
    discord.app_commands.Choice(name="Régime militaire", value="1417252579766829076")
])
@app_commands.choices(gouvernement=[
    discord.app_commands.Choice(name="Régime parlementaire", value="1417254283694313652"),
    discord.app_commands.Choice(name="Régime présidentielle", value="1417254315684528330"),
    discord.app_commands.Choice(name="République parlementaire", value="1417254344180371636"),
    discord.app_commands.Choice(name="République présidentielle", value="1417254681243025428"),
    discord.app_commands.Choice(name="Monarchie parlementaire", value="1417254399004246161"),
    discord.app_commands.Choice(name="Monarchie absolue", value="1417254501110251540"),
    discord.app_commands.Choice(name="Gouvernement directorial", value="1417254550951428147"),
    discord.app_commands.Choice(name="Gouvernement de Transition", value="1417254582156791908"),
    discord.app_commands.Choice(name="Gouvernement populaire", value="1417254615224680508"),
    discord.app_commands.Choice(name="Stratocratie", value="1417254639069560904"),
    discord.app_commands.Choice(name="Aucun gouvernement", value="1417254809253314590")
])
@app_commands.choices(religion=[
    discord.app_commands.Choice(name="Catholicisme", value="1417622211329659010"),
    discord.app_commands.Choice(name="Protestantisme", value="1417622670702280845"),
    discord.app_commands.Choice(name="Orthodoxie", value="1417622925745586206"),
    discord.app_commands.Choice(name="Sunnisme", value="1417623400695988245"),
    discord.app_commands.Choice(name="Chiisme", value="1417624032131682304"),
    discord.app_commands.Choice(name="Judaïsme", value="1417624442905038859"),
    discord.app_commands.Choice(name="Hindouisme", value="1417625845425766562"),
    discord.app_commands.Choice(name="Bouddhisme", value="1417626007770366123"),
    discord.app_commands.Choice(name="Laïcisme", value="1417626204885745805"),
    discord.app_commands.Choice(name="Athéisme", value="1417626362738512022"),
    discord.app_commands.Choice(name="Foi des Sept", value="1419446723310256138"),
])
@app_commands.choices(religion=[
    discord.app_commands.Choice(name="Catholicisme", value="1417622211329659010"),
    discord.app_commands.Choice(name="Protestantisme", value="1417622670702280845"),
    discord.app_commands.Choice(name="Orthodoxie", value="1417622925745586206"),
    discord.app_commands.Choice(name="Sunnisme", value="1417623400695988245"),
    discord.app_commands.Choice(name="Chiisme", value="1417624032131682304"),
    discord.app_commands.Choice(name="Judaïsme", value="1417624442905038859"),
    discord.app_commands.Choice(name="Hindouisme", value="1417625845425766562"),
    discord.app_commands.Choice(name="Bouddhisme", value="1417626007770366123"),
    discord.app_commands.Choice(name="Laïcisme", value="1417626204885745805"),
    discord.app_commands.Choice(name="Athéisme", value="1417626362738512022"),
    discord.app_commands.Choice(name="Foi des Sept", value="1419446723310256138"),
])
async def creer_pays(
    interaction: discord.Interaction, 
    nom: str,
    budget: int,
    pib: int,
    continent: str,
    categorie: discord.CategoryChannel,
    dirigeant: discord.Member,
    drapeau_salon: str = None,
    drapeau_perso: str = None,
    couleur: str = None,
    image: str = None,
    nom_salon_secret: str = None,
    categorie_secret: discord.CategoryChannel = None,
    economie: str = None,
    regime_politique: str = None,
    gouvernement: str = None,
    religion: str = None
):
    """Crée un nouveau pays avec son rôle et son salon."""
    await interaction.response.defer()
    
    # Vérifier que le budget est positif
    ROLE_PAYS_PAR_DEFAUT = 1417253039491776733
    if budget <= 0:
        await interaction.followup.send("> Le budget initial doit être positif.", ephemeral=True)
        return
    
    # Image par défaut ou personnalisée
    pays_image = IMAGE_URL
    if image and is_valid_image_url(image):
        pays_image = image
    
    # Emoji par défaut ou personnalisé
    emoji_pays = drapeau_salon if drapeau_salon else ""
    emoji_message = drapeau_perso if drapeau_perso else "🏛️"
    
    # IDs des rôles à gérer
    # Ajout des rôles économie, régime politique, gouvernement et rôle par défaut
    roles_a_ajouter = [ROLE_PAYS_PAR_DEFAUT]
    if economie:
        roles_a_ajouter.append(int(economie))
    if regime_politique:
        roles_a_ajouter.append(int(regime_politique))
    if gouvernement:
        roles_a_ajouter.append(int(gouvernement))
    # Ajout du rôle de continent
    if continent:
        roles_a_ajouter.append(int(continent))
    # Attribution des rôles au dirigeant
    for role_id in roles_a_ajouter:
        role_obj = interaction.guild.get_role(role_id)
        if role_obj and role_obj not in dirigeant.roles:
            await dirigeant.add_roles(role_obj, reason="Création du pays")
    ROLE_JOUEUR_ID = 1410289640170328244
    ROLE_NON_JOUEUR_ID = 1393344053608710315
    
    # Liste des rôles à ajouter automatiquement
    auto_roles_ids = [
        1413995329656852662,
        1413997188089909398,
        1413993747515052112,
        1413995073632207048,
        1413993786001985567,
        1413994327473918142,
        1413994277029023854,
        1413993819292045315,
        1413994233622302750,
        1413995459827077190,
        ROLE_JOUEUR_ID  # Ajouter le rôle de joueur
    ]
    
    try:
        # Obtenir le rôle de continent pour positionner le nouveau rôle
        continent_role = interaction.guild.get_role(int(continent))
        if not continent_role:
            await interaction.followup.send(f"> Erreur: Rôle de continent introuvable (ID: {continent}).", ephemeral=True)
            return
        print(f"[DEBUG] Rôle continent trouvé : {continent_role.name}")

        # Créer le rôle
        role_name = f"{emoji_pays}・❝ ｢ {nom} ｣ ❞" if emoji_pays else f"❝ ｢ {nom} ｣ ❞"
        role_kwargs = {"name": role_name}
        if couleur:
            try:
                if couleur.startswith('#'):
                    couleur = couleur[1:]
                color_value = int(couleur, 16)
                role_kwargs["color"] = discord.Color(color_value)
            except ValueError:
                pass  # Utiliser la couleur par défaut
        print(f"[DEBUG] Création du rôle pays : {role_name}")
        role = await interaction.guild.create_role(**role_kwargs)
        # Définir l'emoji comme icône du rôle si possible
        if emoji_pays:
            try:
                await role.edit(unicode_emoji=emoji_pays)
                print(f"[DEBUG] Icône du rôle définie sur l'emoji : {emoji_pays}")
            except Exception as e:
                print(f"[ERROR] Impossible de définir l'emoji comme icône de rôle : {e}")
        # Enregistrement du budget dans balances
        print(f"[DEBUG] Enregistrement du budget pour le pays {role.id} : {budget}")
        balances[str(role.id)] = budget
        save_balances(balances)
        
        # Initialisation du PIB
        pib_data = load_pib()
        pib_data[str(role.id)] = {"pib": pib}

        # Positionner le rôle pays juste en dessous du rôle de continent
        try:
            server_roles = await interaction.guild.fetch_roles()
            continent_position = continent_role.position
            positions = {role: continent_position - 1}
            await interaction.guild.edit_role_positions(positions)
        except Exception as e:
            print(f"[ERROR] Positionnement du rôle pays : {e}")

        # Création du salon principal
        formatted_name = convert_to_bold_letters(nom)
        channel_name = f"【{emoji_pays}】・{formatted_name.lower().replace(' ', '-')}" if emoji_pays else f"【】・{formatted_name.lower().replace(' ', '-') }"
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
                read_message_history=True,
                embed_links=True,
                attach_files=True,
                add_reactions=True
            )
        }
        print(f"[DEBUG] Création du salon principal : {channel_name}")
        channel = await interaction.guild.create_text_channel(
            name=channel_name,
            category=categorie,
            overwrites=overwrites
        )
        pays_log_channel_data[str(role.id)] = channel.id
        save_pays_log_channel(pays_log_channel_data)
        print(f"[DEBUG] Salon principal créé : {channel.name}")

        # Ajout des rôles au dirigeant
        try:
            print("[DEBUG] Ajout des rôles au dirigeant...")
            await dirigeant.add_roles(role)
            await dirigeant.add_roles(continent_role)
            # Ajout des rôles de base
            for base_role_id in [1417619445060206682, 1417619843611627530]:
                base_role = interaction.guild.get_role(base_role_id)
                if base_role and base_role not in dirigeant.roles:
                    await dirigeant.add_roles(base_role)
            # Ajout du rôle de religion si précisé
            if religion:
                role_religion = interaction.guild.get_role(int(religion))
                if role_religion and role_religion not in dirigeant.roles:
                    await dirigeant.add_roles(role_religion)
        except Exception as e:
            print(f"[ERROR] Ajout des rôles au dirigeant : {e}")

        # Ajout du rôle joueur et retrait du rôle non-joueur
        await asyncio.sleep(0)
        # Ajout du rôle joueur et retrait du rôle non-joueur
        role_joueur_id = 1410289640170328244
        role_non_joueur_id = 1393344053608710315
        role_joueur = interaction.guild.get_role(role_joueur_id)
        role_non_joueur = interaction.guild.get_role(role_non_joueur_id)
        if role_joueur:
            await dirigeant.add_roles(role_joueur)
        if role_non_joueur and role_non_joueur in dirigeant.roles:
            await dirigeant.remove_roles(role_non_joueur)

        # Ajout des rôles automatiques
        try:
            print("[DEBUG] Ajout des rôles automatiques...")
            for auto_role_id in auto_roles_ids:
                auto_role = interaction.guild.get_role(auto_role_id)
                if auto_role:
                    await dirigeant.add_roles(auto_role)
        except Exception as e:
            print(f"[ERROR] Ajout des rôles automatiques : {e}")

        # Enregistrement de l'image si fournie
        try:
            print("[DEBUG] Enregistrement de l'image du pays...")
            if image and is_valid_image_url(image):
                pays_images[str(role.id)] = image
        except Exception as e:
            print(f"[ERROR] Enregistrement image pays : {e}")

        # Initialisation du PIB (déjà fait)
        try:
            print("[DEBUG] Initialisation du PIB...")
        except Exception as e:
            print(f"[ERROR] Initialisation personnel : {e}")

        # Sauvegarde des données
        try:
            print("[DEBUG] Sauvegarde des données...")
            save_balances(balances)
            save_pib(pib_data)
            save_pays_images(pays_images)
            save_all_json_to_postgres()
        except Exception as e:
            print(f"[ERROR] Sauvegarde des données : {e}")

        # Envoi du message embed de confirmation
        try:
            print("[DEBUG] Envoi du message embed de confirmation...")
            regime_role = interaction.guild.get_role(int(regime_politique)) if regime_politique else None
            gouvernement_role = interaction.guild.get_role(int(gouvernement)) if gouvernement else None
            religion_role = interaction.guild.get_role(int(religion)) if religion else None
            continent_role_obj = interaction.guild.get_role(int(continent)) if continent else None
            drapeau_emoji = drapeau_perso if drapeau_perso else ""
            embed = discord.Embed(
                title="🏛️ | Nouveau pays enregistré",
                description=(
                    "⠀\n"
                    f"> − **Nom du pays :** {nom}\n"
                    f"> − **Budget :** {format_number(budget)}\n"
                    f"> − **PIB :** {format_number(pib)}\n"
                    "> \n"
                    f"> − **Continent :** {continent_role_obj.mention if continent_role_obj else 'Non défini'}\n"
                    f"> − **Régime politique :** {regime_role.mention if regime_role else 'Non défini'}\n"
                    f"> − **Forme de Gouvernement :** {gouvernement_role.mention if gouvernement_role else 'Non défini'}\n"
                    f"> − **Religion d'État :** {religion_role.mention if religion_role else 'Non défini'}\n"
                    "> \n"
                    f"> − **Drapeau personnalisé :** {drapeau_emoji}\n⠀"
                ),
                color=0xebe3bd
            )
            embed.set_image(url=image if image and is_valid_image_url(image) else IMAGE_URL)
            await interaction.followup.send(embed=embed)
            # Envoi du message de bienvenue dans le salon spécifique
            bienvenue_channel_id = 1393945519327281153
            bienvenue_channel = interaction.guild.get_channel(bienvenue_channel_id)
            if bienvenue_channel:
                # Récupération des rôles pour l'affichage
                regime_role = interaction.guild.get_role(int(regime_politique)) if regime_politique else None
                gouvernement_role = interaction.guild.get_role(int(gouvernement)) if gouvernement else None
                religion_role = interaction.guild.get_role(int(religion)) if religion else None
                continent_role = interaction.guild.get_role(int(continent)) if continent else None
                drapeau_emoji = drapeau_perso if drapeau_perso else ""
                bienvenue_embed = discord.Embed(
                    title="🏛️ | Un nouveau Pays fait son apparition",
                    description=(
                        "⠀\n"
                        f"> − **Nom du pays** : {role.mention}\n"
                        f"> − **Gouvernement** : {gouvernement_role.mention if gouvernement_role else 'Non défini'}\n"
                        f"> − **Régime Politique** : {regime_role.mention if regime_role else 'Non défini'}\n"
                        f"> − **Religion** : {religion_role.mention if religion_role else 'Non défini'}\n"
                        f"> − **Continent** : {continent_role.mention if continent_role else 'Non défini'}\n"
                        f"> − **Drapeau personnalisé** : {drapeau_emoji}\n"
                        "> \n"
                        f"> En te souhaitant une belle expérience {dirigeant.mention} sur **PAX RUINAE** !\n⠀"
                    ),
                    color=0x162e50
                )
                bienvenue_embed.set_image(url=image if image and is_valid_image_url(image) else IMAGE_URL)
                await bienvenue_channel.send(embed=bienvenue_embed)
        except Exception as e:
            print(f"[ERROR] Envoi embed confirmation : {e}")
            await interaction.followup.send(f"> Pays créé, mais erreur lors de l'envoi du message : {e}", ephemeral=True)

        # Créer le salon secret si demandé
        if nom_salon_secret and categorie_secret:
            try:
                formatted_secret_name = convert_to_bold_letters(nom_salon_secret)
                secret_channel_name = f"【{emoji_pays}】・{formatted_secret_name.lower().replace(' ', '-')}" if emoji_pays else f"【】・{formatted_secret_name.lower().replace(' ', '-') }"
                secret_overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    role: discord.PermissionOverwrite(
                        read_messages=True,
                        manage_webhooks=True,
                        manage_messages=True
                    )
                }
                secret_channel = await interaction.guild.create_text_channel(
                    name=secret_channel_name,
                    category=categorie_secret,
                    overwrites=secret_overwrites
                )
            except Exception as e:
                print(f"[ERROR] Création salon secret : {e}")
                await interaction.followup.send(f"> Pays créé, mais erreur lors de la création du salon secret : {e}", ephemeral=True)

        # Log de l'action
        modifications = []
        modifications.append("Pays créé")
        modifications.append("Rôle attribué")
        modifications.append("Salon créé")
        modifications.append("Budget initialisé")
        log_embed = discord.Embed(
            title=f"🏛️ | Création de pays",
            description=f"> **Administrateur :** {interaction.user.mention}\n> **Pays créé : ** {role.mention}\n> **Modifications : ** {', '.join(modifications)}{INVISIBLE_CHAR}",
            color=EMBED_COLOR,
            timestamp=datetime.datetime.now()
        )
        await send_log(interaction.guild, embed=log_embed)

        # Log détaillé dans le canal de log des pays
        pays_log_embed = discord.Embed(
            title=f"🏛️ | Nouveau Pays : {nom}",
            description=f"Un nouveau pays a rejoint la scène internationale!",
            color=EMBED_COLOR
        )
        pays_log_embed.add_field(
            name="Informations",
            value=f"> **Nom :** {nom}\n"
                f"> **Continent :** {continent_role.name}\n"
                f"> **Rôle :** {role.mention}\n"
                f"> **Salon :** {channel.mention}\n"
                f"> **PIB :** {format_number(pib)} {MONNAIE_EMOJI}\n"
                f"> **Créé par :** {interaction.user.mention}",
            inline=False
        )
        pays_log_embed.add_field(
            name="Gouvernement",
            value=f"> **Dirigeant :** {dirigeant.mention}\n"
                f"> **Budget alloué :** {format_number(budget)} {MONNAIE_EMOJI}",
            inline=False
        )
        pays_log_embed.add_field(
            name="Message officiel",
            value=f"Nous souhaitons la bienvenue à {dirigeant.mention}, nouveau dirigeant de {role.mention} sur la scène internationale. Nous lui souhaitons succès et prospérité dans la conduite de cette nation!",
            inline=False
        )
        pays_log_embed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else None)
        pays_log_embed.set_image(url=image if image and is_valid_image_url(image) else IMAGE_URL)
        pays_log_embed.set_footer(text=f"Date de création : {datetime.datetime.now().strftime('%d/%m/%Y à %H:%M')}")
        await send_pays_log(interaction.guild, pays_log_embed)

    except Exception as e:
        await interaction.followup.send(f"> Erreur lors de la création du pays : {e}", ephemeral=True)
        print(f"[ERROR] Exception dans creer_pays : {e}")
        return

        # Si un emoji personnalisé est fourni, essayer de l'appliquer comme icône du rôle
        if drapeau_perso:
            try:
                emoji_id = None
                if drapeau_perso.startswith('<') and drapeau_perso.endswith('>'):
                    emoji_parts = drapeau_perso.strip('<>').split(':')
                    if len(emoji_parts) >= 3:
                        emoji_id = int(emoji_parts[2])
                if emoji_id:
                    emoji = await interaction.guild.fetch_emoji(emoji_id)
                    if emoji:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(str(emoji.url)) as resp:
                                if resp.status == 200:
                                    emoji_bytes = await resp.read()
                                    try:
                                        await role.edit(display_icon=emoji_bytes)
                                    except discord.Forbidden:
                                        await interaction.followup.send("> Note: Impossible d'appliquer l'emoji comme icône de rôle. Cette fonctionnalité nécessite des boosts de serveur.", ephemeral=True)
                                    except Exception as e:
                                        print(f"Erreur lors de l'application de l'icône de rôle: {e}")
            except Exception as e:
                print(f"Erreur lors du traitement de l'emoji personnalisé: {e}")

        # Trouver la position correcte pour le nouveau rôle de pays
        try:
            server_roles = await interaction.guild.fetch_roles()
            continent_position = continent_role.position
            positions = {role: continent_position - 1}
            await interaction.guild.edit_role_positions(positions)
            print(f"[DEBUG] Rôle de pays positionné juste en dessous du continent {continent_role.name}")
        except Exception as e:
            print(f"Erreur lors du positionnement du rôle: {e}")

        # Créer le salon principal
        formatted_name = convert_to_bold_letters(nom)
        channel_name = f"【{emoji_pays}】・{formatted_name.lower().replace(' ', '-')}" if emoji_pays else f"【】・{formatted_name.lower().replace(' ', '-') }"
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(
                read_messages=True, send_messages=True, read_message_history=True,
                embed_links=True, attach_files=True, add_reactions=True
            )
        }
        print(f"[DEBUG] Création du salon principal : {channel_name}")
        channel = await interaction.guild.create_text_channel(
            name=channel_name,
            category=categorie,
            overwrites=overwrites
        )
        pays_log_channel_data[str(role.id)] = channel.id
        save_pays_log_channel(pays_log_channel_data)
        print(f"[DEBUG] Salon principal créé : {channel.name}")

        # Ajout des rôles au dirigeant
        try:
            print("[DEBUG] Ajout des rôles au dirigeant...")
            await dirigeant.add_roles(role)
            await dirigeant.add_roles(continent_role)
        except Exception as e:
            print(f"[ERROR] Ajout des rôles au dirigeant : {e}")

        # Ajout du rôle joueur et retrait du rôle non-joueur
        try:
            print("[DEBUG] Ajout du rôle joueur et retrait du rôle non-joueur...")
            role_joueur_id = 1410289640170328244
            role_non_joueur_id = 1393344053608710315
            role_joueur = interaction.guild.get_role(role_joueur_id)
            role_non_joueur = interaction.guild.get_role(role_non_joueur_id)
            if role_joueur:
                await dirigeant.add_roles(role_joueur)
            if role_non_joueur and role_non_joueur in dirigeant.roles:
                await dirigeant.remove_roles(role_non_joueur)
        except Exception as e:
            print(f"[ERROR] Ajout/retrait rôle joueur/non-joueur : {e}")

        # Ajout des rôles automatiques
        try:
            print("[DEBUG] Ajout des rôles automatiques...")
            for auto_role_id in auto_roles_ids:
                auto_role = interaction.guild.get_role(auto_role_id)
                if auto_role:
                    await dirigeant.add_roles(auto_role)
        except Exception as e:
            print(f"[ERROR] Ajout des rôles automatiques : {e}")

        # Enregistrement de l'image si fournie
        try:
            print("[DEBUG] Enregistrement de l'image du pays...")
            if image and is_valid_image_url(image):
                pays_images[str(role.id)] = image
        except Exception as e:
            print(f"[ERROR] Enregistrement image pays : {e}")

        # Initialisation du PIB (déjà fait)
        try:
            print("[DEBUG] Initialisation du PIB...")
        except Exception as e:
            print(f"[ERROR] Initialisation personnel : {e}")

        # Sauvegarde des données
        try:
            print("[DEBUG] Sauvegarde des données...")
            save_balances(balances)
            save_pib(pib_data)
            save_pays_images(pays_images)
            save_all_json_to_postgres()
        except Exception as e:
            print(f"[ERROR] Sauvegarde des données : {e}")

        # Envoi du message embed de confirmation
        try:
            print("[DEBUG] Envoi du message embed de confirmation...")
            embed = discord.Embed(
                title="🏛️ Nouveau pays créé",
                description=f"> **Pays:** {role.mention}\n"
                    f"> **Continent:** {continent_role.mention}\n"
                    f"> **Salon:** {channel.mention}\n"
                    f"> **PIB:** {format_number(pib)} {MONNAIE_EMOJI}\n"
                    f"> **Budget alloué:** {format_number(budget)} {MONNAIE_EMOJI}\n"
                    f"> **Dirigeant:** {dirigeant.mention}{INVISIBLE_CHAR}",
                color=EMBED_COLOR
            )
            embed.set_image(url=image if image and is_valid_image_url(image) else IMAGE_URL)
            await interaction.followup.send(embed=embed)
        except Exception as e:
            print(f"[ERROR] Envoi embed confirmation : {e}")
            await interaction.followup.send(f"> Pays créé, mais erreur lors de l'envoi du message : {e}", ephemeral=True)

    except Exception as e:
        await interaction.followup.send(f"> Erreur lors de la création du pays : {e}", ephemeral=True)
        print(f"[ERROR] Exception dans creer_pays : {e}")
        return

        # Créer le salon secret si un nom est fourni et une catégorie spécifiée
        secret_channel = None
        if nom_salon_secret and categorie_secret:
            formatted_secret_name = convert_to_bold_letters(nom_salon_secret)
            secret_channel_name = f"【{emoji_pays}】・{formatted_secret_name.lower().replace(' ', '-')}" if emoji_pays else f"【】・{formatted_secret_name.lower().replace(' ', '-')}"
            secret_overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                role: discord.PermissionOverwrite(
                    read_messages=True,
                    manage_webhooks=True,
                    manage_messages=True
                )
            }
            secret_channel = await interaction.guild.create_text_channel(
                name=secret_channel_name,
                category=categorie_secret,
                overwrites=secret_overwrites
            )
        
        # Gérer les données du pays
        role_id = str(role.id)
        
        # Attribuer le budget au pays
        balances[role_id] = budget
        
        # ID des rôles spéciaux de joueur et non-joueur
        role_joueur_id = 1410289640170328244
        role_non_joueur_id = 1393344053608710315
        
        # Attribuer les rôles au dirigeant
        await dirigeant.add_roles(role)
        await dirigeant.add_roles(continent_role)
        
        # Ajouter le rôle joueur et retirer le rôle non-joueur
        role_joueur = interaction.guild.get_role(role_joueur_id)
        role_non_joueur = interaction.guild.get_role(role_non_joueur_id)
        
        if role_joueur:
            await dirigeant.add_roles(role_joueur)
        
        if role_non_joueur and role_non_joueur in dirigeant.roles:
            await dirigeant.remove_roles(role_non_joueur)
        
        # Ajouter tous les rôles automatiques
        for auto_role_id in auto_roles_ids:
            auto_role = interaction.guild.get_role(auto_role_id)
            if auto_role:
                await dirigeant.add_roles(auto_role)
        
        # Enregistrer l'image si fournie
        if image and is_valid_image_url(image):
            pays_images[role_id] = image
        
        # Initialiser le PIB
        pib_data[role_id] = {
            "pib": pib
        }
        
        # Sauvegarder toutes les données
        save_balances(balances)
        save_pib(pib_data)
        save_pays_images(pays_images)
        save_all_json_to_postgres()
        
        # Embed de confirmation
        embed = discord.Embed(
            title="🏛️ Nouveau pays créé",
            description=f"> **Pays:** {role.mention}\n"
                f"> **Continent:** {continent_role.mention}\n"
                f"> **Salon:** {channel.mention}\n"
                f"> **PIB:** {format_number(pib)} {MONNAIE_EMOJI}\n"
                f"> **Budget alloué:** {format_number(budget)} {MONNAIE_EMOJI}\n"
                f"> **Dirigeant:** {dirigeant.mention}{INVISIBLE_CHAR}",
            color=EMBED_COLOR
        )
        embed.set_image(url=pays_image)
        await interaction.followup.send(embed=embed)
    
        # Message de bienvenue
        welcome_embed = discord.Embed(
            title=f"{emoji_message} | Bienvenue dans votre pays !",
            description=f"> *Ce salon est réservé aux membres du pays {role.mention}*\n"
                       f"> \n" 
                       f"> PIB : {format_number(pib)} {MONNAIE_EMOJI}\n"
                       f"> Budget alloué : {format_number(budget)} {MONNAIE_EMOJI}\n"
                       f"> Dirigeant : {dirigeant.mention}\n"
                       f"> \n"
                       f"> :black_small_square: Nous vous souhaitons une agréable expérience au sein du Rôleplay !{INVISIBLE_CHAR}",
            color=EMBED_COLOR
        )
        welcome_embed.set_image(url=pays_image)
        await channel.send(embed=welcome_embed)
    
        # Log de l'action
        log_embed = discord.Embed(
            title=f"🏛️ | Création de pays",
            description=f"> **Administrateur :** {interaction.user.mention}\n"
                       f"> **Pays créé : ** {role.mention}\n"
                       f"> **Continent : ** {continent_role.mention}\n"
                       f"> **PIB : ** {format_number(pib)} {MONNAIE_EMOJI}\n"
                       f"> **Dirigeant désigné : ** {dirigeant.mention}\n"
                       f"> **Budget alloué : ** {format_number(budget)} {MONNAIE_EMOJI}"
                       f"{INVISIBLE_CHAR}",
            color=EMBED_COLOR,
            timestamp=datetime.datetime.now()
        )
        await send_log(interaction.guild, embed=log_embed)
    
        # Envoyer un log détaillé dans le canal de log des pays
        pays_log_embed = discord.Embed(
            title=f"🏛️ | Nouveau Pays : {nom}",
            description=f"Un nouveau pays a rejoint la scène internationale!",
            color=EMBED_COLOR
        )
        pays_log_embed.add_field(
            name="Informations",
            value=f"> **Nom :** {nom}\n"
                f"> **Continent :** {continent_role.name}\n"
                f"> **Rôle :** {role.mention}\n"
                f"> **Salon :** {channel.mention}\n"
                f"> **PIB :** {format_number(pib)} {MONNAIE_EMOJI}\n"
                f"> **Créé par :** {interaction.user.mention}",
            inline=False
        )
    
        pays_log_embed.add_field(
            name="Gouvernement",
            value=f"> **Dirigeant :** {dirigeant.mention}\n"
                f"> **Budget alloué :** {format_number(budget)} {MONNAIE_EMOJI}",
            inline=False
        )
    
        pays_log_embed.add_field(
            name="Message officiel",
            value=f"Nous souhaitons la bienvenue à {dirigeant.mention}, nouveau dirigeant de {role.mention} sur la scène internationale. Nous lui souhaitons succès et prospérité dans la conduite de cette nation!",
            inline=False
        )
    
        pays_log_embed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else None)
        pays_log_embed.set_image(url=pays_image)
        pays_log_embed.set_footer(text=f"Date de création : {datetime.datetime.now().strftime('%d/%m/%Y à %H:%M')}")
        
        await send_pays_log(interaction.guild, pays_log_embed)
        
    except Exception as e:
        await interaction.followup.send(f"> Erreur inattendue ou blocage lors de la création du pays : {e}", ephemeral=True)

# Ajouter une commande pour modifier l'image d'un pays
@bot.tree.command(name="modifier_image_pays", description="Modifie l'image d'un pays")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(
    role="Rôle du pays dont vous voulez modifier l'image",
    image="URL de la nouvelle image du pays"
)
async def modifier_image_pays(
    interaction: discord.Interaction,
    role: discord.Role,
    image: str
):
    """Modifie l'image d'un pays."""
    await interaction.response.defer(ephemeral=True)
    
    # Vérifier que le rôle est bien un pays
    role_id = str(role.id)
    if role_id not in balances:
        await interaction.followup.send("> Ce rôle ne semble pas être un pays.", ephemeral=True)
        return
    
    # Vérifier l'URL de l'image
    if not is_valid_image_url(image):
        await interaction.followup.send("> URL d'image invalide. Veuillez fournir une URL directe vers une image (JPG, PNG, etc.)", ephemeral=True)
        return
    
    # Enregistrer la nouvelle image
    pays_images[role_id] = image
    save_pays_images(pays_images)
    save_all_json_to_postgres()
    
    # Confirmation
    embed = discord.Embed(
        description=f"> L'image du pays {role.mention} a été mise à jour.{INVISIBLE_CHAR}",
        color=EMBED_COLOR
    )
    embed.set_image(url=image)
    await interaction.followup.send(embed=embed)
    
    # Log de l'action
    log_embed = discord.Embed(
        title="🏛️ | Modification d'image de pays",
        description=f"> **Administrateur :** {interaction.user.mention}\n"
                   f"> **Pays modifié :** {role.mention}{INVISIBLE_CHAR}",
        color=EMBED_COLOR,
        timestamp=datetime.datetime.now()
    )
    log_embed.set_image(url=image)
    await send_log(interaction.guild, embed=log_embed)

# Ajouter la commande pour définir le canal de log des pays
@bot.tree.command(name="setlogpays", description="Définit le salon de logs pour les pays")
@app_commands.checks.has_permissions(administrator=True)
async def setlogpays(interaction: discord.Interaction, channel: discord.TextChannel):
    pays_log_channel_data[str(interaction.guild.id)] = channel.id
    save_pays_log_channel(pays_log_channel_data)
    embed = discord.Embed(
        description=f"> Salon de logs pour les pays défini sur {channel.mention}.{INVISIBLE_CHAR}",
        color=EMBED_COLOR
    )
    embed.set_image(url=IMAGE_URL)
    await interaction.response.send_message(embed=embed, ephemeral=True)


# Commande ranking simplifiée : affiche seulement l'argent total en circulation

# Commande classement : affiche le classement des membres par argent
@bot.tree.command(name="classement_eco", description="Affiche le classement des membres par argent")
async def classement_eco(interaction: discord.Interaction):

    classement = sorted(balances.items(), key=lambda x: x[1], reverse=True)
    per_page = 15
    pages = [classement[i:i+per_page] for i in range(0, len(classement), per_page)]
    def make_embed(page_idx):
        page = pages[page_idx]
        desc = "⠀\n"
        for idx, (role_id, amount) in enumerate(page):
            rank = idx + 1 + page_idx * per_page
            if rank == 1:
                medal = "🥇"
            elif rank == 2:
                medal = "🥈"
            elif rank == 3:
                medal = "🥉"
            else:
                medal = f"{rank}."
            role = interaction.guild.get_role(int(role_id))
            if role:
                desc += f"{medal} {role.mention} — {format_number(amount)} <:PX_MDollars:1417605571019804733>\n"
        embed = discord.Embed(
            title="Classement des budgets par pays",
            description=desc,
            color=EMBED_COLOR
        )
        embed.set_image(url=IMAGE_URL)
        embed.set_footer(text=f"Page {page_idx+1}/{len(pages)}")
        return embed

    if not classement:
        await interaction.response.send_message("Aucun membre n'a d'argent enregistré.", ephemeral=True)
        return

    class ClassementView(discord.ui.View):
        def __init__(self, pages):
            super().__init__(timeout=600)
            self.pages = pages
            self.page_idx = 0
            self.message = None

        @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.secondary)
        async def prev(self, interaction_btn: discord.Interaction, button: discord.ui.Button):
            if self.page_idx > 0:
                self.page_idx -= 1
                await interaction_btn.response.edit_message(embed=make_embed(self.page_idx), view=self)

        @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.secondary)
        async def next(self, interaction_btn: discord.Interaction, button: discord.ui.Button):
            if self.page_idx < len(self.pages) - 1:
                self.page_idx += 1
                await interaction_btn.response.edit_message(embed=make_embed(self.page_idx), view=self)

    view = ClassementView(pages)
    await interaction.response.send_message(embed=make_embed(0), view=view)


# Commande /payer : la cible est un rôle (pays) obligatoire, si rien n'est précisé l'argent est détruit (bot), et on ne save pas dans ce cas
@bot.tree.command(name="payer", description="Payer un autre pays ou détruire de l'argent de son pays")
@app_commands.describe(
    cible="Le rôle (pays) à payer. Si rien n'est sélectionné, l'argent est payé au bot.",
    montant="Montant à payer"
)
@app_commands.choices()
async def payer(interaction: discord.Interaction, montant: int, cible: typing.Optional[discord.Role] = None):
    # Cherche le premier rôle pays du membre qui a de l'argent
    user_roles = [r for r in interaction.user.roles if str(r.id) in balances and balances[str(r.id)] > 0]
    if not user_roles:
        await interaction.response.send_message(
            "> Vous n'avez aucun rôle pays avec de l'argent pour payer.", ephemeral=True)
        return
    pays_role = user_roles[0]
    pays_id = str(pays_role.id)
    solde = balances.get(pays_id, 0)
    if montant <= 0:
        await interaction.response.send_message(
            "> Le montant doit être positif.", ephemeral=True)
        return
    if montant > solde:
        await interaction.response.send_message(
            "> Votre pays n'a pas assez d'argent pour payer.", ephemeral=True)
        return
    if cible:
        cible_id = str(cible.id)
        balances[pays_id] -= montant
        balances[cible_id] = balances.get(cible_id, 0) + montant
        print("[DEBUG] Sauvegarde balances.json après paiement...")
        save_balances(balances)
        print("[DEBUG] Sauvegarde PostgreSQL après paiement...")
        save_all_json_to_postgres()
        embed = discord.Embed(
            description=f"> {format_number(montant)} {MONNAIE_EMOJI} payés de {pays_role.mention} à {cible.mention}.{INVISIBLE_CHAR}",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        # Paiement au bot : l'argent est détruit, on ne save pas balances
        balances[pays_id] -= montant
        print("[DEBUG] Sauvegarde balances.json après destruction d'argent...")
        save_balances(balances)
        print("[DEBUG] Sauvegarde PostgreSQL après destruction d'argent...")
        save_all_json_to_postgres()
        embed = discord.Embed(
            description=f"> {format_number(montant)} {MONNAIE_EMOJI} ont été retirés de la circulation depuis {pays_role.mention}.{INVISIBLE_CHAR}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

# Commande pour reset l'économie
@bot.tree.command(name="reset_economie", description="Réinitialise toute l'économie et supprime l'argent en circulation (admin seulement)")
@app_commands.checks.has_permissions(administrator=True)
async def reset_economie(interaction: discord.Interaction):
    """Réinitialise l'économie : vide tous les fichiers de données économiques."""
    await interaction.response.defer(ephemeral=True)
    confirm_view = discord.ui.View()
    confirm_button = discord.ui.Button(label="Confirmer la réinitialisation", style=discord.ButtonStyle.danger)
    cancel_button = discord.ui.Button(label="Annuler", style=discord.ButtonStyle.secondary)
    confirm_view.add_item(confirm_button)
    confirm_view.add_item(cancel_button)

    async def confirm_callback(interaction2: discord.Interaction):
        if interaction2.user.id != interaction.user.id:
            await interaction2.response.send_message("Vous n'êtes pas autorisé à confirmer cette action.", ephemeral=True)
            return
        # Vider les variables en mémoire
        global balances, loans
        balances.clear()
        loans.clear()
        # personnel supprimé
        # Sauvegarder les fichiers vides
        for file_path, empty_value in [
            (BALANCE_FILE, {}),
            (BALANCE_BACKUP_FILE, {}),
            (LOANS_FILE, []),
            (PIB_FILE, {}),
            (TRANSACTION_LOG_FILE, []),
        ]:
            try:
                with open(file_path, "w") as f:
                    json.dump(empty_value, f)
            except Exception as e:
                await interaction2.response.send_message(f"Erreur lors de la suppression de {os.path.basename(file_path)} : {e}", ephemeral=True)
                return
        # Supprimer les données économiques dans PostgreSQL
        import psycopg2, os
        DATABASE_URL = os.getenv("DATABASE_URL")
        if DATABASE_URL:
            try:
                with psycopg2.connect(DATABASE_URL) as conn:
                    with conn.cursor() as cur:
                        for filename in ["balances.json", "balances_backup.json", "loans.json", "transactions.json", "personnel.json"]:
                            cur.execute("DELETE FROM json_backups WHERE filename = %s", (filename,))
                    conn.commit()
                print("[DEBUG] Données économiques supprimées de PostgreSQL.")
            except Exception as e:
                print(f"[DEBUG] Erreur lors de la suppression des données économiques dans PostgreSQL : {e}")
        await interaction2.response.edit_message(content="✅ Économie réinitialisée avec succès !", view=None)

    async def cancel_callback(interaction2: discord.Interaction):
        if interaction2.user.id != interaction.user.id:
            await interaction2.response.send_message("Vous n'êtes pas autorisé à annuler cette action.", ephemeral=True)
            return
        await interaction2.response.edit_message(content="❌ Réinitialisation annulée.", view=None)

    confirm_button.callback = confirm_callback
    cancel_button.callback = cancel_callback

    await interaction.followup.send(
        "⚠️ Cette action va supprimer toutes les données économiques (balances, prêts, transactions). Confirmez-vous ?",
        view=confirm_view,
        ephemeral=True
    )


# Commande /balance : voir l'argent de son pays ou d'un autre (optionnel)
@bot.tree.command(name="balance", description="Affiche l'argent de votre pays ou d'un autre rôle (optionnel)")
@app_commands.describe(role="Le rôle (pays) dont vous voulez voir l'argent (optionnel)")
async def balance(interaction: discord.Interaction, role: discord.Role = None):
    # Si aucun rôle n'est précisé, on cherche le premier rôle du membre qui a de l'argent
    if role is None:
        user_roles = [r for r in interaction.user.roles if str(r.id) in balances and balances[str(r.id)] > 0]
        if not user_roles:
            await interaction.response.send_message(
                "> Vous n'avez aucun rôle pays avec de l'argent. Précisez un rôle pour voir sa balance.", ephemeral=True)
            return
        role = user_roles[0]
    # Vérifie que l'utilisateur a bien ce rôle ou est admin
    if role not in interaction.user.roles and not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "> Vous n'avez pas ce rôle, vous ne pouvez pas voir la balance de ce pays.", ephemeral=True)
        return
    role_id = str(role.id)
    montant = balances.get(role_id, 0)
    print(f"[DEBUG] Balance pour role_id {role_id}: {montant}")
    
    # Récupérer le PIB depuis pib.json
    pib_data = load_pib()
    pib = pib_data.get(role_id, {}).get("pib", None)
    print(f"[DEBUG] PIB pour role_id {role_id}: {pib}")
    print(f"[DEBUG] PIB data complet: {pib_data}")
    # Calcul de la dette totale (somme des emprunts avec taux)
    dette_totale = 0
    emprunts_trouves = []
    
    print(f"[DEBUG] Recherche d'emprunts pour role_id: {role_id}")
    print(f"[DEBUG] Total emprunts dans la base: {len(loans)}")
    print(f"[DEBUG] Tous les emprunts: {loans}")
    
    # Récupérer tous les membres ayant ce rôle pour identifier les citoyens
    citoyens_ids = []
    for member in interaction.guild.members:
        if any(str(member_role.id) == role_id for member_role in member.roles):
            citoyens_ids.append(str(member.id))
    
    print(f"[DEBUG] Citoyens du pays {role.name} (role_id: {role_id}): {citoyens_ids}")
    
    for i, emprunt in enumerate(loans):
        # Vérifier si l'emprunt concerne ce rôle/pays
        emprunt_role_id = emprunt.get("role_id")
        emprunt_demandeur_id = emprunt.get("demandeur_id")
        
        print(f"[DEBUG] Emprunt {i}: role_id={emprunt_role_id}, demandeur_id={emprunt_demandeur_id}")
        
        # Cas 1: Emprunt fait par le pays lui-même
        if emprunt_role_id == role_id:
            principal = emprunt.get("somme", 0)
            taux = emprunt.get("taux", 0)
            dette_emprunt = int(principal * (1 + taux / 100))
            dette_totale += dette_emprunt
            emprunts_trouves.append({
                "type": "pays",
                "principal": principal,
                "taux": taux,
                "dette": dette_emprunt
            })
            print(f"[DEBUG] ✅ Emprunt du pays trouvé: principal={principal}, taux={taux}, dette={dette_emprunt}")
        
        # Cas 2: Emprunt fait par un citoyen auprès de la Banque centrale
        elif emprunt_role_id is None and emprunt_demandeur_id in citoyens_ids:
            principal = emprunt.get("somme", 0)
            taux = emprunt.get("taux", 0)
            dette_emprunt = int(principal * (1 + taux / 100))
            dette_totale += dette_emprunt
            emprunts_trouves.append({
                "type": "citoyen_banque_centrale",
                "demandeur": emprunt_demandeur_id,
                "principal": principal,
                "taux": taux,
                "dette": dette_emprunt
            })
            print(f"[DEBUG] ✅ Emprunt citoyen Banque centrale trouvé: demandeur={emprunt_demandeur_id}, principal={principal}, taux={taux}, dette={dette_emprunt}")
    
    print(f"[DEBUG] Dette totale calculée pour {role_id}: {dette_totale}")
    print(f"[DEBUG] PIB pour {role_id}: {pib}")
    print(f"[DEBUG] Nombre d'emprunts trouvés: {len(emprunts_trouves)}")
    
    # Pourcentage dette/PIB
    pourcentage_pib = 0
    if pib and pib > 0 and dette_totale > 0:
        pourcentage_pib = round((dette_totale / pib) * 100, 2)
        print(f"[DEBUG] Calcul pourcentage: {dette_totale} / {pib} * 100 = {pourcentage_pib}%")
    else:
        print(f"[DEBUG] Pas de calcul de pourcentage: pib={pib}, dette_totale={dette_totale}")
    # Texte formaté
    texte = (
        "⠀\n"
        "> <:PX_MDollars:1417605571019804733> | **Budget :** {}\n"
        "> <:PX_MDollars:1417605571019804733> | **PIB :** {}\n"
        "> <:PX_MDollars:1417605571019804733> | **Dette total :** {} - ({}% au PIB)\n⠀"
    ).format(
        format_number(montant),
        format_number(pib) if pib is not None else "Non défini",
        format_number(dette_totale),
        pourcentage_pib
    )
    embed = discord.Embed(
        description=texte,
        color=0xebe3bd
    )
    embed.set_image(url="https://zupimages.net/up/21/03/vl8j.png")
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Commande pour ajouter de l'argent à un rôle
@bot.tree.command(name="add_argent", description="Ajoute de l'argent à un rôle (admin seulement)")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(role="Le rôle (pays) à créditer", montant="Montant à ajouter")
async def add_argent(interaction: discord.Interaction, role: discord.Role, montant: int):
    if montant <= 0:
        await interaction.response.send_message("> Le montant doit être positif.", ephemeral=True)
        return
    role_id = str(role.id)
    balances[role_id] = balances.get(role_id, 0) + montant
    print("[DEBUG] Sauvegarde balances.json après ajout d'argent...")
    save_balances(balances)
    print("[DEBUG] Sauvegarde PostgreSQL après ajout d'argent...")
    save_all_json_to_postgres()
    embed = discord.Embed(
        description=f"> {format_number(montant)} {MONNAIE_EMOJI} ajoutés à {role.mention}. Nouveau solde : {format_number(balances[role_id])} {MONNAIE_EMOJI}.{INVISIBLE_CHAR}",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Commande pour retirer de l'argent à un rôle (utilisable uniquement par les membres du rôle)
@bot.tree.command(name="remove_argent", description="Retire de l'argent à un rôle (utilisable uniquement par les membres du rôle)")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(role="Le rôle (pays) à débiter", montant="Montant à retirer")
async def remove_argent(interaction: discord.Interaction, role: discord.Role, montant: int):
    if montant <= 0:
        await interaction.response.send_message("> Le montant doit être positif.", ephemeral=True)
        return
    
    role_id = str(role.id)
    solde = balances.get(role_id, 0)
    if montant > solde:
        await interaction.response.send_message("> Le rôle n'a pas assez d'argent.", ephemeral=True)
        return
    
    # Vérification et retrait du montant
    nouveau_solde = solde - montant
    balances[role_id] = nouveau_solde
    print("[DEBUG] Sauvegarde balances.json après retrait d'argent...")
    save_balances(balances)
    print("[DEBUG] Sauvegarde PostgreSQL après retrait d'argent...")
    save_all_json_to_postgres()
    embed = discord.Embed(
        description=f"> {format_number(montant)} {MONNAIE_EMOJI} retirés à {role.mention}. Nouveau solde : {format_number(nouveau_solde)} {MONNAIE_EMOJI}.{INVISIBLE_CHAR}",
        color=discord.Color.red()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="supprimer_pays", description="Supprime un pays, son rôle et son salon")
@app_commands.checks.has_permissions(administrator=True)
async def supprimer_pays(interaction: discord.Interaction, pays: discord.Role, raison: str = None):
    """Supprime un pays, son rôle et son salon."""
    # Suppression des transactions liées au pays
    try:
        import os, json
        DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        transactions_path = os.path.join(DATA_DIR, "transactions.json")
        with open(transactions_path, "r") as f:
            transactions = json.load(f)
        # Filtrer toutes les transactions où le pays supprimé n'est ni source ni destination
        transactions = [t for t in transactions if str(pays.id) not in (str(t.get("source")), str(t.get("destination")))]
        with open(transactions_path, "w") as f:
            json.dump(transactions, f)
        # Mettre à jour le backup PostgreSQL
        try:
            import psycopg2, os
            DATABASE_URL = os.getenv("DATABASE_URL")
            if DATABASE_URL:
                with psycopg2.connect(DATABASE_URL) as conn:
                    with conn.cursor() as cur:
                        cur.execute("DELETE FROM json_backups WHERE filename = %s", ("transactions.json",))
                        with open(transactions_path, "r") as f:
                            content = f.read()
                        cur.execute("""
                            INSERT INTO json_backups (filename, content, updated_at)
                            VALUES (%s, %s, NOW())
                            ON CONFLICT (filename) DO UPDATE SET content = EXCLUDED.content, updated_at = NOW()
                        """, ("transactions.json", content))
                    conn.commit()
                print("[DEBUG] Données économiques supprimées de PostgreSQL.")
        except Exception as e:
            print(f"[DEBUG] Erreur lors de la suppression des données économiques dans PostgreSQL : {e}")
    except Exception as e:
        print(f"[ERROR] Suppression des transactions liées au pays : {e}")
    await interaction.response.defer(ephemeral=True)
    try:
        # Liste des rôles à retirer aux membres du pays
        roles_a_retirer = [
            1413995329656852662, 1413995459827077190, 1413993747515052112, 1413995073632207048,
            1417253039491776733, 1413993786001985567, 1413994327473918142, 1413994277029023854,
            1413993819292045315, 1413994233622302750, 1410289640170328244, 1413997188089909398
        ]
        # Rôles de continent
        roles_continents = [1413995502785138799, 1413995608922128394, 1413995735732457473, 1413995874304004157, 1413996176956461086]
        # Retirer tous les rôles listés + rôles de continent + rôle du pays
        # Tous les IDs possibles pour economie, regime, gouvernement
        roles_economie = [1417234199353622569, 1417234220115431434, 1417234887508754584, 1417234944832442621, 1417234931146555433, 1417235038168289290, 1417235052814794853]
        roles_regime = [1417251476782448843, 1417251480573968525, 1417251556776218654, 1417251565068226691, 1417251568327200828, 1417251571661537320, 1417251574568456232, 1417251577714053170, 1417252579766829076]
        roles_gouv = [1417254283694313652, 1417254315684528330, 1417254344180371636, 1417254681243025428, 1417254399004246161, 1417254501110251540, 1417254550951428147, 1417254582156791908, 1417254615224680508, 1417254639069560904, 1417254809253314590]
        for membre in pays.members:
            # Retirer tous les rôles à retirer
            for role_id in roles_a_retirer + roles_continents + [pays.id]:
                role_obj = interaction.guild.get_role(role_id)
                if role_obj and role_obj in membre.roles:
                    await membre.remove_roles(role_obj)
            # Retirer tous les rôles economie, regime, gouvernement
            for role_id in roles_economie + roles_regime + roles_gouv:
                role_selected = interaction.guild.get_role(role_id)
                if role_selected and role_selected in membre.roles:
                    await membre.remove_roles(role_selected)
            # Retirer le rôle de religion
                roles_religion = [
                    1417622211329659010, 1417622670702280845, 1417622925745586206,
                    1417623400695988245, 1417624032131682304, 1417624442905038859,
                    1417625845425766562, 1417626007770366123, 1417626204885745805,
                    1417626362738512022,
                    1419446723310256138  # Ajout du rôle de religion à supprimer
                ]
            for role_id in roles_religion:
                role_religion = interaction.guild.get_role(role_id)
                if role_religion and role_religion in membre.roles:
                    await membre.remove_roles(role_religion)
            # Retirer les rôles de base
            for base_role_id in [1417619445060206682, 1417619843611627530]:
                base_role = interaction.guild.get_role(base_role_id)
                if base_role and base_role in membre.roles:
                    await membre.remove_roles(base_role)
            # Ajouter le rôle 1393344053608710315
            role_ajouter = interaction.guild.get_role(1393344053608710315)
            if role_ajouter and role_ajouter not in membre.roles:
                await membre.add_roles(role_ajouter)
        # Supprimer le salon du pays via l'ID associé au rôle (stocké dans pays_log_channel_data)
        salons_supprimes = []
        # Suppression par ID (stocké lors de creer_pays)
        salon_id = pays_log_channel_data.get(str(pays.id))
        salon_trouve = None
        if salon_id:
            salon = interaction.guild.get_channel(int(salon_id))
            if salon:
                salon_trouve = salon
        # Si pas trouvé par ID, recherche par nom EXACT généré comme dans creer_pays
        if not salon_trouve:
            # Récupérer l'emoji utilisé dans le nom du salon (si possible)
            emoji_pays = ""
            # On tente de récupérer l'emoji du nom du rôle (si présent)
            if pays.name.startswith("【") and "】" in pays.name:
                emoji_pays = pays.name.split("【")[1].split("】")[0]
            # Récupérer le nom du pays sans emoji ni décorations
            nom_pays_brut = pays.name
            if "】・" in nom_pays_brut:
                nom_pays_brut = nom_pays_brut.split("】・", 1)[1]
            # Reconstruire le nom du salon
            formatted_name = nom_pays_brut
            channel_name = f"【{emoji_pays}】・{formatted_name}".lower().replace(" ", "-")
            for channel in interaction.guild.text_channels:
                if channel.name == channel_name:
                    salon_trouve = channel
                    break
        # Suppression du salon trouvé (uniquement si trouvé par ID ou nom exact)
        if salon_trouve:
            try:
                await salon_trouve.delete(reason=f"Suppression du pays {pays.name}")
                salons_supprimes.append(salon_trouve.name)
            except Exception:
                pass
        # Nettoyage de l'association
        pays_log_channel_data.pop(str(pays.id), None)
        save_pays_log_channel(pays_log_channel_data)
        # Suppression de l'argent associé au rôle du pays
        if str(pays.id) in balances:
            balances.pop(str(pays.id))
            save_balances(balances)
            
        # Suppression du PIB associé au rôle du pays
        pib_data = load_pib()
        if str(pays.id) in pib_data:
            pib_data.pop(str(pays.id))
            save_pib(pib_data)
            
            # Suppression dans PostgreSQL
            try:
                import psycopg2, os
                DATABASE_URL = os.getenv("DATABASE_URL")
                if DATABASE_URL:
                    with psycopg2.connect(DATABASE_URL) as conn:
                        with conn.cursor() as cur:
                            cur.execute("DELETE FROM json_backups WHERE filename = %s", ("balances.json",))
                            # Réenregistrer balances.json sans le pays supprimé
                            import json
                            DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
                            balances_path = os.path.join(DATA_DIR, "balances.json")
                            with open(balances_path, "w") as f:
                                json.dump(balances, f)
                            with open(balances_path, "r") as f:
                                content = f.read()
                            cur.execute("""
                                INSERT INTO json_backups (filename, content, updated_at)
                                VALUES (%s, %s, NOW())
                                ON CONFLICT (filename) DO UPDATE SET content = EXCLUDED.content, updated_at = NOW()
                            """, ("balances.json", content))
                        conn.commit()
            except Exception as err:
                print(f"[ERROR] Suppression balance pays dans PostgreSQL : {err}")
        # Supprimer le rôle du pays
        await pays.delete(reason=raison or "Suppression du pays")
        # Réponse à l'utilisateur
        embed = discord.Embed(
            title="Pays supprimé",
            description=f"> Le pays {pays.name} et son salon associé ont été supprimés.\n> Salon supprimé : {', '.join(salons_supprimes) if salons_supprimes else 'Aucun'}",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"> Erreur lors de la suppression du pays : {e}", ephemeral=True)

@bot.tree.command(name="modifier_pays", description="Modifie les informations d'un pays existant")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(
    role="Rôle du pays à modifier",
    nom="Nouveau nom pour le pays (facultatif)",
    nouveau_dirigeant="Nouveau dirigeant du pays (facultatif)",
    economie="Type d'économie du pays (facultatif)",
    regime_politique="Régime politique du pays (facultatif)",
    gouvernement="Forme de gouvernement du pays (facultatif)"
)
@app_commands.choices(economie=[
    discord.app_commands.Choice(name="Économie ultra-libérale", value="1417234199353622569"),
    discord.app_commands.Choice(name="Économie libérale", value="1417234220115431434"),
    discord.app_commands.Choice(name="Économie mixte", value="1417234887508754584"),
    discord.app_commands.Choice(name="Socialisme de marché", value="1417234944832442621"),
    discord.app_commands.Choice(name="Économie planifiée", value="1417234931146555433"),
    discord.app_commands.Choice(name="Économie dirigiste", value="1417235038168289290"),
    discord.app_commands.Choice(name="Économie corporatiste", value="1417235052814794853")
])
@app_commands.choices(regime_politique=[
    discord.app_commands.Choice(name="Démocratie", value="1417251476782448843"),
    discord.app_commands.Choice(name="Autoritarisme", value="1417251480573968525"),
    discord.app_commands.Choice(name="Totalitarisme", value="1417251556776218654"),
    discord.app_commands.Choice(name="Monarchie", value="1417251565068226691"),
    discord.app_commands.Choice(name="Oligarchie", value="1417251568327200828"),
    discord.app_commands.Choice(name="Théocratie", value="1417251571661537320"),
    discord.app_commands.Choice(name="Technocratie", value="1417251574568456232"),
    discord.app_commands.Choice(name="Régime populaire", value="1417251577714053170"),
    discord.app_commands.Choice(name="Régime militaire", value="1417252579766829076")
])
@app_commands.choices(gouvernement=[
    discord.app_commands.Choice(name="Régime parlementaire", value="1417254283694313652"),
    discord.app_commands.Choice(name="Régime présidentielle", value="1417254315684528330"),
    discord.app_commands.Choice(name="République parlementaire", value="1417254344180371636"),
    discord.app_commands.Choice(name="République présidentielle", value="1417254681243025428"),
    discord.app_commands.Choice(name="Monarchie parlementaire", value="1417254399004246161"),
    discord.app_commands.Choice(name="Monarchie absolue", value="1417254501110251540"),
    discord.app_commands.Choice(name="Gouvernement directorial", value="1417254550951428147"),
    discord.app_commands.Choice(name="Gouvernement de Transition", value="1417254582156791908"),
    discord.app_commands.Choice(name="Gouvernement populaire", value="1417254615224680508"),
    discord.app_commands.Choice(name="Stratocratie", value="1417254639069560904"),
    discord.app_commands.Choice(name="Aucun gouvernement", value="1417254809253314590")
])
async def modifier_pays(
    interaction: discord.Interaction,
    role: discord.Role,
    nom: str = None,
    nouveau_dirigeant: discord.Member = None,
    economie: str = None,
    regime_politique: str = None,
    gouvernement: str = None,
    religion: str = None
):
    """Modifie le nom et/ou le dirigeant d'un pays existant."""
    await interaction.response.defer()
    modifications = []
    try:
        # Changement de nom du pays
        if nom:
            old_role_name = role.name
            role_name = f"❝ ｢ {nom} ｣ ❞"
            await role.edit(name=role_name)
            modifications.append("nom du rôle")
            # Renommer le salon principal si trouvé
            for channel in interaction.guild.text_channels:
                if channel.permissions_for(role).read_messages and not channel.permissions_for(interaction.guild.default_role).read_messages:
                    formatted_name = convert_to_bold_letters(nom)
                    channel_name = f"【】・{formatted_name.lower().replace(' ', '-')}"
                    await channel.edit(name=channel_name)
                    modifications.append("nom du salon")
                    break
        # Changement de dirigeant
        if nouveau_dirigeant:
            ancien_dirigeant = None
            for membre in role.members:
                # Ajout des rôles de base
                for base_role_id in [1417619445060206682, 1417619843611627530]:
                    base_role = interaction.guild.get_role(base_role_id)
                    if base_role and base_role not in membre.roles:
                        await membre.add_roles(base_role)
                if religion:
                    role_religion = interaction.guild.get_role(int(religion))
                    if role_religion:
                        await membre.add_roles(role_religion)
                    if membre != nouveau_dirigeant:
                        ancien_dirigeant = membre
                        # break  # Removed invalid break statement
            auto_roles_ids = [
                1413995329656852662, 1413997188089909398, 1413993747515052112, 1413995073632207048,
                1413993786001985567, 1413994327473918142, 1413994277029023854, 1413993819292045315,
                1413994233622302750, 1413995459827077190, 1410289640170328244
            ]
            if ancien_dirigeant:
                await ancien_dirigeant.remove_roles(role)
                for auto_role_id in auto_roles_ids:
                    auto_role = interaction.guild.get_role(auto_role_id)
                    if auto_role and auto_role in ancien_dirigeant.roles:
                        await ancien_dirigeant.remove_roles(auto_role)
            await nouveau_dirigeant.add_roles(role)
            for auto_role_id in auto_roles_ids:
                auto_role = interaction.guild.get_role(auto_role_id)
                if auto_role and auto_role not in nouveau_dirigeant.roles:
                    await nouveau_dirigeant.add_roles(auto_role)
            modifications.append("dirigeant remplacé")
        # Modification des rôles économie, régime politique, gouvernement
        ROLE_PAYS_PAR_DEFAUT = 1417253039491776733
        roles_economie = [1417234199353622569, 1417234220115431434, 1417234887508754584, 1417234944832442621, 1417234931146555433, 1417235038168289290, 1417235052814794853]
        roles_regime = [1417251476782448843, 1417251480573968525, 1417251556776218654, 1417251565068226691, 1417251568327200828, 1417251571661537320, 1417251574568456232, 1417251577714053170, 1417252579766829076]
        roles_gouv = [1417254283694313652, 1417254315684528330, 1417254344180371636, 1417254681243025428, 1417254399004246161, 1417254501110251540, 1417254550951428147, 1417254582156791908, 1417254615224680508, 1417254639069560904, 1417254809253314590]
        # Retirer tous les anciens rôles
        for role_id in [ROLE_PAYS_PAR_DEFAUT] + roles_economie + roles_regime + roles_gouv:
            role_obj = interaction.guild.get_role(role_id)
            if role_obj:
                for membre in role.members:
                    if role_obj in membre.roles:
                        await membre.remove_roles(role_obj)
        # Ajouter les nouveaux rôles si précisés
        for membre in role.members:
            if economie:
                role_economie = interaction.guild.get_role(int(economie))
                if role_economie:
                    await membre.add_roles(role_economie)
            if regime_politique:
                role_regime = interaction.guild.get_role(int(regime_politique))
                if role_regime:
                    await membre.add_roles(role_regime)
            if gouvernement:
                role_gouv = interaction.guild.get_role(int(gouvernement))
                if role_gouv:
                    await membre.add_roles(role_gouv)
            # Toujours ajouter le rôle par défaut
            role_defaut = interaction.guild.get_role(ROLE_PAYS_PAR_DEFAUT)
            if role_defaut:
                await membre.add_roles(role_defaut)
        modifications.append("rôles modifiés")
        if modifications:
            embed = discord.Embed(
                title="🏛️ Pays modifié",
                description=f"> **Pays:** {role.mention}\n> **Modifications:** {', '.join(modifications)}{INVISIBLE_CHAR}",
                color=EMBED_COLOR
            )
            embed.set_image(url=IMAGE_URL)
            await interaction.followup.send(embed=embed)
            log_embed = discord.Embed(
                title=f"🏛️ | Modification de pays",
                description=f"> **Administrateur :** {interaction.user.mention}\n> **Pays modifié : ** {role.mention}\n> **Modifications : ** {', '.join(modifications)}{INVISIBLE_CHAR}",
                color=EMBED_COLOR,
                timestamp=datetime.datetime.now()
            )
            await send_log(interaction.guild, embed=log_embed)
        else:
            await interaction.followup.send("> Aucune modification n'a été apportée.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"> Erreur lors de la modification du pays: {e}", ephemeral=True)

@bot.tree.command(name="creer_drapeau", description="Convertit une image en drapeau style emoji Twitter")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(
    image_url="URL de l'image à convertir en drapeau",
    nom_emoji="Nom à donner à l'emoji (sans espaces ni caractères spéciaux)"
)
async def creer_drapeau(interaction: discord.Interaction, image_url: str, nom_emoji: str):
    """Convertit une image en drapeau style emoji Twitter."""
    await interaction.response.defer(ephemeral=True)
    
    try:
        # Vérifier le nom d'emoji
        if not nom_emoji.replace("_", "").isalnum():
            await interaction.followup.send("> Le nom de l'emoji doit contenir uniquement des lettres, chiffres et underscores.", ephemeral=True)
            return
        
        # Télécharger l'image
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                if resp.status != 200:
                    await interaction.followup.send(f"> Erreur lors du téléchargement de l'image (code {resp.status}).", ephemeral=True)
                    return
                img_bytes = await resp.read()
        
        # Ouvrir l'image
        original = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
        
        # Créer une image carrée avec ratio 4:3 (style Twitter flag)
        width, height = 128, 96
        
        # Redimensionner l'image en préservant son ratio et en la recadrant si nécessaire
        img_ratio = original.width / original.height
        target_ratio = width / height
        
        if img_ratio > target_ratio:  # Image plus large
            new_height = height
            new_width = int(new_height * img_ratio)
            resized = original.resize((new_width, new_height), Image.LANCZOS)
            # Recadrer le centre
            left = (new_width - width) // 2
            resized = resized.crop((left, 0, left + width, height))
        else:  # Image plus haute
            new_width = width
            new_height = int(new_width / img_ratio)
            resized = original.resize((new_width, new_height), Image.LANCZOS)
            # Recadrer le centre
            top = (new_height - height) // 2
            resized = resized.crop((0, top, width, top + height))
        
        # Créer un masque avec coins arrondis (style Twitter)
        # Les drapeaux Twitter ont des coins légèrement arrondis
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        # Rayon d'arrondi style Twitter (environ 10% de la largeur)
        radius = int(width * 0.1)
        
        # Dessiner un rectangle avec coins arrondis
        draw.rectangle((radius, 0, width - radius, height), fill=255)  # Partie horizontale centrale
        draw.rectangle((0, radius, width, height - radius), fill=255)  # Partie verticale centrale
        
        # Coins arrondis
        draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=255)  # Coin supérieur gauche
        draw.pieslice((width - radius * 2, 0, width, radius * 2), 270, 0, fill=255)  # Coin supérieur droit
        draw.pieslice((0, height - radius * 2, radius * 2, height), 90, 180, fill=255)  # Coin inférieur gauche
        draw.pieslice((width - radius * 2, height - radius * 2, width, height), 0, 90, fill=255)  # Coin inférieur droit
        
        # Appliquer le masque
        result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        result.paste(resized, (0, 0), mask)
        
        # Enregistrer en mémoire
        buffer = io.BytesIO()
        result.save(buffer, format="PNG")
        buffer.seek(0)
        
        # Créer l'emoji
        try:
            emoji = await interaction.guild.create_custom_emoji(
                name=nom_emoji,
                image=buffer.read()
            )
            
            # Message de confirmation
            embed = discord.Embed(
                title="🏁 Drapeau créé",
                description=f"> L'emoji a été créé avec succès : {str(emoji)}\n"
                           f"> **Nom :** {emoji.name}\n"
                           f"> **ID :** {emoji.id}{INVISIBLE_CHAR}",
                color=EMBED_COLOR
            )
            embed.set_image(url=emoji.url)
            await interaction.followup.send(embed=embed)
            
        except discord.Forbidden:
            await interaction.followup.send("> Je n'ai pas les permissions nécessaires pour créer des emojis sur ce serveur.", ephemeral=True)
        except discord.HTTPException as e:
                       await interaction.followup.send(f"> Erreur lors de la création de l'emoji : {e}", ephemeral=True)
        
    except Exception as e:
        await interaction.followup.send(f"> Erreur lors de la création du drapeau : {str(e)}", ephemeral=True)

def check_duplicate_json_files():
    """Vérifie s'il existe des fichiers JSON en double dans le projet."""
    json_files = [
        "balances.json", "log_channel.json", "message_log_channel.json", 
        "loans.json", "balances_backup.json",
        "transactions.json", "pays_log_channel.json", "pays_images.json"
    ]
    
    duplicates = []
    for file in json_files:
        root_path = os.path.join(BASE_DIR, file)
        data_path = os.path.join(DATA_DIR, file)
        
        if os.path.exists(root_path) and os.path.exists(data_path):
            duplicates.append(file)
    

    
    if duplicates:
        print(f"AVERTISSEMENT: Les fichiers suivants existent à la fois à la racine et dans le dossier data: {', '.join(duplicates)}")
        print("Pour éviter les conflits, supprimez les fichiers à la racine et gardez uniquement ceux dans le dossier data.")

from discord import Permissions

# Durées de mute disponibles (en secondes)
MUTE_DURATIONS = [
    ("1 minute", 60),
    ("5 minutes", 5 * 60),
    ("10 minutes", 10 * 60),
    ("15 minutes", 15 * 60),
    ("30 minutes", 30 * 60),
    ("1 heure", 60 * 60),
    ("2 heures", 2 * 60 * 60),
    ("4 heures", 4 * 60 * 60),
    ("6 heures", 6 * 60 * 60),
    ("10 heures", 10 * 60 * 60),
    ("24 heures", 24 * 60 * 60),
]

MUTE_ROLE_ID = 1414694151622234212  # ID du rôle mute à utiliser en priorité

def get_mute_role(guild):
    """Retourne le rôle mute par ID si possible, sinon par nom."""
    role = guild.get_role(MUTE_ROLE_ID)
    if role:
        return role
    for role in guild.roles:
        if role.name.lower() == "mute":
            return role
    return None

@bot.tree.command(name="creer_role_mute", description="Crée le rôle mute et configure les permissions sur tous les salons")
@app_commands.checks.has_permissions(administrator=True)
async def creer_role_mute(interaction: discord.Interaction):
    await interaction.response.send_message("Création du rôle mute en cours...", ephemeral=True)
    guild = interaction.guild

    # Vérifier si le rôle mute existe déjà
    mute_role = get_mute_role(guild)
    if mute_role:
        await interaction.followup.send(f"> Le rôle mute existe déjà : {mute_role.mention}", ephemeral=True)
        return

    # Créer le rôle mute
    try:
        mute_role = await guild.create_role(name="Mute", color=discord.Color.grey(), reason="Rôle pour mute")
    except Exception as e:
        await interaction.followup.send(f"> Erreur lors de la création du rôle mute : {e}", ephemeral=True)
        return

    # Configurer les permissions sur toutes les catégories et salons
    for category in guild.categories:
        try:
            await category.set_permissions(mute_role, send_messages=False, speak=False, add_reactions=False)
        except Exception:
            pass
    for channel in guild.channels:
        try:
            await channel.set_permissions(mute_role, send_messages=False, speak=False, add_reactions=False)
        except Exception:
            pass

    embed = discord.Embed(
        description=f"> Le rôle {mute_role.mention} a été créé et configuré sur tous les salons.{INVISIBLE_CHAR}",
        color=EMBED_COLOR
    )
    await interaction.followup.send(embed=embed, ephemeral=True)

# Générer les choix pour la durée
duration_choices = [
    app_commands.Choice(name=label, value=str(seconds))
    for label, seconds in MUTE_DURATIONS
]

@bot.tree.command(name="mute", description="Mute un membre pour une durée définie")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(
    membre="Membre à mute",
    duree="Durée du mute",
    raison="Raison du mute (optionnel)"
)
@app_commands.choices(duree=duration_choices)
async def mute(
    interaction: discord.Interaction,
    membre: discord.Member,
    duree: str,
    raison: str = None
):
    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild
    mute_role = get_mute_role(guild)
    if not mute_role:
        await interaction.followup.send("> Le rôle mute n'existe pas. Utilisez /creer_role_mute d'abord.", ephemeral=True)
        return
    await membre.add_roles(mute_role, reason=raison or "Mute via commande")
    seconds = int(duree)
    label = next((lbl for lbl, sec in MUTE_DURATIONS if sec == seconds), f"{seconds} secondes")
    try:
        await membre.send(
            f"Vous avez été mute sur **{guild.name}** pour {label}." + (f"\nRaison : {raison}" if raison else "")
        )
    except Exception:
        pass
    embed = discord.Embed(
        description=f"> {membre.mention} a été mute pour **{label}**.{INVISIBLE_CHAR}",
        color=discord.Color.orange()
    )
    await interaction.followup.send(embed=embed, ephemeral=True)
    # Log dans le salon de mute
    log_embed = discord.Embed(
        title="🔇 Mute appliqué",
        description=f"> **Utilisateur :** {membre.mention}\n> **Durée :** {label}\n> **Par :** {interaction.user.mention}\n> **Raison :** {raison or 'Non spécifiée'}",
        color=discord.Color.orange(),
        timestamp=datetime.datetime.now()
    )
    await send_mute_log(guild, log_embed)
    # Enregistre le mute actif
    unmute_time = time.time() + seconds
    active_mutes[f"{guild.id}:{membre.id}"] = {
        "guild_id": str(guild.id),
        "user_id": str(membre.id),
        "unmute_time": unmute_time
    }
    save_active_mutes(active_mutes)
    bot.loop.create_task(schedule_unmute(guild.id, membre.id, unmute_time))

@bot.tree.command(name="unmute", description="Retire le mute d'un membre")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(
    membre="Membre à unmute"
)
async def unmute(interaction: discord.Interaction, membre: discord.Member):
    await interaction.response.defer(ephemeral=True)
    mute_role = get_mute_role(interaction.guild)
    if not mute_role:
        await interaction.followup.send("> Le rôle mute n'existe pas.", ephemeral=True)
        return
    if mute_role not in membre.roles:
        await interaction.followup.send("> Ce membre n'est pas mute.", ephemeral=True)
        return
    await membre.remove_roles(mute_role, reason="Unmute via commande")
    try:
        await membre.send(f"Vous avez été unmute sur **{interaction.guild.name}**.")
    except Exception:
        pass
    embed = discord.Embed(
        description=f"> {membre.mention} a été unmute.{INVISIBLE_CHAR}",
        color=discord.Color.green()
    )
    await interaction.followup.send(embed=embed, ephemeral=True)
    # Log dans le salon de mute
    log_embed = discord.Embed(
        title="🔊 Unmute manuel",
        description=f"> **Utilisateur :** {membre.mention}\n> **Par :** {interaction.user.mention}",
        color=discord.Color.green(),
        timestamp=datetime.datetime.now()
    )
    await send_mute_log(interaction.guild, log_embed)
    # Supprime le mute actif si existant
    active_mutes.pop(f"{interaction.guild.id}:{membre.id}", None)
    save_active_mutes(active_mutes)

@bot.tree.command(name="ban", description="Ban un membre du serveur")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(
    membre="Membre à bannir",
    raison="Raison du ban (optionnel)"
)
async def ban(interaction: discord.Interaction, membre: discord.Member, raison: str = None):
    class ConfirmBanView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=30)
        @discord.ui.button(label="Oui", style=discord.ButtonStyle.success)
        async def confirm(self, interaction2: discord.Interaction, button: discord.ui.Button):
            if interaction2.user.id != interaction.user.id:
                await interaction2.response.send_message("Vous n'êtes pas autorisé à confirmer ce ban.", ephemeral=True)
                return
            try:
                try:
                    await membre.send(
                        f"Vous avez été **banni** du serveur **{interaction.guild.name}**."
                        + (f"\nRaison : {raison}" if raison else "")
                    )
                except Exception:
                    pass
                await membre.ban(reason=raison or f"Banni par {interaction.user} via /ban")
                embed = discord.Embed(
                    description=f"> {membre.mention} a été **banni** du serveur.{INVISIBLE_CHAR}",
                    color=discord.Color.red()
                )
                await interaction2.response.edit_message(content=None, embed=embed, view=None)
                log_embed = discord.Embed(
                    title="⛔ Ban appliqué",
                    description=f"> **Utilisateur :** {membre.mention}\n"
                                f"> **Par :** {interaction.user.mention}\n"
                                f"> **Raison :** {raison or 'Non spécifiée'}",
                    color=discord.Color.red(),
                    timestamp=datetime.datetime.now()
                )
                await send_mute_log(interaction.guild, log_embed)
            except Exception as e:
                await interaction2.response.edit_message(content=f"> Erreur lors du ban : {e}", view=None)
        @discord.ui.button(label="Non", style=discord.ButtonStyle.danger)
        async def cancel(self, interaction2: discord.Interaction, button: discord.ui.Button):
            if interaction2.user.id != interaction.user.id:
                await interaction2.response.send_message("Vous n'êtes pas autorisé à annuler.", ephemeral=True)
                return
            await interaction2.response.edit_message(content="❌ Ban annulé.", view=None)
    embed = discord.Embed(
        description=f"> Voulez-vous vraiment bannir {membre.mention} ?",
        color=discord.Color.red()
    )
    await interaction.response.send_message(embed=embed, view=ConfirmBanView(), ephemeral=True)

# === LOG MUTE ===
MUTE_LOG_FILE = os.path.join(DATA_DIR, "mute_log_channel.json")
mute_log_channel_data = {}

def load_mute_log_channel():
    if not os.path.exists(MUTE_LOG_FILE):
        with open(MUTE_LOG_FILE, "w") as f:
            json.dump({}, f)
    try:
        with open(MUTE_LOG_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement du log mute: {e}")
        return {}

def save_mute_log_channel(data):
    try:
        with open(MUTE_LOG_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du log mute: {e}")

mute_log_channel_data.update(load_mute_log_channel())

@bot.tree.command(name="setpermission_mute", description="Réapplique les permissions du rôle mute sur tous les salons et catégories")
@app_commands.checks.has_permissions(administrator=True)
async def setpermission_mute(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild
    mute_role = get_mute_role(guild)
    if not mute_role:
        await interaction.followup.send("> Le rôle mute n'existe pas. Utilisez /creer_role_mute d'abord.", ephemeral=True)
        return
    for category in guild.categories:
        try:
            await category.set_permissions(mute_role, send_messages=False, speak=False, add_reactions=False)
        except Exception:
            pass
    for channel in guild.channels:
        try:
            await channel.set_permissions(mute_role, send_messages=False, speak=False, add_reactions=False)
        except Exception:
            pass
    embed = discord.Embed(
        description=f"> Permissions du rôle {mute_role.mention} réappliquées sur tous les salons et catégories.",
        color=EMBED_COLOR
    )
    await interaction.followup.send(embed=embed, ephemeral=True)

@bot.tree.command(name="setlogmute", description="Définit le salon de logs pour les sanctions mute/unmute")
@app_commands.checks.has_permissions(administrator=True)
async def setlogmute(interaction: discord.Interaction, channel: discord.TextChannel):
    mute_log_channel_data[str(interaction.guild.id)] = channel.id
    save_mute_log_channel(mute_log_channel_data)
    embed = discord.Embed(
        description=f"> Salon de logs mute défini sur {channel.mention}.{INVISIBLE_CHAR}",
        color=EMBED_COLOR
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

# === GESTION DES MUTES PERSISTANTS ===
ACTIVE_MUTES_FILE = os.path.join(DATA_DIR, "active_mutes.json")

def load_active_mutes():
    if not os.path.exists(ACTIVE_MUTES_FILE):
        with open(ACTIVE_MUTES_FILE, "w") as f:
            json.dump({}, f)
    try:
        with open(ACTIVE_MUTES_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement des mutes actifs: {e}")
        return {}

def save_active_mutes(data):
    try:
        with open(ACTIVE_MUTES_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des mutes actifs: {e}")

active_mutes = load_active_mutes()

async def schedule_unmute(guild_id, user_id, unmute_time):
    now = time.time()
    delay = unmute_time - now
    if delay > 0:
        await asyncio.sleep(delay)
    guild = bot.get_guild(int(guild_id))
    if not guild:
        return
    member = guild.get_member(int(user_id))
    mute_role = get_mute_role(guild)
    if member and mute_role and mute_role in member.roles:
        try:
            await member.remove_roles(mute_role, reason="Fin du mute automatique")
            try:
                await member.send(f"Votre sanction mute sur **{guild.name}** est terminée.")
            except Exception:
                pass
            # Log de l'unmute automatique
            unmute_embed = discord.Embed(
                title="🔊 Mute terminé",
                description=f"> **Utilisateur :** {member.mention}\n> **Fin de la durée automatique**",
                color=discord.Color.green(),
                timestamp=datetime.datetime.now()
            )
            await send_mute_log(guild, unmute_embed)
        except Exception:
            pass
    # Nettoyer le mute actif
    active_mutes.pop(f"{guild_id}:{user_id}", None)
    save_active_mutes(active_mutes)

async def restore_mutes_on_start():
    now = time.time()
    for key, mute in list(active_mutes.items()):
        guild_id, user_id = mute["guild_id"], mute["user_id"]
        unmute_time = mute["unmute_time"]
        if unmute_time <= now:
            await schedule_unmute(guild_id, user_id, now)
        else:
            bot.loop.create_task(schedule_unmute(guild_id, user_id, unmute_time))

# ===== NOUVELLES COMMANDES =====

class TriView(discord.ui.View):
    def __init__(self, guild: discord.Guild):
        super().__init__(timeout=None)
        self.guild = guild

@bot.tree.command(name="id", description="Enregistre tous les IDs des membres du serveur dans invites.json")
@app_commands.checks.has_permissions(administrator=True)
async def id(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild
    invites_path = os.path.join(DATA_DIR, "invites.json")
    restore_all_json_from_postgres()
    member_ids = [str(member.id) for member in guild.members if not member.bot]
    # Toujours écrire une liste d'IDs, jamais un objet vide
    if member_ids:
        with open(invites_path, "w") as f:
            json.dump(member_ids, f)
    else:
        with open(invites_path, "w") as f:
            json.dump([], f)
    save_all_json_to_postgres()
    await interaction.followup.send(f"IDs de {len(member_ids)} membres enregistrés dans invites.json.", ephemeral=True)

@bot.tree.command(name="invites", description="Envoie une invitation Discord en MP à tous les membres (admin seulement)")
@app_commands.checks.has_permissions(administrator=True)
async def invites(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild
    invite_link = "https://discord.gg/paxr"
    invites_path = os.path.join(DATA_DIR, "invites.json")
    if os.path.exists(invites_path):
        with open(invites_path, "r") as f:
            invited_ids = set(json.load(f))
    else:
        invited_ids = set()
    sent_count = 0
    failed_count = 0
    for member in guild.members:
        if member.bot or str(member.id) in invited_ids:
            continue
        try:
            await member.send(f"Invitation à rejoindre le serveur : {invite_link}")
            invited_ids.add(str(member.id))
            sent_count += 1
        except Exception:
            failed_count += 1
    # Sauvegarder les IDs invités
    with open(invites_path, "w") as f:
        json.dump(list(invited_ids), f)
    save_all_json_to_postgres()
    await interaction.followup.send(f"> Invitations envoyées à {sent_count} membres. {failed_count} échecs. Les membres déjà invités ne recevront pas de doublon.", ephemeral=True)
    # The following block seems misplaced and should be removed or integrated properly.
    # If you want to send a message with TriView, you should loop over members again or merge logic.
    # For now, comment out or remove the block to fix indentation error.
    # if str(member.id) in mp_tri_responses:
    #     continue
    # try:
    #     await member.send(embed=embed, view=TriView(guild))
    #     count += 1
    # except Exception:
    #     pass  # Ignore les membres qui n'acceptent pas les MP
    # await interaction.followup.send(f"Message envoyé à {count} membres.", ephemeral=True)

# === COMMANDES XP/LEVEL ===
@bot.tree.command(name="set_lvl", description="Active le système de niveau (XP)")
@app_commands.checks.has_permissions(administrator=True)
async def set_lvl(interaction: discord.Interaction):
    global xp_system_status
    guild_id = str(interaction.guild.id)
    if xp_system_status["servers"].get(guild_id, False):
        await interaction.response.send_message(
            "Le système de niveau est déjà actif.", ephemeral=True)
        return
    xp_system_status["servers"][guild_id] = True
    save_xp_system_status(xp_system_status)
    await interaction.response.send_message(
        "Système de niveau activé !", ephemeral=True)
    save_all_json_to_postgres()

@bot.tree.command(name="set_channel_lvl", description="Définit le salon de log pour les passages de niveau")
@app_commands.checks.has_permissions(administrator=True)
async def set_channel_lvl(interaction: discord.Interaction, channel: discord.TextChannel):
    lvl_log_channel_data[str(interaction.guild.id)] = channel.id
    save_lvl_log_channel(lvl_log_channel_data)
    await interaction.response.send_message(
        f"Salon de log niveau défini sur {channel.mention}.", ephemeral=True)

@bot.tree.command(name="lvl", description="Affiche votre niveau et progression XP")
async def lvl(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    if user_id not in levels:
        levels[user_id] = {"xp": 0, "level": 1}
        save_levels(levels)
    xp = levels[user_id]["xp"]
    level = levels[user_id]["level"]
    bar = get_progress_bar(xp, level)
    percent = int((xp / xp_for_level(level)) * 100) if xp_for_level(level) > 0 else 0
    # Détection du grade de palier
    palier_roles = {
        10: 1417893183903502468,
        20: 1417893555376230570,
        30: 1417893729066291391,
        40: 1417893878136176680,
        50: 1417894464122261555,
        60: 1417894846844244139,
        70: 1417895041862733986,
        80: 1417895157553958922,
        90: 1417895282443812884,
        100: 1417895415273099404
    }
    palier = (level // 10) * 10
    grade = None
    if palier in palier_roles:
        role_obj = interaction.guild.get_role(palier_roles[palier])
        if role_obj and role_obj in interaction.user.roles:
            grade = role_obj.name
    embed = discord.Embed(
        title=f"Niveau de {interaction.user.display_name}",
        description=f"⠀\n> − **Niveau :** {level}\n> − **Progression :**\n> {bar}\n" + (f"> − **Grade : {grade}**\n⠀" if grade else "⠀"),
        color=0xebe3bd
    )
    embed.set_image(url="https://zupimages.net/up/21/03/vl8j.png")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="classement_lvl", description="Affiche le classement des membres par niveau")
async def classement_lvl(interaction: discord.Interaction):
    # Récupérer les 15 meilleurs niveaux
    classement = sorted(levels.items(), key=lambda x: x[1]["level"], reverse=True)
    per_page = 15
    pages = [classement[i:i+per_page] for i in range(0, len(classement), per_page)]
    def make_embed(page_idx):
        page = pages[page_idx]
        desc = "⠀\n"
        for idx, (user_id, data) in enumerate(page):
            rank = idx + 1 + page_idx * per_page
            if rank == 1:
                medal = "🥇"
            elif rank == 2:
                medal = "🥈"
            elif rank == 3:
                medal = "🥉"
            else:
                medal = f"{rank}."
            member = interaction.guild.get_member(int(user_id))
            if member:
                desc += f"> {medal} : {member.mention} - **Niveau {data['level']}**\n"
        desc += "⠀"
        embed = discord.Embed(
            title="🔝 | Classement en Niveaux",
            description=desc,
            color=0x162e50
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1412872314525192233/1417982063839154318/PAX_RUINAE_4.gif?ex=68cc7634&is=68cb24b4&hm=5c7411791192069f1030b0aef0e51be790bb957c288658954070e2cc2f1d862c&")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1412872314525192233/1417981197899792565/Sans_titre_1024_x_1024_px_3.png?ex=68cc7566&is=68cb23e6&hm=8e0c7eb0093be4cb173de373bc050949d1efb52fa2e974de8b3dd2acd3b5deaa&")
        return embed

    # Récupérer les 15 meilleurs niveaux
    classement = sorted(levels.items(), key=lambda x: x[1]["level"], reverse=True)
    per_page = 15
    pages = [classement[i:i+per_page] for i in range(0, len(classement), per_page)]
    def make_embed(page_idx):
        page = pages[page_idx]
        desc = "⠀\n"
        for idx, (user_id, data) in enumerate(page):
            rank = idx + 1 + page_idx * per_page
            if rank == 1:
                medal = "🥇"
            elif rank == 2:
                medal = "🥈"
            elif rank == 3:
                medal = "🥉"
            else:
                medal = f"{rank}."
            member = interaction.guild.get_member(int(user_id))
            if member:
                desc += f"> {medal} : {member.mention} - **Niveau {data['level']}**\n"
        desc += "⠀"
        embed = discord.Embed(
            title="🔝 | Classement en Niveaux",
            description=desc,
            color=0x162e50
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1412872314525192233/1417982063839154318/PAX_RUINAE_4.gif?ex=68cc7634&is=68cb24b4&hm=5c7411791192069f1030b0aef0e51be790bb957c288658954070e2cc2f1d862c&")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1412872314525192233/1417981197899792565/Sans_titre_1024_x_1024_px_3.png?ex=68cc7566&is=68cb23e6&hm=8e0c7eb0093be4cb173de373bc050949d1efb52fa2e974de8b3dd2acd3b5deaa&")
        return embed

    class ClassementView(discord.ui.View):
        def __init__(self, pages):
            super().__init__(timeout=600)
            self.pages = pages
            self.page_idx = 0
            self.message = None

        @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.secondary)
        async def prev(self, interaction_btn: discord.Interaction, button: discord.ui.Button):
            if self.page_idx > 0:
                self.page_idx -= 1
                await interaction_btn.response.edit_message(embed=make_embed(self.page_idx), view=self)

        @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.secondary)
        async def next(self, interaction_btn: discord.Interaction, button: discord.ui.Button):
            if self.page_idx < len(self.pages) - 1:
                self.page_idx += 1
                await interaction_btn.response.edit_message(embed=make_embed(self.page_idx), view=self)

    view = ClassementView(pages)
    await interaction.response.send_message(embed=make_embed(0), view=view)


@bot.tree.command(name="creer_emprunt", description="Crée un emprunt et attribue la somme au demandeur")
@app_commands.describe(
    somme="Montant à emprunter",
    taux="Taux d'intérêt (%) - détermine la dette totale",
    duree="Durée supposée de l'emprunt (texte libre, informatif seulement)",
    nombre_paiement="Nombre de paiements prévus (informatif seulement)",
    role="Rôle (pays) à débiter - si non spécifié, débit de la Banque centrale"
)
async def creer_emprunt(
    interaction: discord.Interaction,
    somme: int,
    taux: float,
    duree: str,
    nombre_paiement: int = None,
    role: discord.Role = None
):
    await interaction.response.defer(ephemeral=True)
    
    demandeur_id = str(interaction.user.id)
    role_id = str(role.id) if role else None
    banque_centrale_id = "BOT"
    
    # Vérification des montants
    if somme <= 0 or taux < 0:
        await interaction.followup.send("> Paramètres invalides. Le montant doit être positif et le taux non négatif.", ephemeral=True)
        return
    # Vérification du PIB si le demandeur est un pays
    pib = None
    if role:
        # Récupérer le PIB depuis pib_data
        pib_data = load_pib()
        pib_info = pib_data.get(str(role.id), {})
        pib = pib_info.get("pib", None)
        
        # Si le PIB est trouvé et la somme dépasse 50% du PIB, erreur
        if pib and somme > 0.5 * pib:
            await interaction.followup.send(f"> Erreur : L'emprunt ({format_number(somme)}) dépasse 50% du PIB du pays ({format_number(pib)}). Emprunt refusé pour raison de stabilité économique !", ephemeral=True)
            return
    # Débit du rôle ou Banque centrale
    if role:
        balances[role_id] = balances.get(role_id, 0) - somme
        debiteur = role.mention
        print(f"[DEBUG] Débit du pays {role.name} (ID: {role_id}), montant: {somme}")
    else:
        debiteur = "Banque centrale"
        print(f"[DEBUG] Débit de la Banque centrale, montant: {somme}")
    
    # Crédit du demandeur
    balances[demandeur_id] = balances.get(demandeur_id, 0) + somme
    print(f"[DEBUG] Crédit du demandeur {interaction.user.name} (ID: {demandeur_id}), montant: {somme}")
    # Création de l'emprunt
    emprunt = {
        "id": f"{demandeur_id}-{int(time.time())}",
        "demandeur_id": demandeur_id,
        "role_id": role_id,
        "somme": somme,
        "taux": taux,
        "duree": duree,
        "nombre_paiement": nombre_paiement,
        "restant": somme,
        "date_debut": int(time.time()),
        "remboursements": []
    }
    loans.append(emprunt)
    save_loans(loans)
    save_balances(balances)
    
    print(f"[DEBUG] Emprunt créé: demandeur={demandeur_id}, role_id={role_id}, somme={somme}, taux={taux}")
    print(f"[DEBUG] Total emprunts actifs: {len(loans)}")
    
    # Log de la transaction
    log_transaction(
        from_id=role_id if role else banque_centrale_id,
        to_id=demandeur_id,
        amount=somme,
        transaction_type="emprunt",
        guild_id=str(interaction.guild.id)
    )
    save_all_json_to_postgres()
    # Log embed
    embed = discord.Embed(
        title="💸 | Création d'emprunt",
        description=(
            f"> **Demandeur :** {interaction.user.mention}\n"
            f"> **Montant :** {format_number(somme)} {MONNAIE_EMOJI}\n"
            f"> **Taux :** {taux}%\n"
            f"> **Durée prévue :** {duree} (informatif)\n"
            f"> **Nombre de paiements prévus :** {nombre_paiement if nombre_paiement else 'Non défini'}\n"
            f"> **Débiteur :** {debiteur}{INVISIBLE_CHAR}"
        ),
        color=EMBED_COLOR,
        timestamp=datetime.datetime.now()
    )
    await send_log(interaction.guild, embed=embed)
    
    # Log dans le salon staff
    staff_channel_id = 1412876030980391063
    staff_channel = interaction.guild.get_channel(staff_channel_id)
    if staff_channel:
        await staff_channel.send(embed=embed)
    
    # Réponse à l'utilisateur
    confirmation_embed = discord.Embed(
        title="✅ | Emprunt créé avec succès",
        description=(
            f"> **Montant accordé :** {format_number(somme)} {MONNAIE_EMOJI}\n"
            f"> **Taux d'intérêt :** {taux}%\n"
            f"> **Durée prévue :** {duree} (informatif)\n"
            f"> **Montant total à rembourser :** {format_number(int(somme * (1 + taux / 100)))} {MONNAIE_EMOJI}\n"
            f"> **Source :** {debiteur}\n"
            f"> ⚠️ **Note :** La durée est purement informative, aucun remboursement automatique."
        ),
        color=0x00FF00
    )
    await interaction.followup.send(embed=confirmation_embed, ephemeral=True)


# Commande /liste_emprunt : affiche la liste des emprunts du joueur avec pagination
@bot.tree.command(name="liste_emprunt", description="Affiche la liste de vos emprunts")
async def liste_emprunt(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    # Filtrer les emprunts du joueur
    emprunts_user = [e for e in loans if e["demandeur_id"] == user_id]
    if not emprunts_user:
        await interaction.response.send_message("> Vous n'avez aucun emprunt en cours.", ephemeral=True)
        return
    # Pagination : 5 emprunts par page
    pages = []
    for i in range(0, len(emprunts_user), 5):
        emprunts_page = emprunts_user[i:i+5]
        texte = ""
        for idx, emprunt in enumerate(emprunts_page, start=i+1):
            # Calcul du montant à rembourser
            montant_rembourse = int(emprunt["somme"] * (1 + emprunt["taux"] / 100))
            if emprunt["role_id"]:
                # Emprunt auprès d'un rôle
                role_obj = interaction.guild.get_role(int(emprunt["role_id"])) if emprunt["role_id"] else None
                role_name = role_obj.mention if role_obj else "Rôle inconnu"
                texte += (
                    "⠀\n"
                    f"> {idx}. − Emprunt avec {role_name} :\n"
                    f"> − **Durée :** {emprunt['duree']}\n"
                    f"> − **Taux d'intérêt :** {emprunt['taux']}%\n"
                    f"> − **Somme emprunté :** {emprunt['somme']} {MONNAIE_EMOJI}\n"
                    f"> − **Somme à remboursé :** {montant_rembourse} {MONNAIE_EMOJI}\n⠀"
                )
            else:
                # Emprunt auprès de la Banque centrale
                texte += (
                    "⠀\n"
                    f"> {idx}. − Emprunt formulé à la **Banque centrale** :\n"
                    f"> − **Durée :** {emprunt['duree']}\n"
                    f"> − **Taux d'intérêt :** {emprunt['taux']}%\n"
                    f"> − **Somme emprunté :** {emprunt['somme']} {MONNAIE_EMOJI}\n"
                    f"> − **Somme à remboursé :** {montant_rembourse} {MONNAIE_EMOJI}\n⠀"
                )
        embed = discord.Embed(
            title="💰 | Liste des Emprunts",
            description=texte,
            color=EMBED_COLOR
        )
        pages.append(embed)
    # Affichage avec pagination si besoin
    if len(pages) == 1:
        await interaction.response.send_message(embed=pages[0], ephemeral=True)
    else:
        view = PaginationView(pages, interaction.user.id)
        await interaction.response.send_message(embed=pages[0], view=view, ephemeral=True)

# Commande /remboursement : sélectionne un emprunt et effectue un paiement
@bot.tree.command(name="remboursement", description="Rembourse un emprunt en cours")
@app_commands.describe(
    numero_emprunt="Numéro de l'emprunt à rembourser (voir /liste_emprunt)",
    montant="Montant à rembourser"
)
async def remboursement(
    interaction: discord.Interaction,
    numero_emprunt: int,
    montant: int
):
        """
        Permet de rembourser un emprunt en cours en saisissant son numéro (voir /liste_emprunt).
        Le montant à rembourser inclut le taux d'intérêt.
        Si l'emprunt est auprès de la Banque centrale, l'argent est détruit.
        Si l'emprunt est auprès d'un pays (rôle), l'argent est transféré à ce pays.
        """
        await interaction.response.defer(ephemeral=True)
        user_id = str(interaction.user.id)
        emprunts_user = [e for e in loans if e["demandeur_id"] == user_id]
        if not emprunts_user:
            await interaction.followup.send("> Aucun emprunt trouvé pour vous.", ephemeral=True)
            return
        if numero_emprunt < 1 or numero_emprunt > len(emprunts_user):
            await interaction.followup.send(f"> Numéro d'emprunt invalide. Utilisez /liste_emprunt pour voir vos emprunts.", ephemeral=True)
            return
        emprunt = emprunts_user[numero_emprunt - 1]
        # Calcul du montant total à rembourser (somme + intérêts)
        principal = emprunt.get("somme", 0)
        taux = emprunt.get("taux", 0)
        total_remboursement = int(principal * (1 + taux / 100))
        deja_rembourse = sum([r["montant"] for r in emprunt.get("remboursements", [])])
        restant = total_remboursement - deja_rembourse
        if montant <= 0 or montant > restant:
            await interaction.followup.send(f"> Montant invalide. Il reste à rembourser : {restant} {MONNAIE_EMOJI}.", ephemeral=True)
            return
        # Débit du joueur
        if balances.get(user_id, 0) < montant:
            await interaction.followup.send(f"> Fonds insuffisants pour le remboursement.", ephemeral=True)
            return
        balances[user_id] = balances.get(user_id, 0) - montant
        # Crédit du pays ou destruction
        if emprunt["role_id"]:
            # Créditer le pays
            balances[emprunt["role_id"]] = balances.get(emprunt["role_id"], 0) + montant
            destinataire = interaction.guild.get_role(int(emprunt["role_id"])).mention if interaction.guild.get_role(int(emprunt["role_id"])) else "Pays inconnu"
        else:
            destinataire = "Banque centrale (argent détruit)"
        # Mise à jour du remboursement
        if "remboursements" not in emprunt:
            emprunt["remboursements"] = []
        emprunt["remboursements"].append({"montant": montant, "date": int(time.time())})
        restant_apres = restant - montant
        
        # Si l'emprunt est totalement remboursé, le supprimer de la liste
        if restant_apres <= 0:
            loans.remove(emprunt)
            print(f"[DEBUG] Emprunt n°{numero_emprunt} totalement remboursé et supprimé")
        
        save_balances(balances)
        save_loans(loans)
        save_all_json_to_postgres()
        
        # Message de confirmation
        if restant_apres <= 0:
            await interaction.followup.send(
                f"> Emprunt n°{numero_emprunt} totalement remboursé et supprimé ! ✅\n> Destinataire : {destinataire}\n> Montant total remboursé : {format_number(total_remboursement)} {MONNAIE_EMOJI}.",
                ephemeral=True
            )
        else:
            await interaction.followup.send(
                f"> Remboursement de {format_number(montant)} {MONNAIE_EMOJI} effectué pour l'emprunt n°{numero_emprunt}.\n> Destinataire : {destinataire}\n> Il reste à rembourser : {format_number(restant_apres)} {MONNAIE_EMOJI}.",
                ephemeral=True
            )


@bot.tree.command(name="reset_debt", description="Supprime toutes les dettes et emprunts du serveur")
@app_commands.checks.has_permissions(administrator=True)
async def reset_debt(interaction: discord.Interaction):
    """Supprime toutes les dettes et emprunts."""
    await interaction.response.defer(ephemeral=True)
    
    # Sauvegarder le nombre d'emprunts avant suppression
    nombre_emprunts = len(loans)
    
    # Calculer le montant total des emprunts
    montant_total = 0
    for emprunt in loans:
        principal = emprunt.get("somme", 0)
        taux = emprunt.get("taux", 0)
        montant_total += int(principal * (1 + taux / 100))
    
    # Vider la liste des emprunts
    loans.clear()
    
    # Sauvegarder les changements
    save_loans(loans)
    save_all_json_to_postgres()
    
    # Log de l'action
    embed_log = discord.Embed(
        title="🗑️ | Réinitialisation des dettes",
        description=(
            f"> **Administrateur :** {interaction.user.mention}\n"
            f"> **Emprunts supprimés :** {nombre_emprunts}\n"
            f"> **Montant total effacé :** {format_number(montant_total)} {MONNAIE_EMOJI}\n"
            f"> **Date :** {datetime.datetime.now().strftime('%d/%m/%Y à %H:%M')}"
        ),
        color=0xFF6B6B,
        timestamp=datetime.datetime.now()
    )
    await send_log(interaction.guild, embed=embed_log)
    
    # Confirmation à l'utilisateur
    confirmation_embed = discord.Embed(
        title="✅ | Dettes supprimées",
        description=(
            f"> **{nombre_emprunts} emprunts** ont été supprimés\n"
            f"> **Montant total effacé :** {format_number(montant_total)} {MONNAIE_EMOJI}\n"
            f"> Toutes les dettes ont été annulées"
        ),
        color=0x00FF00
    )
    await interaction.followup.send(embed=confirmation_embed, ephemeral=True)


    # === Mise à jour des salons vocaux de stats ===

async def update_stats_voice_channels(guild):
    category_id = 1418006771053887571
    membres_role_id = 1393340583665209514
    joueurs_role_id = 1410289640170328244
    noms_salons = {
        "membres": f"╭【👥】・𝗠embres : ",
        "joueurs": f"╰【✅】・𝗝oueurs : "
    }
    category = guild.get_channel(category_id)
    if not category or not isinstance(category, discord.CategoryChannel):
        print(f"[STATS VOICE] Catégorie non trouvée ou invalide : {category}")
        return
    membres_role = guild.get_role(membres_role_id)
    joueurs_role = guild.get_role(joueurs_role_id)
    membres_count = len(membres_role.members) if membres_role else 0
    joueurs_count = len(joueurs_role.members) if joueurs_role else 0
    # Cherche les salons existants
    membres_channel = None
    joueurs_channel = None
    for channel in category.voice_channels:
        if channel.name.startswith(noms_salons["membres"]):
            membres_channel = channel
        if channel.name.startswith(noms_salons["joueurs"]):
            joueurs_channel = channel
    # Met à jour ou crée le salon Membres
    membres_name = f"{noms_salons['membres']}{membres_count}"
    if membres_channel:
        await membres_channel.edit(name=membres_name)
    else:
        await category.create_voice_channel(name=membres_name)
    # Met à jour ou crée le salon Joueurs
    joueurs_name = f"{noms_salons['joueurs']}{joueurs_count}"
    if joueurs_channel:
        await joueurs_channel.edit(name=joueurs_name)
    else:
        await category.create_voice_channel(name=joueurs_name)

# === Bloc principal déplacé à la toute fin du fichier ===

# === Tâche planifiée pour mise à jour des salons vocaux de stats ===
from discord.ext.tasks import loop

@loop(seconds=600)
async def update_stats_voice_channels_periodically():
    guild = bot.get_guild(PRIMARY_GUILD_ID)
    if guild:
        print("[DEBUG] Mise à jour périodique des salons vocaux de stats")
        await update_stats_voice_channels(guild)

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user.name}')
    await apply_permanent_presence(bot)

    try:
        cmds = await bot.tree.sync()
        print(f"Commandes synchronisées globalement ({len(cmds)}) : {[c.name for c in cmds]}")
    except Exception as exc:
        print(f"[SYNC ERROR] Synchronisation globale échouée : {exc}")

    await restore_mutes_on_start()
    await verify_economy_data(bot)

    guild = bot.get_guild(PRIMARY_GUILD_ID)
    if guild:
        await update_stats_voice_channels(guild)

    if not update_stats_voice_channels_periodically.is_running():
        update_stats_voice_channels_periodically.start()

    calendrier_data = load_calendrier()
    if calendrier_data and calendrier_data["mois_index"] < len(CALENDRIER_MONTHS):
        if not calendrier_update_task.is_running():
            calendrier_update_task.start()

# === Mise à jour dynamique des salons vocaux de stats ===
@bot.event
async def on_member_update(before, after):
    membres_role_id = WELCOME_ROLE_ID
    joueurs_role_id = 1410289640170328244
    guild = after.guild
    if guild is None:
        return
    before_roles = set(r.id for r in before.roles)
    after_roles = set(r.id for r in after.roles)
    if WELCOME_ROLE_ID not in before_roles and WELCOME_ROLE_ID in after_roles:
        channel = guild.get_channel(WELCOME_CHANNEL_ID)
        if channel:
            try:
                await channel.send(WELCOME_PUBLIC_MESSAGE.format(mention=after.mention))
            except Exception as exc:
                print(f"[WARN] Impossible d'envoyer le message de bienvenue public: {exc}")
        try:
            await after.send(WELCOME_DM_MESSAGE)
        except discord.Forbidden:
            print(f"[WARN] Impossible d'envoyer un DM de bienvenue à {after} (forbidden)")
        except discord.HTTPException as exc:
            print(f"[WARN] Échec de l'envoi du DM de bienvenue: {exc}")
    if membres_role_id in before_roles or membres_role_id in after_roles or joueurs_role_id in before_roles or joueurs_role_id in after_roles:
        print(f"[DEBUG] Changement de rôle détecté pour {after.display_name} (avant: {before_roles}, après: {after_roles})")
        print(f"[DEBUG] Appel de update_stats_voice_channels pour guild: {guild.name} ({guild.id})")
        await update_stats_voice_channels(guild)

    category_id = 1418006771053887571
    membres_role_id = WELCOME_ROLE_ID
    joueurs_role_id = 1410289640170328244
    membres_channel_id = 1418018437485166741
    joueurs_channel_id = 1418018438990925864
    noms_salons = {
        "membres": f"╭【👥】・𝗠embres : ",
        "joueurs": f"╰【✅】・𝗝oueurs : "
    }
    membres_role = guild.get_role(membres_role_id)
    joueurs_role = guild.get_role(joueurs_role_id)
    membres_count = len(membres_role.members) if membres_role else 0
    joueurs_count = len(joueurs_role.members) if joueurs_role else 0
    membres_channel = guild.get_channel(membres_channel_id)
    joueurs_channel = guild.get_channel(joueurs_channel_id) if joueurs_channel_id else None
    membres_name = f"{noms_salons['membres']}{membres_count}"
    joueurs_name = f"{noms_salons['joueurs']}{joueurs_count}"
    # Mise à jour uniquement si le nombre a changé
    if membres_channel:
        if membres_channel.name != membres_name:
            print(f"[DEBUG] Mise à jour du nom du salon Membres: {membres_channel.name} -> {membres_name}")
            await membres_channel.edit(name=membres_name)
        else:
            print(f"[DEBUG] Aucun changement pour le salon Membres")
    else:
        print(f"[DEBUG] Salon Membres non trouvé (ID: {membres_channel_id})")
    if joueurs_channel:
        if joueurs_channel.name != joueurs_name:
            print(f"[DEBUG] Mise à jour du nom du salon Joueurs: {joueurs_channel.name} -> {joueurs_name}")
            await joueurs_channel.edit(name=joueurs_name)
        else:
            print(f"[DEBUG] Aucun changement pour le salon Joueurs")
    else:
        print(f"[DEBUG] Salon Joueurs non modifié (aucun ID fourni)")

@bot.tree.command(name="creer_stats_voice_channels", description="Crée les salons vocaux de stats dans la catégorie stats (temporaire)")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(categorie="Catégorie où créer les salons vocaux de stats")
async def creer_stats_voice_channels(interaction: discord.Interaction, categorie: discord.CategoryChannel):
    await interaction.response.defer(ephemeral=True)
    membres_role_id = 1393340583665209514
    joueurs_role_id = 1410289640170328244
    noms_salons = {
        "membres": f"╭【👥】・𝗠embres : ",
        "joueurs": f"╰【✅】・𝗝oueurs : "
    }
    guild = interaction.guild
    membres_role = guild.get_role(membres_role_id)
    joueurs_role = guild.get_role(joueurs_role_id)
    membres_count = len(membres_role.members) if membres_role else 0
    joueurs_count = len(joueurs_role.members) if joueurs_role else 0
    membres_name = f"{noms_salons['membres']}{membres_count}"
    joueurs_name = f"{noms_salons['joueurs']}{joueurs_count}"
    # Crée les salons vocaux si non existants
    membres_channel = None
    joueurs_channel = None
    for channel in categorie.voice_channels:
        if channel.name.startswith(noms_salons['membres']):
            membres_channel = channel
        if channel.name.startswith(noms_salons['joueurs']):
            joueurs_channel = channel
    if not membres_channel:
        membres_channel = await categorie.create_voice_channel(membres_name)
    if not joueurs_channel:
        joueurs_channel = await categorie.create_voice_channel(joueurs_name)
    embed = discord.Embed(
        description=f"Salons vocaux de stats créés :\n- {membres_channel.mention}\n- {joueurs_channel.mention}",
        color=0xefe7c5
    )
    await interaction.followup.send(embed=embed, ephemeral=True)


# === Commande /guide (présentation serveur) ===
@bot.tree.command(name="guide", description="Guide de présentation du serveur")
@app_commands.checks.has_permissions(administrator=True)
async def guide(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🪐 | Guide de Présentation du Serveur",
        description="⠀\n> − Voici le serveur **PAX RUINAE** <:Logo_PaxRuinae:1410270324985168032>, descendant de plusieurs serveurs sous la direction de <@772821169664426025>. Celui-ci se veut le plus ambitieux de ces projets dans le cadre d'un rôleplay **« Nouvelle ère »**, où le but est de créer sa propre nation dans un monde qui a chuté à la suite d’un apocalypse causé par l'homme. Dans ce rôleplay, vous ferez peut-être partie de ses acteurs qui marqueront l'histoire par leur RP ✨.\n> \n> − Dans ce serveur, vous trouverez tout ce dont vous avez besoin via les boutons en dessous de l'embed, avec des guides dédiés aux questions que vous pourriez vous poser, notamment sur l'intégration au RP ou sur son fonctionnement même. Et ici, dans l'ordre, je vous présente les catégories les plus importantes afin de comprendre l'organisation du serveur.\n> \n> − En premier lieu, il y a la catégorie **« Informations Générales »**. Il y a notamment les différents salons d'annonces : <#1393350471661387846> pour le HRP, et le salon <#1411066244848816179> pour le RP, le salon <#1411066404597268550>, mais également les différents salons liés aux partenariats : le salon <#1410271619930259496> listant les partenariats actifs, le salon <#1411068927978508359> qui liste les différentes conditions si un autre serveur propose un partenariat avec le nôtre, et le salon <#1395547599649378304> qui met en avant la dite pub du serveur.\n> \n> − Il y a également la catégorie **« L'Administration »**. Ici, il y a différents salons qui listent les actions du staff de **PAX RUINAE** <:Logo_PaxRuinae:1410270324985168032>, comme les <#1411053256926302278>, mais également un explicatif des rôles de celui-ci <#1414284229189046385> et de la <#1414283395537572030>.\n> \n> − Enfin, il y a la catégorie **« Règlements du Serveur »**. Elle liste directement tous les règlements dans cette catégorie-ci, à savoir le <#1393318935692312787>, le <#1410450203433111764>, le <#1393324090562973776>, le <#1393324354619576362>, le <#1393325798685016256>, et enfin le <#1410450325248147560>.\n> \n> − <:PX_Attention:1417603257953685616> : Si vous n'avez pas forcément tous les salons dans votre liste, n'oubliez pas d'activer l’option **« Montrer tous les salons »**, cela vous aidera à vous repérer. Dans cette présentation, les salons cités sont __non exhaustifs__ ; il en existe d'autres, plus ou moins importants.\n⠀",
        color=0x162e50
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1412872314525192233/1418276962417512539/PAX_RUINAE.png?ex=68cd88da&is=68cc375a&hm=2d58da59a0d97e4263759860e12b0bf72d7f35785a72d8b1eb08efc1c83310d5&")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1412872314525192233/1418276839624937512/image.png?ex=68cd88bc&is=68cc373c&hm=ad9b769761c9b1c2d4dc6f0a783d3bcaf0ee3c09a48e8cc4fc5a9865458ae806&")
    await interaction.response.send_message(embed=embed, ephemeral=True)

# === CALENDRIER RP ===
CALENDRIER_FILE = os.path.join(DATA_DIR, "calendrier.json")
CALENDRIER_CHANNEL_ID = 1419301872996712458
CALENDRIER_IMAGE_URL = "https://zupimages.net/up/21/03/vl8j.png"
CALENDRIER_COLOR = 0x162e50
CALENDRIER_EMOJI = "<:PX_Calendrier:1417607613587259505>"
CALENDRIER_MONTHS = [
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
]

def load_calendrier():
    if os.path.exists(CALENDRIER_FILE):
        with open(CALENDRIER_FILE, "r") as f:
            return json.load(f)
    return None

def save_calendrier(data):
    with open(CALENDRIER_FILE, "w") as f:
        json.dump(data, f)

def reset_calendrier():
    if os.path.exists(CALENDRIER_FILE):
        os.remove(CALENDRIER_FILE)

from discord.ext.tasks import loop
import pytz
import datetime

@bot.tree.command(name="calendrier", description="Lance le calendrier RP pour une année donnée")
@app_commands.describe(annee="Année RP à lancer (ex: 2025)")
@app_commands.checks.has_permissions(administrator=True)
async def calendrier(interaction: discord.Interaction, annee: int):
    # Initialisation ou reprise
    calendrier_data = load_calendrier()
    if calendrier_data:
        await interaction.response.send_message(f"> Un calendrier est déjà en cours pour l'année {calendrier_data['annee']} ! Utilisez /reset-calendrier pour recommencer.", ephemeral=True)
        return
    calendrier_data = {
        "annee": annee,
        "mois_index": 0,
        "jour_index": 0, # 0 = 1/2, 1 = 2/2
        "last_update": None,
        "messages": []
    }
    save_calendrier(calendrier_data)
    await interaction.response.send_message(f"> Calendrier RP lancé pour l'année {annee}. Mise à jour chaque jour à minuit (heure Paris).", ephemeral=True)
    calendrier_update_task.start()

@bot.tree.command(name="reset-calendrier", description="Réinitialise le calendrier RP")
@app_commands.checks.has_permissions(administrator=True)
async def reset_calendrier_cmd(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    # Arrête la tâche si elle tourne
    if calendrier_update_task.is_running():
        calendrier_update_task.stop()
    # Supprime les messages précédemment envoyés
    calendrier_data = load_calendrier()
    deleted_count = 0
    channel = bot.get_channel(CALENDRIER_CHANNEL_ID)
    message_ids = []
    if calendrier_data:
        message_ids = [int(mid) for mid in calendrier_data.get("messages", []) if str(mid).isdigit()]

    # Fallback: si aucun ID stocké, tenter de retrouver les messages récents du bot
    async def delete_message(message_id: int) -> None:
        nonlocal deleted_count
        if not channel:
            return
        try:
            message = await channel.fetch_message(message_id)
            await message.delete()
            deleted_count += 1
        except (discord.NotFound, discord.Forbidden):
            pass
        except discord.HTTPException:
            pass

    if channel:
        if not message_ids:
            message_ids = []
            async for message in channel.history(limit=100):
                if message.author != bot.user:
                    continue
                if not message.embeds:
                    continue
                embed = message.embeds[0]
                embed_desc = embed.description or ""
                if embed.image and embed.image.url == CALENDRIER_IMAGE_URL:
                    message_ids.append(message.id)
                    continue
                if CALENDRIER_EMOJI in embed_desc:
                    message_ids.append(message.id)
        for mid in message_ids:
            await delete_message(int(mid))

    # Supprime le fichier calendrier.json
    reset_calendrier()

    # Supprime également la sauvegarde PostgreSQL pour éviter une restauration au redémarrage
    remote_deleted = False
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL:
        try:
            import psycopg2  # type: ignore

            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM json_backups WHERE filename = %s", ("calendrier.json",))
                    remote_deleted = cur.rowcount > 0
                conn.commit()
        except Exception as e:
            print(f"[DEBUG] Échec suppression calendrier.json dans PostgreSQL : {e}")

    await interaction.followup.send(
        f"> Le calendrier RP a été totalement réinitialisé. Tous les effets de /calendrier sont annulés."
        + (f" ({deleted_count} message(s) supprimé(s))." if deleted_count else "")
        + (" Sauvegarde PostgreSQL nettoyée." if remote_deleted else ""),
        ephemeral=True
    )
async def generate_help_banner(
    sections: typing.List[typing.Tuple[str, typing.List[typing.Tuple[str, str]]]]
) -> typing.Optional[io.BytesIO]:
    """Construit une image composite pour l'en-tête de l'aide (séparateur + bannière + texte)."""
    try:
        timeout = aiohttp.ClientTimeout(total=8)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(HELP_HEADER_IMAGE_URL) as resp:
                resp.raise_for_status()
                base_bytes = await resp.read()
        base_image = Image.open(io.BytesIO(base_bytes)).convert("RGBA")
    except Exception as exc:
        print(f"[HELP] Impossible de récupérer l'image de base : {exc}")
        base_image = Image.new("RGBA", (960, 360), (48, 60, 122, 255))

    card_margin = 42
    card_padding = 40
    max_inner_width = 980
    scale_ratio = min(max_inner_width / base_image.width, 1.0)
    new_size = (
        max(1, int(base_image.width * scale_ratio)),
        max(1, int(base_image.height * scale_ratio))
    )
    base_image = base_image.resize(new_size, Image.LANCZOS)

    separator_font_path_candidates = [
        "/System/Library/Fonts/SFNSRounded.ttf",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/Library/Fonts/Arial Unicode.ttf"
    ]

    def load_font(size: int) -> ImageFont.FreeTypeFont:
        for path in separator_font_path_candidates:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except Exception:
                    continue
        return ImageFont.load_default()

    separator_font = load_font(34)
    title_font = load_font(46)
    body_font = load_font(30)

    def measure(text: str, font: ImageFont.ImageFont) -> typing.Tuple[int, int]:
        if hasattr(font, "getbbox"):
            bbox = font.getbbox(text)
            return bbox[2] - bbox[0], bbox[3] - bbox[1]
        width, height = font.getsize(text)
        return width, height

    wrap_width = 60
    line_spacing = 8
    section_spacing = 24

    info_blocks = [
        ("Besoin d'un coup de main ?", title_font, (245, 240, 255), 28),
        (
            "Les commandes sont triées selon les autorisations nécessaires. Utilise-les via la barre slash.",
            body_font,
            (215, 210, 225),
            16,
        ),
        (
            "Les sections ci-dessous regroupent tout pour l'administration comme pour les membres.",
            body_font,
            (215, 210, 225),
            16,
        ),
        (
            "Astuce : tape '/' puis les premières lettres de la commande pour la retrouver instantanément.",
            body_font,
            (215, 210, 225),
            section_spacing,
        ),
    ]

    section_title_font = load_font(32)
    bullet_font = body_font

    layout_lines: typing.List[typing.Dict[str, typing.Any]] = []

    def append_text_block(text: str, font: ImageFont.ImageFont, color: typing.Tuple[int, int, int], *, spacing_after: int, wrap: bool = True, bullet: bool = False) -> None:
        if wrap and font != title_font:
            wrapper = textwrap.TextWrapper(width=wrap_width, subsequent_indent="    " if bullet else "")
            lines = wrapper.wrap(text)
        else:
            lines = [text]
        for idx, line in enumerate(lines):
            spacing = line_spacing if idx < len(lines) - 1 else spacing_after
            layout_lines.append({
                "text": line,
                "font": font,
                "color": color,
                "spacing": spacing
            })

    for text, font, color, spacing_after in info_blocks:
        append_text_block(text, font, color, spacing_after=spacing_after, wrap=True, bullet=False)

    for title, commands in sections:
        append_text_block(title, section_title_font, (240, 232, 255), spacing_after=12, wrap=False)
        for name, description in commands:
            formatted = f"• {name} — {description}"
            append_text_block(formatted, bullet_font, (210, 205, 222), spacing_after=10, wrap=True, bullet=True)
        if layout_lines:
            layout_lines[-1]["spacing"] += section_spacing

    if layout_lines:
        layout_lines[-1]["spacing"] = 0

    total_text_height = 0
    for entry in layout_lines:
        _, h = measure(entry["text"], entry["font"])
        total_text_height += h + entry["spacing"]

    _, separator_height = measure(HELP_HEADER_SEPARATOR, separator_font)

    card_width = max(base_image.width + card_padding * 2, max_inner_width + card_padding * 2)
    card_height = (
        card_padding * 2
        + separator_height
        + 24  # espace après le séparateur
        + base_image.height
        + 36  # espace après l'image
        + total_text_height
    )

    canvas_width = card_width + card_margin * 2
    canvas_height = card_height + card_margin * 2

    background_color = (15, 10, 24)
    card_color = (30, 21, 43)
    banner = Image.new("RGB", (canvas_width, canvas_height), background_color)
    draw = ImageDraw.Draw(banner)

    card_rect = (
        card_margin,
        card_margin,
        card_margin + card_width,
        card_margin + card_height
    )
    draw.rounded_rectangle(card_rect, radius=38, fill=card_color)

    sep_width, _ = measure(HELP_HEADER_SEPARATOR, separator_font)
    sep_x = card_margin + (card_width - sep_width) // 2
    sep_y = card_margin + 10
    draw.text((sep_x, sep_y), HELP_HEADER_SEPARATOR, font=separator_font, fill=(210, 205, 220))

    image_x = card_margin + (card_width - base_image.width) // 2
    image_y = sep_y + separator_height + 24
    banner.paste(base_image, (image_x, image_y))

    text_y = image_y + base_image.height + 36
    text_x = card_margin + card_padding
    for entry in layout_lines:
        draw.text((text_x, text_y), entry["text"], font=entry["font"], fill=entry["color"])
        _, h = measure(entry["text"], entry["font"])
        text_y += h + entry["spacing"]

    output = io.BytesIO()
    banner.save(output, format="PNG")
    output.seek(0)
    return output




HAS_ADVANCED_HELP_VIEW = all(
    hasattr(discord.ui, attr)
    for attr in (
        "LayoutView",
        "Container",
        "MediaGallery",
        "MediaGalleryItem",
        "Separator",
        "SeparatorSpacing",
        "TextDisplay",
    )
)


if HAS_ADVANCED_HELP_VIEW:
    class Components(discord.ui.LayoutView):
        container1 = discord.ui.Container(
            discord.ui.MediaGallery(
                discord.MediaGalleryItem(
                    media=HELP_VIEW_TOP_URL,
                ),
            ),
            discord.ui.Separator(visible=True, spacing=discord.SeparatorSpacing.small),
            discord.ui.TextDisplay(content="⠀\n> /\n⠀"),
            discord.ui.Separator(visible=True, spacing=discord.SeparatorSpacing.small),
            discord.ui.MediaGallery(
                discord.MediaGalleryItem(
                    media=HELP_VIEW_BOTTOM_URL,
                ),
            ),
            accent_colour=discord.Colour(1519957),
        )

        def __init__(self, content: str) -> None:
            super().__init__()
            try:
                text_display = self.container1.children[2]
                if isinstance(text_display, discord.ui.TextDisplay):
                    text_display.content = content
            except Exception:
                pass
else:
    Components = None  # type: ignore[assignment]


@bot.tree.command(name="help", description="Affiche la liste complète des commandes du bot")
async def help_command(interaction: discord.Interaction):
    # Vérifier si l'utilisateur est administrateur
    is_admin = interaction.user.guild_permissions.administrator
    
    # Commandes membres organisées par catégorie
    economie_membres = [
        ("/balance", "Consulte le budget et dette/PIB de ton pays."),
        ("/classement_eco", "Affiche le classement des pays par budget."),
        ("/payer", "Transfère des fonds vers un autre pays ou la banque."),
        ("/creer_emprunt", "Crée un emprunt avec un tiers."),
        ("/liste_emprunt", "Liste tes emprunts en cours avec leur statut."),
        ("/remboursement", "Effectue un paiement sur un emprunt en cours."),
    ]
    
    xp_et_autre_membres = [
        ("/lvl", "Affiche ton niveau et ta progression XP."),
        ("/classement_lvl", "Affiche le classement des membres par niveau."),
        ("/help", "Affiche cette fenêtre d'aide."),
    ]
    
    if is_admin:
        # Commandes administrateur organisées par catégorie
        gestion_pays = [
            ("/creer_pays", "Crée un pays avec ses salons et rôles associés."),
            ("/modifier_pays", "Met à jour le nom, PIB, capitale ou dirigeant d'un pays."),
            ("/supprimer_pays", "Supprime un pays et nettoie ses données."),
            ("/modifier_image_pays", "Met à jour l'image utilisée pour un pays."),
            ("/creer_drapeau", "Génère un emoji drapeau à partir d'une image."),
        ]
        
        economie_admin = [
            ("/add_argent", "Ajoute des fonds à un pays."),
            ("/remove_argent", "Retire des fonds d'un pays (admin ou membre du rôle)."),
            ("/reset_economie", "Réinitialise toutes les données économiques."),
            ("/reset_debt", "Supprime toutes les dettes et emprunts du serveur."),
        ]

        moderation = [
            ("/purge", "Supprime jusqu'à 1000 messages dans un salon."),
            ("/creer_role_mute", "Crée le rôle mute et applique les permissions."),
            ("/mute", "Mute un membre pour une durée définie."),
            ("/unmute", "Retire le mute d'un membre."),
            ("/ban", "Bannit un membre du serveur après confirmation."),
            ("/setpermission_mute", "Réapplique les permissions du rôle mute partout."),
        ]
        
        configuration_logs = [
            ("/setlogeconomy", "Définit le salon de logs pour l'économie."),
            ("/setlogpays", "Configure le salon de logs des actions liées aux pays."),
            ("/setlogmute", "Définit le salon de logs pour les sanctions."),
            ("/set_lvl", "Active ou désactive le système de niveaux."),
            ("/set_channel_lvl", "Choisit le salon de logs des passages de niveau."),
        ]
        
        outils_rp = [
            ("/guide", "Guide de présentation du serveur."),
            ("/calendrier", "Lance les annonces du calendrier RP."),
            ("/reset-calendrier", "Réinitialise le calendrier RP en cours."),
            ("/creer_stats_voice_channels", "Génère les salons vocaux de statistiques."),
        ]

        sections_data = [
            ("🏛️ Gestion des Pays", gestion_pays),
            ("💰 Économie & Finance", economie_admin),
            ("🛡️ Modération", moderation),
            ("⚙️ Configuration & Logs", configuration_logs),
            ("🎭 Outils RP", outils_rp),
            ("👥 Économie Membres", economie_membres),
            ("⭐ XP & Divers", xp_et_autre_membres),
        ]
        
        embed = discord.Embed(
            title="Centre d'aide - Mode Administrateur",
            description=(
                "Commandes organisées par catégorie. "
                "Utilise la barre slash pour accéder à toutes les fonctionnalités."
            ),
            color=EMBED_COLOR,
        )
    else:
        # Seules les commandes membres pour les non-admins
        sections_data = [
            ("💰 Économie & Emprunts", economie_membres),
            ("⭐ XP & Divers", xp_et_autre_membres),
        ]
        
        embed = discord.Embed(
            title="Centre d'aide",
            description=(
                "Voici toutes les commandes organisées par catégorie. "
                "Utilise la barre slash pour les exécuter."
            ),
            color=EMBED_COLOR,
        )

    embed.set_thumbnail(url=HELP_THUMBNAIL_URL)
    embed.set_footer(text="Astuce : tape '/' puis le nom de la commande pour voir ses options.")

    for title, commands in sections_data:
        field_lines = [f"`{name}` — {description}" for name, description in commands]
        embed.add_field(name=title, value="\n".join(field_lines), inline=False)

    summary_lines: typing.List[str] = []
    for title, commands in sections_data:
        summary_lines.append(f"**{title}**")
        summary_lines.extend(f"`{name}` — {description}" for name, description in commands)
        summary_lines.append("")
    while summary_lines and not summary_lines[-1]:
        summary_lines.pop()

    condensed_summary = "\n".join(summary_lines)
    if len(condensed_summary) > 1800:
        condensed_summary = condensed_summary[:1797] + "…"
    block_content = f"⠀\n> " + "\n> ".join(condensed_summary.splitlines()) + "\n⠀"

    response_kwargs: dict[str, typing.Any] = {"embed": embed, "ephemeral": True}
    if Components is not None and HAS_ADVANCED_HELP_VIEW:
        response_kwargs["view"] = Components(block_content)  # type: ignore[call-arg]

    await interaction.response.send_message(**response_kwargs)

@loop(minutes=1)
async def calendrier_update_task():
    calendrier_data = load_calendrier()
    if not calendrier_data:
        calendrier_update_task.stop()
        return
    # Vérifier si on doit avancer (minuit heure Paris)
    paris_tz = pytz.timezone("Europe/Paris")
    now = datetime.datetime.now(paris_tz)
    last_update = calendrier_data.get("last_update")
    if last_update:
        last_update_dt = datetime.datetime.fromisoformat(last_update)
        # Ne pas relocaliser si tzinfo déjà présent
        if last_update_dt.tzinfo is None:
            last_update_dt = paris_tz.localize(last_update_dt)
        if last_update_dt.date() == now.date():
            return # déjà mis à jour aujourd'hui
    # Avancer le calendrier
    mois_index = calendrier_data["mois_index"]
    jour_index = calendrier_data["jour_index"]
    if mois_index >= len(CALENDRIER_MONTHS):
        calendrier_update_task.stop()
        return
    mois = CALENDRIER_MONTHS[mois_index]
    jour_str = "1/2" if jour_index == 0 else "2/2"
    # Poster le message
    channel = bot.get_channel(CALENDRIER_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            description=(
                "\u2800\n"
                f"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{CALENDRIER_EMOJI} **{mois} {calendrier_data['annee']} ({jour_str})**\n"
                "\u2800"
            ),
            color=CALENDRIER_COLOR
        )
        embed.set_image(url=CALENDRIER_IMAGE_URL)
        message = await channel.send(embed=embed)
        calendrier_data.setdefault("messages", [])
        calendrier_data["messages"].append(str(message.id))
    # Avancer le jour
    if jour_index == 0:
        calendrier_data["jour_index"] = 1
    else:
        calendrier_data["jour_index"] = 0
        calendrier_data["mois_index"] += 1
    calendrier_data["last_update"] = now.isoformat()
    save_calendrier(calendrier_data)
    # Stop si Décembre 2/2 passé
    if calendrier_data["mois_index"] >= len(CALENDRIER_MONTHS):
        calendrier_update_task.stop()

if __name__ == "__main__":
    # Toujours restaurer les fichiers JSON depuis PostgreSQL avant tout chargement local
    restore_all_json_from_postgres()
    # Recharge l'état XP après restauration
    xp_system_status = load_xp_system_status()
    load_all_data()
    # Charger les niveaux XP au démarrage
    levels = load_levels()
    lvl_log_channel_data = load_lvl_log_channel()
    # Créer le fichier levels.json si absent
    if not os.path.exists(LVL_FILE):
        with open(LVL_FILE, "w") as f:
            json.dump({}, f)
    check_duplicate_json_files()
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    atexit.register(exit_handler)
    print("Démarrage du bot...")
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"Erreur lors du démarrage du bot: {e}")
        save_balances(balances)
        sys.exit(1)
