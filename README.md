# Bot d'Économie pour Discord

Ce bot Discord permet de gérer un système d'économie complet pour votre serveur, avec une monnaie virtuelle, des prêts, du personnel, et plus encore.

## Fonctionnalités

- **Économie de base** : Balances, transferts d'argent, classement
- **Système de prêts** : Création et remboursement de prêts avec intérêts
- **Gestion de personnel** : Recrutement et paiement de salaires
- **Création de pays** : Création de pays avec leur propre économie
- **Journalisation** : Logs des transactions économiques et des actions de modération
- **AutoMod** : Système de modération automatique avec gestion des mots bannis

## Installation

1. Clonez ce dépôt
2. Installez les dépendances : `pip install -r requirements.txt`
3. Créez un fichier `.env` dans le répertoire `data` avec votre token Discord :
   ```
   DISCORD_TOKEN=votre_token_ici
   ```
4. Exécutez le bot : `python client.py`

## Configuration requise

- Python 3.8 ou supérieur
- discord.py 2.0 ou supérieur
- python-dotenv

## Commandes principales

### Économie de base
- `/balance [rôle]` - Affiche votre budget ou celui d'un pays
- `/pay <utilisateur> <montant>` - Paye un utilisateur depuis votre pays
- `/ranking` - Affiche le classement des pays par budget

### Système de prêts
- `/creer_pret <emprunteur> <montant> <taux> <paiements> [preteur]` - Crée un prêt
- `/remboursement_pret <emprunteur> [preteur]` - Effectue un remboursement
- `/remboursement_annuel` - Rembourse automatiquement tous les prêts actifs (admin)

### Personnel
- `/bareme_personnel` - Affiche les coûts de recrutement et salaires
- `/voir_son_personnel <role>` - Affiche le personnel d'un pays
- `/recruter_du_personnel <role> <type> <quantite>` - Recrute du personnel
- `/paiement_annuel_personnel` - Force le paiement des salaires (admin)

### Administration
- `/setlogeconomy <salon>` - Définit le salon des logs économiques
- `/setlogmessage <salon>` - Définit le salon des logs de messages
- `/setautomodlog <salon>` - Définit le salon des logs d'AutoMod
- `/add_money <cible> <montant>` - Ajoute de l'argent
- `/remove_money <cible> <montant>` - Retire de l'argent

## Licence

Ce projet est sous licence MIT.
>>>>>>> e010696 (Sauvegarde locale avant synchronisation)
>>>>>>> ac12a6f (first commit)
