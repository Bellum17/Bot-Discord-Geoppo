# Bot d'Économie pour Discord

Ce bot Discord gère un système d'économie avancé pour votre serveur, avec une monnaie virtuelle, des prêts, du personnel, la création de pays, et une persistance robuste des données via PostgreSQL (Railway).

## Fonctionnalités principales

- **Économie de base** : Balances, transferts d'argent, classement
- **Système de prêts** : Création et remboursement de prêts avec intérêts
- **Gestion de personnel** : Recrutement et paiement de salaires
- **Création de pays** : Pays avec économie propre, salons et rôles dédiés
- **Journalisation** : Logs des transactions économiques et des actions de modération
- **AutoMod** : Système de modération automatique avec gestion des mots bannis
- **Sauvegarde automatique** : Toutes les modifications économiques sont sauvegardées dans PostgreSQL après chaque commande
- **Restauration automatique** : Les données d'économie sont restaurées depuis PostgreSQL au démarrage du bot

## Installation

1. Clonez ce dépôt
2. Installez les dépendances : `pip install -r requirements.txt`
3. Créez un fichier `.env` à la racine avec votre token Discord et l'URL PostgreSQL :
   ```
   DISCORD_TOKEN=votre_token_ici
   DATABASE_URL=postgresql://user:password@host:port/dbname
   ```
4. Exécutez le bot : `python client.py`

## Configuration requise

- Python 3.8 ou supérieur
- discord.py 2.0 ou supérieur
- python-dotenv
- psycopg2-binary

## Persistance des données (Railway/PostgreSQL)

- Les fichiers d'économie (`balances.json`, `balances_backup.json`, `loans.json`, `transactions.json`) sont automatiquement sauvegardés dans la base PostgreSQL après chaque commande économique.
- Au démarrage, le bot restaure ces fichiers depuis la base PostgreSQL.
- Si vous supprimez le contenu des fichiers JSON, ils seront recréés automatiquement lors de l'utilisation des commandes du bot.
- Plus de perte de données lors des redéploiements Railway.

## Commandes principales

### Économie de base
- `/balance [rôle]` - Affiche le budget d'un pays
- `/payer <rôle> <montant>` - Paye un autre pays ou détruit de l'argent
- `/ranking` - Affiche l'argent total en circulation

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
- `/setlogpays <salon>` - Définit le salon des logs de pays
- `/add_argent <rôle> <montant>` - Ajoute de l'argent à un pays
- `/remove_argent <rôle> <montant>` - Retire de l'argent à un pays
- `/reset_economie` - Réinitialise toute l'économie (admin)

## Bonnes pratiques

- Pour repartir de zéro, videz les fichiers JSON d'économie (`data/balances.json`, etc.) : ils seront recréés automatiquement.
- Toutes les modifications sont persistées dans PostgreSQL, même après un redéploiement Railway.

## Licence

Ce projet est sous licence MIT.
>>>>>>> e010696 (Sauvegarde locale avant synchronisation)
>>>>>>> ac12a6f (first commit)
