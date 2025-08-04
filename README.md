# Pizzapi 🍕

## Présentation

**Pizzapi** est une application backend moderne développée en Python avec FastAPI et SQLModel, dédiée à la gestion complète d'une pizzeria en ligne. Cette API permet de gérer dynamiquement le menu, de prendre et suivre des commandes clients, et d'intégrer des agents vocaux IA pour automatiser la prise de commandes téléphoniques.

## Objectifs

- **Gestion complète du menu** : Création, modification, suppression et gestion de la disponibilité des pizzas et boissons
- **Système de commandes** : Prise de commandes avec calcul automatique des totaux et suivi des statuts
- **Intelligence artificielle** : Intégration d'agents vocaux pour automatiser la prise de commandes par téléphone
- **Évolutivité** : Architecture moderne permettant l'ajout facile de nouvelles fonctionnalités
- **Automatisation** : Workflows intelligents pour améliorer l'expérience client et la productivité


## Technologies utilisées

### Backend

- **Python 3.11** - Langage principal
- **FastAPI** - Framework web asynchrone et performant
- **SQLModel** - ORM moderne basé sur SQLAlchemy et Pydantic
- **PostgreSQL** - Base de données relationnelle robuste
- **Alembic** - Gestionnaire de migrations de base de données


### Infrastructure

- **Docker** - Conteneurisation des services
- **Dockploy** - Plateforme de déploiement simplifiée
- **UFW** - Configuration firewall pour la sécurité


### Intelligence Artificielle (coming soon)

- **Ollama** - Modèles IA auto-hébergés (Llama 3.2)
- **Retell AI** - Plateforme cloud d'agents vocaux
- **n8n** - Orchestrateur no-code pour workflows d'automatisation


### Services externes (coming soon)

- **Twilio** - Gestion des appels téléphoniques
- **ElevenLabs** - Synthèse vocale de haute qualité


## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Client    │───▶│  FastAPI     │───▶│ PostgreSQL  │
│ (Web/Mobile)│    │   Backend    │    │   Database  │
└─────────────┘    └──────────────┘    └─────────────┘
                           │
                           ▼
                   ┌──────────────┐
                   │  n8n Workflow│
                   │  Orchestrator │
                   └──────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
      ┌─────────────┐ ┌──────────┐ ┌──────────┐
      │   Ollama    │ │Retell AI │ │  Twilio  │
      │ (Self-host) │ │ (Cloud)  │ │ (Calls)  │
      └─────────────┘ └──────────┘ └──────────┘
```


## Fonctionnalités principales

### 🍕 Gestion du menu

- CRUD complet des items du menu
- Gestion des catégories (pizza, boisson, dessert)
- Contrôle de la disponibilité en temps réel
- Mise à jour dynamique des prix


### 📞 Commandes

- Prise de commandes via API REST
- Prise de commandes vocales automatisées
- Calcul automatique des totaux
- Suivi des statuts (pending, confirmed, preparing, ready, delivered)
- Gestion des informations client


### 🤖 Agent vocal IA (Sofia)

- Assistant vocal intelligent nommé Sofia
- Compréhension du langage naturel en français
- Intégration avec le menu dynamique
- Collecte automatique des informations client
- Confirmation des commandes avant validation


### 👨💼 Administration

- Interface d'administration sécurisée
- Authentification JWT avec rôles (admin/utilisateur)
- Gestion des commandes par statut
- Logs et analytiques des appels


## Installation et déploiement

### Prérequis

- VPS avec Docker
- Dockploy installé
- Nom de domaine configuré


### Services à déployer

1. **PostgreSQL** (base de données)
2. **FastAPI Backend** (API principale)
3. **Ollama** (IA locale - optionnel)
4. **n8n** (orchestrateur de workflows)

### Configuration des variables d'environnement

```env
# Base de données
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/pizza
DATABASE_URL_SYNC=postgresql+psycopg2://user:password@db:5432/pizza

# Sécurité
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256

# Services externes
RETELL_API_KEY=your-retell-api-key
OPENAI_API_KEY=your-openai-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
```


## Endpoints API

### Authentification

- `POST /api/auth/login` - Connexion admin
- `GET /api/auth/me` - Informations utilisateur actuel


### Menu (Public)

- `GET /api/menu/` - Afficher le menu disponible
- `GET /api/menu/categories` - Lister les catégories
- `GET /api/menu/category/{category}` - Menu par catégorie


### Menu (Admin)

- `POST /api/menu/admin/` - Créer un item
- `PUT /api/menu/admin/{id}` - Modifier un item
- `DELETE /api/menu/admin/{id}` - Supprimer un item
- `PATCH /api/menu/admin/{id}/toggle-availability` - Changer disponibilité


### Commandes (Public)

- `POST /api/orders/` - Passer une commande
- `GET /api/orders/{id}` - Détails d'une commande


### Commandes (Admin)

- `GET /api/orders/admin/all` - Toutes les commandes
- `GET /api/orders/admin/status/{status}` - Commandes par statut
- `PATCH /api/orders/admin/{id}/status` - Modifier le statut


## Utilisation de l'agent vocal

1. **Configuration Retell AI** avec le prompt optimisé
2. **Déploiement du workflow n8n** pour l'intégration
3. **Configuration du numéro de téléphone** via Twilio
4. **Test et mise en production**

### Exemple d'appel client (coming soon)

```
Client: "Bonjour, je voudrais commander 2 Pizza Margherita et 1 Coca-Cola"
Sofia: "Parfait ! Donc 2 Pizza Margherita et 1 Coca-Cola. Puis-je avoir votre nom et numéro de téléphone ?"
Client: "Jean Dupont, 0123456789"
Sofia: "Merci ! Votre commande sera prête dans 20 minutes pour un total de 27,50€"
```


## Sécurité

- **Authentification JWT** pour les endpoints administrateur
- **Hashage bcrypt** des mots de passe
- **Validation Pydantic** des données d'entrée
- **Firewall UFW** configuré pour limiter l'accès
- **HTTPS/SSL** recommandé pour la production


## Tests

Collection Bruno incluse pour tester tous les endpoints :

- Authentification et gestion des tokens
- CRUD complet du menu
- Création et gestion des commandes
- Tests des workflows n8n


## Objectifs futurs

- 💳 **Intégration paiement** en ligne (Stripe, PayPal)
- 🚚 **Système de livraison** avec géolocalisation
- 📱 **Application mobile** client
- 🌐 **Interface web** d'administration
- 📊 **Tableaux de bord** et analytics avancés
- 🔄 **Intégrations** avec d'autres services (comptabilité, stock)


## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouvelles fonctionnalités
- Améliorer la documentation


## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

**Développé avec ❤️ pour moderniser la gestion des pizzerias**

*Pizzapi - Transformez votre pizzeria avec l'intelligence artificielle !* 🚀

