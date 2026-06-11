# IFRI MentorLink — Guide de déploiement sur Render

## Prérequis
- Un compte **GitHub** (gratuit)
- Un compte **Render** (gratuit) — https://render.com

---

## Étape 1 — Préparer le dépôt GitHub

### 1.1 Créer un nouveau dépôt
1. Sur GitHub, cliquer **New repository**
2. Nom : `PIL1_2526_40` (ou ce que vous voulez)
3. Visibilité : **Public** (nécessaire pour le plan gratuit Render)
4. Cliquer **Create repository**

### 1.2 Pousser le code
```bash
# Dans le dossier du projet
cd backend-flask

git init
git add .
git commit -m "Initial commit — IFRI MentorLink v6"
git branch -M main
git remote add origin https://github.com/VOTRE_NOM/PIL1_2526_40.git
git push -u origin main
```

---

## Étape 2 — Créer la base de données PostgreSQL sur Render

1. Sur https://dashboard.render.com → cliquer **New +** → **PostgreSQL**
2. Remplir :
   - **Name** : `mentorlink-db`
   - **Database** : `mentorlink`
   - **User** : `mentorlink_user`
   - **Region** : `Frankfurt (EU Central)` (plus proche de l'Afrique)
   - **Plan** : **Free**
3. Cliquer **Create Database**
4. Attendre ~2 minutes que la BDD soit disponible
5. **Copier** la valeur **Internal Database URL** (on en aura besoin)

---

## Étape 3 — Créer le service Web Flask sur Render

1. Sur le dashboard → **New +** → **Web Service**
2. Connecter votre dépôt GitHub → sélectionner `PIL1_2526_40`
3. Remplir :
   - **Name** : `ifri-mentorlink`
   - **Region** : `Frankfurt (EU Central)`
   - **Branch** : `main`
   - **Root Directory** : `backend-flask` ← **important**
   - **Runtime** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn wsgi:app --config gunicorn.conf.py`
   - **Plan** : **Free**

### 3.1 Variables d'environnement
Cliquer **Add Environment Variable** et ajouter :

| Clé | Valeur |
|-----|--------|
| `DATABASE_URL` | *(coller l'Internal Database URL de l'étape 2)* |
| `JWT_SECRET_KEY` | *(générer une clé aléatoire, ex: `openssl rand -hex 32`)* |
| `FLASK_DEBUG` | `False` |

4. Cliquer **Create Web Service**
5. Render va builder et déployer automatiquement (~3-5 minutes)

---

## Étape 4 — Initialiser la base de données

Une fois le service déployé, ouvrir l'onglet **Shell** sur Render (ou utiliser la Console) :

```bash
# Créer les tables
python init_db.py

# Créer les tables + données de test (5 comptes démo)
python init_db.py --seed
```

Comptes de démo créés avec `--seed` (mot de passe : `password123`) :
- `leonce@ifri.bj` — M2 SI (mentor)
- `jeffry@ifri.bj` — M1 GL (mentor)
- `ibrahim@ifri.bj` — M2 IA (mentor)
- `salomon@ifri.bj` — L3 GL (mentoré)
- `laurine@ifri.bj` — L2 SI (mentorée)

---

## Étape 5 — Accéder à l'application

Render fournit une URL publique du type :
```
https://ifri-mentorlink.onrender.com
```

Votre application est accessible depuis n'importe quel navigateur dans le monde.

---

## Étape 6 — Redéploiements automatiques

Chaque `git push` sur la branche `main` déclenche automatiquement un nouveau déploiement.

```bash
# Modifier du code, puis :
git add .
git commit -m "Fix: description du changement"
git push origin main
# → Render redéploie automatiquement en ~2 minutes
```

---

## Points importants à retenir

### ⚠️ Plan gratuit Render
- Le service se **met en veille** après 15 minutes d'inactivité
- Le premier accès après la mise en veille prend ~30 secondes
- La base de données gratuite **expire après 90 jours**

### 🔐 Sécurité
- Ne jamais versionner le fichier `.env`
- Le fichier `.gitignore` l'exclut déjà
- Changer la `JWT_SECRET_KEY` avec une vraie clé aléatoire en production

### 🗄️ Variables d'environnement sur Render
Les variables sont définies dans **Dashboard → Service → Environment**.
Render les injecte automatiquement au démarrage, pas besoin de fichier `.env` sur le serveur.

---

## Arborescence du projet

```
PIL1_2526_40/
└── backend-flask/
    ├── app/
    │   ├── __init__.py          ← Factory Flask
    │   ├── models.py            ← Modèles SQLAlchemy
    │   ├── routes/
    │   │   ├── auth.py          ← Inscription / Connexion / Reset
    │   │   ├── users.py         ← Profil + Photo + Compétences + Lacunes
    │   │   ├── annonces.py      ← Annonces de mentorat
    │   │   ├── matching.py      ← Algorithme de matching
    │   │   ├── messages.py      ← Messagerie
    │   │   ├── disponibilite.py ← Planning des disponibilités
    │   │   └── main.py          ← Pages HTML
    │   └── utils/
    │       └── decoration.py    ← Décorateur JWT
    ├── static/
    │   ├── css/                 ← Feuilles de style
    │   └── img/                 ← Logo + illustration
    ├── templates/               ← Pages HTML (Jinja2)
    │   ├── login.html
    │   ├── register.html
    │   ├── dashboard.html
    │   ├── annonces.html
    │   ├── matching.html
    │   ├── messages.html
    │   ├── profil.html          ← Avec upload photo
    │   ├── planning.html        ← Planning des disponibilités
    │   ├── forgot_password.html
    │   └── reset_password.html
    ├── config.py                ← Configuration (supporte Render)
    ├── wsgi.py                  ← Point d'entrée Gunicorn
    ├── gunicorn.conf.py         ← Config Gunicorn
    ├── run.py                   ← Développement local
    ├── init_db.py               ← Initialisation BDD + seed
    ├── schema.sql               ← Schéma SQL complet
    ├── requirements.txt         ← Dépendances Python
    ├── render.yaml              ← Config Render (optionnel)
    ├── .gitignore
    └── .env.example             ← Modèle pour .env local
```

---

## Développement local

```bash
cd backend-flask
cp .env.example .env
# Éditer .env avec vos infos PostgreSQL locales

python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows

pip install -r requirements.txt

# Créer la BDD locale
psql -U postgres -c "CREATE DATABASE mentorlink;"
python init_db.py --seed

# Lancer le serveur
python run.py
# → http://localhost:5000
```
