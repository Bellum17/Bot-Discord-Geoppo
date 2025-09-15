import json
import os
import time
import random
from config import (
    BALANCE_FILE, BALANCE_BACKUP_FILE, LOG_FILE, MESSAGE_LOG_FILE,
    LOANS_FILE, PERSONNEL_FILE, STATUS_BOT_FILE, TRANSACTION_LOG_FILE,
    balances, log_channel_data, message_log_channel_data, loans, personnel, status_bot_data
)

def load_all_data():
    """Charge toutes les données nécessaires au démarrage."""
    global balances, log_channel_data, message_log_channel_data, loans, personnel, status_bot_data
    
    # Chargement de toutes les données
    balances.update(load_balances())
    log_channel_data.update(load_log_channel())
    message_log_channel_data.update(load_message_log_channel())
    loans.extend(load_loans())
    personnel.update(load_personnel())
    status_bot_data.update(load_status_bot())
    
    print("Chargement des données terminé")
    return True

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

def load_personnel():
    """Charge les données du personnel."""
    if not os.path.exists(PERSONNEL_FILE):
        with open(PERSONNEL_FILE, "w") as f:
            json.dump({}, f)
    try:
        with open(PERSONNEL_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement du personnel: {e}")
        return {}

def save_personnel(personnel_data):
    """Sauvegarde les données du personnel."""
    try:
        with open(PERSONNEL_FILE, "w") as f:
            json.dump(personnel_data, f)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du personnel: {e}")

def load_status_bot():
    """Charge les données de statut du bot."""
    if not os.path.exists(STATUS_BOT_FILE):
        with open(STATUS_BOT_FILE, "w") as f:
            json.dump({
                "channel_id": None, 
                "message_id": None, 
                "status": "normal",
                "message_history": []
            }, f)
    
    try:
        with open(STATUS_BOT_FILE, "r") as f:
            data = json.load(f)
        
        # Assurer la migration depuis l'ancien format vers le nouveau
        if "message_history" not in data:
            data["message_history"] = []
            # Si un message_id existe, l'ajouter à l'historique
            if data.get("message_id"):
                try:
                    message_id = data["message_id"]
                    if isinstance(message_id, (int, str)):
                        data["message_history"].append(message_id)
                except Exception as e:
                    print(f"Erreur lors de l'ajout du message_id à l'historique: {e}")
            save_status_bot(data)
        
        return data
    except json.JSONDecodeError:
        # Si le fichier est corrompu, créer un nouveau
        print("Fichier de statut corrompu, création d'un nouveau fichier")
        default_data = {
            "channel_id": None, 
            "message_id": None, 
            "status": "normal",
            "message_history": []
        }
        save_status_bot(default_data)
        return default_data
    except Exception as e:
        print(f"Erreur lors du chargement du statut du bot: {e}")
        return {
            "channel_id": None, 
            "message_id": None, 
            "status": "normal",
            "message_history": []
        }

def save_status_bot(data):
    """Sauvegarde les données de statut du bot."""
    # Assurer que les données ont le bon format et valider les types
    if "message_history" not in data:
        data["message_history"] = []
    
    # Assurer que tous les IDs dans message_history sont des entiers ou des chaînes
    cleaned_history = []
    for msg_id in data.get("message_history", []):
        if isinstance(msg_id, (int, str)):
            cleaned_history.append(msg_id)
    data["message_history"] = cleaned_history
    
    try:
        with open(STATUS_BOT_FILE, "w") as f:
            json.dump(data, f, indent=2)  # Ajouter indent pour une meilleure lisibilité
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données de statut: {e}")

def log_transaction(from_id, to_id, amount, transaction_type, guild_id=None):
    """Enregistre une transaction dans le journal."""
    try:
        # Assurer que les types sont corrects
        if isinstance(from_id, int):
            from_id = str(from_id)
        if isinstance(to_id, int):
            to_id = str(to_id)
        if not isinstance(amount, (int, float)):
            amount = 0
        
        transactions = []
        if os.path.exists(TRANSACTION_LOG_FILE):
            with open(TRANSACTION_LOG_FILE, "r") as f:
                try:
                    transactions = json.load(f)
                except json.JSONDecodeError:
                    print("Fichier de transactions corrompu, création d'un nouveau")
                    transactions = []
        
        # Limiter la taille du journal des transactions (garder les 1000 plus récentes)
        if len(transactions) > 1000:
            transactions = transactions[-1000:]
        
        # Ajouter la nouvelle transaction
        transactions.append({
            "timestamp": int(time.time()),
            "from_id": from_id,
            "to_id": to_id,
            "amount": amount,
            "type": transaction_type,
            "guild_id": guild_id
        })
        
        with open(TRANSACTION_LOG_FILE, "w") as f:
            json.dump(transactions, f)
            
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de la transaction: {e}")

def create_backup(backup_dir, backup_time=None):
    """Crée une sauvegarde complète des données."""
    if backup_time is None:
        backup_time = int(time.time())
    
    # Créer le répertoire de sauvegarde s'il n'existe pas
    os.makedirs(backup_dir, exist_ok=True)
    
    try:
        # Sauvegarder toutes les données
        with open(os.path.join(backup_dir, f"balances_backup_{backup_time}.json"), "w") as f:
            json.dump(balances, f)
        with open(os.path.join(backup_dir, f"loans_backup_{backup_time}.json"), "w") as f:
            json.dump(loans, f)
        with open(os.path.join(backup_dir, f"personnel_backup_{backup_time}.json"), "w") as f:
            json.dump(personnel, f)
        with open(os.path.join(backup_dir, f"log_channel_backup_{backup_time}.json"), "w") as f:
            json.dump(log_channel_data, f)
        with open(os.path.join(backup_dir, f"message_log_channel_backup_{backup_time}.json"), "w") as f:
            json.dump(message_log_channel_data, f)
        with open(os.path.join(backup_dir, f"status_bot_backup_{backup_time}.json"), "w") as f:
            json.dump(status_bot_data, f)
        
        print(f"Sauvegarde complète créée avec ID: {backup_time}")
        return True, backup_time
    except Exception as e:
        print(f"Erreur lors de la création de la sauvegarde: {e}")
        return False, None

def restore_backup(backup_dir, backup_time):
    """Restaure une sauvegarde à partir de son ID."""
    global balances, loans, personnel, log_channel_data, message_log_channel_data, status_bot_data
    
    try:
        # Vérifier si les fichiers de sauvegarde existent
        balance_file = os.path.join(backup_dir, f"balances_backup_{backup_time}.json")
        loans_file = os.path.join(backup_dir, f"loans_backup_{backup_time}.json")
        personnel_file = os.path.join(backup_dir, f"personnel_backup_{backup_time}.json")
        log_channel_file = os.path.join(backup_dir, f"log_channel_backup_{backup_time}.json")
        msg_log_file = os.path.join(backup_dir, f"message_log_channel_backup_{backup_time}.json")
        status_bot_file = os.path.join(backup_dir, f"status_bot_backup_{backup_time}.json")
        
        # Restaurer chaque fichier si disponible
        if os.path.exists(balance_file):
            with open(balance_file, "r") as f:
                balances.clear()
                balances.update(json.load(f))
            save_balances(balances)
        
        if os.path.exists(loans_file):
            with open(loans_file, "r") as f:
                loans.clear()
                loans.extend(json.load(f))
            save_loans(loans)
        
        if os.path.exists(personnel_file):
            with open(personnel_file, "r") as f:
                personnel.clear()
                personnel.update(json.load(f))
            save_personnel(personnel)
        
        if os.path.exists(log_channel_file):
            with open(log_channel_file, "r") as f:
                log_channel_data.clear()
                log_channel_data.update(json.load(f))
            save_log_channel(log_channel_data)
        
        if os.path.exists(msg_log_file):
            with open(msg_log_file, "r") as f:
                message_log_channel_data.clear()
                message_log_channel_data.update(json.load(f))
            save_message_log_channel(message_log_channel_data)
        
        if os.path.exists(status_bot_file):
            with open(status_bot_file, "r") as f:
                status_bot_data.clear()
                status_bot_data.update(json.load(f))
            save_status_bot(status_bot_data)
        
        print(f"Sauvegarde {backup_time} restaurée avec succès")
        return True
    except Exception as e:
        print(f"Erreur lors de la restauration de la sauvegarde {backup_time}: {e}")
        return False

def list_backups(backup_dir):
    """Liste toutes les sauvegardes disponibles."""
    if not os.path.exists(backup_dir):
        return []
    
    backups = {}
    for filename in os.listdir(backup_dir):
        if filename.startswith("balances_backup_") and filename.endswith(".json"):
            try:
                backup_id = filename.replace("balances_backup_", "").replace(".json", "")
                backup_time = int(backup_id)
                backup_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(backup_time))
                backups[backup_id] = {
                    "id": backup_id,
                    "timestamp": backup_time,
                    "date": backup_date
                }
            except ValueError:
                # Ignorer les fichiers qui ne suivent pas le format attendu
                continue
    
    # Trier par timestamp (plus récent d'abord)
    return sorted(backups.values(), key=lambda x: x["timestamp"], reverse=True)

def verify_data_integrity():
    """Vérifie l'intégrité des données et effectue des corrections si nécessaire."""
    issues_found = []
    corrections_made = []
    
    # Vérifier les balances
    for role_id, balance in list(balances.items()):
        if not isinstance(balance, (int, float)):
            old_value = balance
            balances[role_id] = 0
            corrections_made.append(f"Balance pour {role_id} corrigée: {old_value} → 0")
        elif balance < 0:
            old_value = balance
            balances[role_id] = 0
            corrections_made.append(f"Balance négative pour {role_id} corrigée: {old_value} → 0")
    
    # Vérifier les prêts
    valid_loans = []
    for loan in loans:
        if not isinstance(loan, dict):
            issues_found.append(f"Prêt invalide détecté (non-dictionnaire): {loan}")
            continue
        
        required_fields = ["emprunteur_id", "preteur_id", "montant_initial", "montant_restant", "taux"]
        if not all(field in loan for field in required_fields):
            issues_found.append(f"Prêt incomplet détecté: {loan}")
            continue
        
        # Correction des valeurs numériques
        for field in ["montant_initial", "montant_restant", "taux"]:
            if not isinstance(loan[field], (int, float)):
                loan[field] = 0
                corrections_made.append(f"Correction de la valeur {field} dans un prêt")
        
        valid_loans.append(loan)
    
    if len(valid_loans) != len(loans):
        loans.clear()
        loans.extend(valid_loans)
        corrections_made.append(f"{len(loans) - len(valid_loans)} prêts invalides supprimés")
    
    # Sauvegarder les corrections
    if corrections_made:
        save_balances(balances)
        save_loans(loans)
    
    return {
        "issues": issues_found,
        "corrections": corrections_made,
        "status": "success" if not issues_found else "warnings"
    }
