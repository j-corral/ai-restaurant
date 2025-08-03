#!/bin/bash
set -e

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

wait_for_db() {
    log "⏳ Attente de la base de données..."
    while ! pg_isready -h db -p 5432 -U user; do
        log "Base de données non disponible, attente..."
        sleep 2
    done
    log "✅ Base de données disponible"
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
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
}

# Exécution principale
wait_for_db
run_migrations
start_app
