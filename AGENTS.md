# AGENTS.md

This file provides guidance to AI coding agents working with this repository.

## Project Overview

Strapi v5 headless CMS application (JavaScript/CommonJS) serving as a content backend. Uses SQLite by default (configurable to MySQL/PostgreSQL). Requires Node.js >=18.0.0 <=22.x.x.

## Commands

```bash
npm run develop        # Start dev server with auto-reload
npm run build          # Build admin panel for production
npm run start          # Start production server
npm run seed:example   # Seed database with example data from data/data.json
npm run deploy         # Deploy to Strapi Cloud
```

## Architecture

### Content Model

**Collection types** (multiple entries): Article, Author, Category
**Single types** (singletons): Global (site settings + SEO), About

**Relationships**: Article → many-to-one with Author and Category.

**Dynamic zones** on Article and About use shared components: `shared.media`, `shared.rich-text`, `shared.quote`, `shared.slider`, `shared.seo`.

### Source Layout

- `src/api/{entity}/` — Each entity has `content-types/{entity}/schema.json`, `controllers/{entity}.js`, `services/{entity}.js`, `routes/{entity}.js`
- `src/components/shared/` — Reusable component schemas (JSON)
- `src/bootstrap.js` — App initialization; seeds database on first run using `data/data.json`
- `config/` — Server, database, admin, API, and middleware configuration (CommonJS modules)
- `scripts/seed.js` — Standalone seed script

### Conventions

- Controllers, services, and routes all use Strapi's factory pattern (`createCoreController`, `createCoreService`, `createCoreRouter`) with minimal custom logic
- Config files are CommonJS modules that export functions, using `env('KEY', default)` with typed getters (`env.int()`, `env.bool()`)
- Permission actions follow `api::{entity}.{entity}.{action}` naming
- Public role gets read-only access (find, findOne) configured in bootstrap
- REST API pagination: default 25 items, max 100, `withCount: true`
- Bootstrap checks `pluginStore` for `initHasRun` flag to prevent duplicate seeding

### Adding a New Content Type

1. Create `src/api/{entity}/content-types/{entity}/schema.json` with the schema definition
2. Create `src/api/{entity}/controllers/{entity}.js` using `createCoreController('api::{entity}.{entity}')`
3. Create `src/api/{entity}/services/{entity}.js` using `createCoreService('api::{entity}.{entity}')`
4. Create `src/api/{entity}/routes/{entity}.js` using `createCoreRouter('api::{entity}.{entity}')`
5. If the type needs public read access, add permission grants in `src/bootstrap.js`

### File Naming

Lowercase only, hyphens for multi-word names, no spaces or special characters (e.g., `rich-text.json`, `article.js`).
