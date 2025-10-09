# 🏎️ F1 Dashboard - Projet DevOps

Un projet complet pour apprendre le DevOps en travaillant avec les données de la Formule 1.

## 🎯 Objectifs pédagogiques

- **Conteneurisation** : Docker et Docker Compose
- **CI/CD** : GitHub Actions avec tests automatisés
- **APIs REST** : FastAPI avec documentation Swagger
- **Cache** : Redis pour optimiser les performances
- **Base de données** : PostgreSQL
- **Tests** : pytest avec couverture de code
- **Monitoring** : Health checks et métriques

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│   Backend   │────▶│  Ergast API │
│   (React)   │     │  (FastAPI)  │     │     (F1)    │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    ▼              ▼
              ┌──────────┐   ┌──────────┐
              │  Redis   │   │ Postgres │
              │  (Cache) │   │   (DB)   │
              └──────────┘   └──────────┘
```

## 🚀 Démarrage rapide

### Prérequis

- Docker Desktop installé
- Git
- Un compte GitHub

### Installation

1. **Cloner le projet**
```bash
git clone <votre-repo>
cd f1-dashboard
```

2. **Créer la structure des dossiers**
```bash
mkdir -p backend/app backend/tests frontend/src nginx .github/workflows
```

3. **Copier les fichiers de configuration**
   - Copiez tous les fichiers que je vous ai fournis dans les bons dossiers
   - `main.py` et `requirements.txt` dans `backend/`
   - `Dockerfile` pour le backend dans `backend/`
   - `docker-compose.yml` à la racine
   - `ci-cd.yml` dans `.github/workflows/`
   - `test_api.py` dans `backend/tests/`

4. **Créer le fichier .env** (optionnel)
```bash
# backend/.env
DATABASE_URL=postgresql://f1user:f1password@postgres:5432/f1db
REDIS_HOST=redis
REDIS_PORT=6379
```

5. **Lancer l'application**
```bash
docker compose up --build
```

6. **Accéder aux services**
   - 🌐 Frontend : http://localhost:3000
   - 🔧 Backend API : http://localhost:8000
   - 📚 Documentation API : http://localhost:8000/docs
   - 🗄️ PostgreSQL : localhost:5432
   - 💾 Redis : localhost:6379

## 📋 Commandes utiles

### Docker
```bash
# Démarrer les services
docker compose up -d

# Voir les logs
docker compose logs -f

# Arrêter les services
docker compose down

# Rebuild après modification
docker compose up --build

# Nettoyer tout (attention : supprime les données)
docker compose down -v
```

### Tests
```bash
# Tests backend
cd backend
pip install -r requirements.txt
pytest tests/ -v

# Tests avec couverture
pytest tests/ --cov=. --cov-report=html
```

### API
```bash
# Tester les endpoints
curl http://localhost:8000/health
curl http://localhost:8000/drivers/current
curl http://localhost:8000/standings/drivers
curl http://localhost:8000/standings/constructors
curl http://localhost:8000/schedule/current
curl http://localhost:8000/race/last
```

## 🧪 Tests et CI/CD

Le pipeline GitHub Actions s'exécute automatiquement sur chaque push et pull request :

1. **Tests Backend** : pytest avec Redis
2. **Linting** : flake8 pour la qualité du code
3. **Build Docker** : construction des images
4. **Scan de sécurité** : Trivy pour les vulnérabilités
5. **Tests d'intégration** : vérification de l'ensemble du système
6. **Déploiement** : sur la branche main uniquement

### Configurer GitHub Actions

1. **Activer GitHub Actions** dans votre repo
2. **Ajouter les secrets** (Settings > Secrets) :
   - `SONAR_TOKEN` (optionnel, pour SonarCloud)

3. **Push votre code**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

## 📊 Endpoints de l'API

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Page d'accueil de l'API |
| `/health` | GET | Health check |
| `/drivers/current` | GET | Liste des pilotes actuels |
| `/constructors/current` | GET | Liste des écuries actuelles |
| `/standings/drivers` | GET | Classement des pilotes |
| `/standings/constructors` | GET | Classement des écuries |
| `/schedule/current` | GET | Calendrier de la saison |
| `/race/last` | GET | Résultats de la dernière course |
| `/driver/{driver_id}/stats` | GET | Statistiques d'un pilote |

## 🔧 Améliorations futures

### Phase 1 - Monitoring (1-2 semaines)
- [ ] Ajouter Prometheus pour les métriques
- [ ] Configurer Grafana pour les dashboards
- [ ] Implémenter des alertes
- [ ] Ajouter des logs structurés (ELK stack)

### Phase 2 - Infrastructure as Code (2-3 semaines)
- [ ] Terraform pour AWS/GCP/Azure
- [ ] Créer des environnements (dev, staging, prod)
- [ ] Configurer un CDN (CloudFront/CloudFlare)
- [ ] Mettre en place un load balancer

### Phase 3 - Kubernetes (3-4 semaines)
- [ ] Déployer sur Minikube localement
- [ ] Créer les manifests K8s (Deployments, Services, Ingress)
- [ ] Configurer les HPA (Horizontal Pod Autoscaler)
- [ ] Implémenter des health checks K8s
- [ ] Ajouter des secrets et ConfigMaps

### Phase 4 - Avancé (4-6 semaines)
- [ ] Service mesh (Istio)
- [ ] GitOps avec ArgoCD
- [ ] Canary deployments
- [ ] Blue-green deployments
- [ ] Backup et disaster recovery

## 🎓 Concepts DevOps couverts

- ✅ **Containerization** : Docker multi-stage builds
- ✅ **Orchestration** : Docker Compose
- ✅ **CI/CD** : GitHub Actions
- ✅ **Testing** : Tests unitaires et d'intégration
- ✅ **Caching** : Redis
- ✅ **Database** : PostgreSQL
- ✅ **API Documentation** : Swagger/OpenAPI
- ✅ **Security** : Trivy scanning
- ✅ **Health Checks** : Monitoring basique

## 📚 Ressources pour approfondir

### Documentation officielle
- [Docker Docs](https://docs.docker.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Ergast F1 API](http://ergast.com/mrd/)

### Tutoriels recommandés
- Docker Mastery (Udemy)
- Kubernetes for Developers
- DevOps Bootcamp

## 🐛 Troubleshooting

### Le backend ne démarre pas
```bash
# Vérifier les logs
docker compose logs backend

# Vérifier que Redis et Postgres sont up
docker compose ps
```

### Redis connection refused
```bash
# Redémarrer Redis
docker compose restart redis

# Vérifier les logs Redis
docker compose logs redis
```

### L'API ne retourne pas de données
- Vérifiez votre connexion internet (l'API Ergast est externe)
- Vérifiez les logs : `docker-compose logs backend`
- Testez l'API Ergast directement : https://ergast.com/api/f1/current/drivers.json

### Tests qui échouent
```bash
# Installer les dépendances
pip install -r backend/requirements.txt

# Lancer Redis localement ou via Docker
docker run -d -p 6379:6379 redis:7-alpine

# Relancer les tests
pytest backend/tests/ -v
```

## 🤝 Contribution

Ce projet est à but éducatif. N'hésitez pas à :
- Ajouter de nouvelles fonctionnalités
- Améliorer le code existant
- Corriger des bugs
- Améliorer la documentation

## 📝 Licence

MIT License - Libre d'utilisation pour l'apprentissage

## 🏁 Prochaines étapes

1. **Comprendre le code** : Lisez et comprenez chaque fichier
2. **Tester localement** : Lancez le projet et testez tous les endpoints
3. **Personnaliser** : Ajoutez vos propres fonctionnalités
4. **Déployer** : Mettez en production sur un cloud provider
5. **Monitorer** : Ajoutez du monitoring et des alertes
6. **Optimiser** : Améliorez les performances et la sécurité

Bon apprentissage ! 🚀