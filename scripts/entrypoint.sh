#!/bin/bash
set -e

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

run_migrations() {
    log "🔄 Lancement des migrations Alembic..."
    if alembic upgrade head; then
        log "✅ Migrations terminées avec succès"
    else
        log "❌ Erreur lors des migrations"
        exit 1
    fi
}

start_app() {
    log "🚀 Démarrage de l'application FastAPI..."
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000
}

# Exécution principale
start_app
run_migrations
