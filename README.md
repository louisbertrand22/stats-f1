# 🏎️ F1 Dashboard — Projet DevOps

Application **full-stack** qui affiche des statistiques F1 (pilotes, classements, calendrier) via un backend Python et un frontend React. Le projet sert de fil rouge DevOps : conteneurisation, CI/CD, scans de sécurité et déploiement automatisé.

---

## 1) 🧭 Description du projet

- **Frontend** : React + Vite, buildé en fichiers statiques et servi par **Nginx**.
- **Backend** : **FastAPI** (Python) exposant des endpoints REST (health, drivers, standings…).
- **Données** : **Mock data** (recommandé) avec statistiques précises fin 2024, ou API publique **Ergast F1** (discontinuée).
- **Cache** : **Redis** (primaire) + **In-Memory cache** (fallback) pour éviter de solliciter l'API externe à chaque requête. Voir [CACHE.md](CACHE.md).
- **CI/CD** : GitHub Actions (tests, lint, build images, scan Trivy, push vers GHCR, déploiement).
- **Prod** : images Docker poussées sur **GitHub Container Registry (GHCR)** et services déployés sur **Railway**.

### Schéma (simplifié)

```
Frontend (React+Nginx)  -->  Backend (FastAPI)  -->  Mock Data (recommandé)
                               │                      ou Ergast F1 API (discontinuée)
                               └─► Redis (cache, optionnel)
```

> ⚠️ **Important**: L'API Ergast a été discontinuée fin 2024. Utilisez `USE_MOCK_DATA=true` en production.  
> Voir [DEPLOYMENT.md](DEPLOYMENT.md) pour les détails de configuration.

---

## 2) 📚 Description de l’API (Backend)

Base URL (prod) : `https://<TON_BACKEND>.up.railway.app`

| Méthode | Endpoint                         | Description                                 |
|--------:|----------------------------------|---------------------------------------------|
| GET     | `/`                              | Page racine (ping)                          |
| GET     | `/health`                        | Health check                                |
| GET     | `/drivers/current`               | Liste des pilotes de la saison en cours     |
| GET     | `/constructors/current`          | Liste des écuries de la saison              |
| GET     | `/standings/drivers`             | Classement pilotes                          |
| GET     | `/standings/constructors`        | Classement constructeurs                    |
| GET     | `/schedule/current`              | Calendrier de la saison                     |
| GET     | `/race/last`                     | Résultat de la dernière course              |
| GET     | `/driver/{driver_id}/stats`      | Stats détaillées d’un pilote                |
| GET     | `/cache/stats`                   | Statistiques du cache (monitoring)          |

Exemples :
```bash
curl https://<TON_BACKEND>.up.railway.app/health
curl https://<TON_BACKEND>.up.railway.app/drivers/current
curl https://<TON_BACKEND>.up.railway.app/standings/drivers
```

> La doc interactive **Swagger** est disponible si activée : `https://<TON_BACKEND>/docs`.

---

## 3) ▶️ Lancer le projet (local & prod)

### A) Lancer **en local** avec Docker Compose

Prérequis : Docker (Desktop/Engine) + Compose

```bash
# 1) cloner
git clone <URL_DU_REPO>
cd stats-f1

# 2) (optionnel) backend/.env
# REDIS_HOST=redis
# REDIS_PORT=6379

# 3) lancer (build + run)
docker compose up --build
```

Accès :
- Frontend : http://localhost:3000  
- Backend :  http://localhost:8000  
- Docs API : http://localhost:8000/docs  
- Redis :    localhost:6379 (si activé)

> Le front **n’utilise pas de proxy `/api`** : il appelle directement l’URL du backend via la variable **`VITE_API_URL`** (voir section déploiement/CI). En local, le compose la définit vers `http://backend:8000` ou `http://localhost:8000` selon ton setup.

### B) Lancer **backend seul** (dev)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### C) Lancer **frontend seul** (dev)
```bash
cd frontend
npm install
# expose VITE_API_URL pour la dev (ex : backend local)
VITE_API_URL=http://localhost:8000 npm run dev
```

---

## 4) 🧰 Technologies utilisées

- **Backend** : Python 3.11, **FastAPI**, Uvicorn
- **Frontend** : **React** + **Vite**, Nginx
- **Cache** (optionnel) : Redis
- **Conteneurs** : Docker, multi-stage builds
- **Orchestration locale** : Docker Compose
- **CI/CD** : GitHub Actions (tests, lint, build, scan sécurité, push GHCR, déploiement)
- **Sécurité** : **Trivy** (scan de vulnérabilités images)
- **Registry** : **GHCR** (ghcr.io)
- **Hébergement** : **Railway** (frontend & backend)

---

## 5) 🔁 Processus Docker / Build / Déploiement

### A) Images Docker

- **Backend** : `backend/Dockerfile`  
  - Expose `8000`  
  - Lance l’app FastAPI (Uvicorn/Gunicorn)

- **Frontend** : `frontend/Dockerfile`  
  - Étape 1 : build Vite  
  - Étape 2 : Nginx statique (pas de proxy)  
  - Expose `80`

### B) Pipeline GitHub Actions (extrait)

1. **Tests & Lint backend**
   - `pytest`, `flake8`, service Redis (pour tests si besoin)

2. **Build images (local pour scan)**
   - `docker/build-push-action@v6` (backend) avec `load: true` pour scanner
   - **Trivy** : `aquasecurity/trivy-action` → rapport SARIF

3. **Push vers GHCR**
   - Login : `docker/login-action` sur `ghcr.io`
   - Tags générés par `docker/metadata-action`
   - Push **backend** : `ghcr.io/<owner>/<repo>:<tag>`
   - Push **frontend** : `ghcr.io/<owner>/<repo>-frontend:<tag>`

4. **Déploiement (Railway)**
   - Services Railway configurés pour **tirer l’image GHCR**
   - Backend : Internal Port **8000**
   - Frontend : Internal Port **80**
   - **Pas de `/api`** : le front appelle l’API via `VITE_API_URL` **baked at build time**

### C) Spécificité Front **sans `/api`**

Le frontend ne proxifie pas. Il lit l’URL d’API à **build-time** :

- **Dockerfile (frontend)** :
  ```dockerfile
  ARG VITE_API_URL
  ENV VITE_API_URL=${VITE_API_URL}
  RUN npm run build
  ```

- **Workflow (build & push frontend)** :
  ```yaml
  - name: Build and push frontend image
    uses: docker/build-push-action@v6
    with:
      context: ./frontend
      push: true
      tags: ${{ steps.meta-frontend.outputs.tags }}
      labels: ${{ steps.meta-frontend.outputs.labels }}
      cache-from: type=gha
      cache-to: type=gha,mode=max
      build-args: |
        VITE_API_URL=https://<TON_BACKEND>.up.railway.app
  ```

- **Code front** (ex.) :
  ```js
  const base = (import.meta.env.VITE_API_URL || "").replace(/\/$/, "");
  fetch(`${base}/drivers/current`);
  ```

> ⚠️ Si tu changes l’URL backend en prod, **rebuild** l’image frontend (la variable est figée au build).

### D) CORS (sans proxy)
Autorise l’origine du front dans le backend.

**FastAPI :**
```py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://<TON_FRONT>.up.railway.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🧪 Tests

```bash
# Lancer les tests backend
cd backend
pip install -r requirements.txt
pytest tests/ -v

# Couverture
pytest tests/ --cov=. --cov-report=term-missing
```

---

## 🛠️ Commandes utiles Docker

```bash
# Démarrer en arrière-plan
docker compose up -d

# Logs temps réel
docker compose logs -f

# Rebuild (après modifs)
docker compose up --build

# Arrêter
docker compose down

# Nettoyer volumes (⚠️ données perdues)
docker compose down -v
```

---

## 🐞 Troubleshooting

- **Le front affiche rien**
  - Ouvre DevTools → onglet **Network**
  - Vérifie que les requêtes partent vers `https://<TON_BACKEND>/...`
  - Erreur **CORS** → vérifie la whitelist d’origines côté backend
  - 404 → vérifie les routes et le base URL (`VITE_API_URL`)

- **Railway ne déploie pas le front**
  - L’image GHCR existe et est publique (ou credentials ajoutés)
  - Internal Port = **80**

- **Trivy échoue**
  - Assure-toi que l’image est **chargée localement** (`load: true`) avant le scan

---

## 📜 Licence

MIT — usage libre pour l’apprentissage.

---

## 🙌 Contribuer

PRs bienvenues : nouvelles features, docs, refacto, fix.  
Ouvre une issue si tu veux proposer une amélioration.

---

## ✅ Checklist rapide

- [ ] `docker compose up --build` fonctionne en local  
- [ ] CI passe (tests + lint + Trivy)  
- [ ] Images poussées sur GHCR (`backend` et `frontend`)  
- [ ] Railway : backend (port 8000) / frontend (port 80)  
- [ ] Front construit avec `VITE_API_URL` pointant vers le backend prod  
- [ ] CORS configuré côté backend  

Bon run 🏁
