---
title: "Template: Automated Migration Runner"
type: "template"
status: "active"
---

# 🚀 Automated Migration Runner (Template)

This generic template implements the "Automated Schema Update Engine" described in `FCVW/DATA.md` Section 12.
When instantiating a new project, the AI agent or developer must adapt this logic into the actual application codebase (e.g., in Node.js, Python, or Go) to ensure databases are safely upgraded on startup.

## The Logic (Pseudo-code / Node.js standard)

```javascript
/**
 * FCVW Automated Schema Update Engine
 * Runs on application startup.
 * Ensures the database schema matches the version recorded in FCVW/DATA.md
 */

const fs = require('fs');
const path = require('path');
const db = require('./db_connection'); // Your SQLite or Postgres driver

const TARGET_VERSION = 3; // Must match the version defined in DATA.md

async function runMigrations() {
  console.log("Checking database schema version...");

  // 1. Check current schema metadata
  // Create table if it does not exist (for brand new databases)
  await db.exec(`
    CREATE TABLE IF NOT EXISTS schema_metadata (
        version INTEGER PRIMARY KEY,
        applied_at TEXT NOT NULL,
        description TEXT NOT NULL
    );
  `);

  const row = await db.get("SELECT MAX(version) as current_version FROM schema_metadata");
  const currentVersion = row?.current_version || 0;

  if (currentVersion >= TARGET_VERSION) {
    console.log(`Database is up to date (Version ${currentVersion}).`);
    return;
  }

  console.log(`Upgrading database from version ${currentVersion} to ${TARGET_VERSION}...`);

  // 2. Automated Backup
  const dbPath = path.join(__dirname, '../data/app.db');
  const backupPath = path.join(__dirname, '../data/app.db.bak');
  if (fs.existsSync(dbPath)) {
      fs.copyFileSync(dbPath, backupPath);
      console.log("Backup created at app.db.bak");
  }

  // 3. Apply Migrations Sequentially
  for (let v = currentVersion + 1; v <= TARGET_VERSION; v++) {
    const migrationFile = path.join(__dirname, `../data/migrations/V${v}.sql`);

    if (!fs.existsSync(migrationFile)) {
      throw new Error(`Migration file missing: V${v}.sql`);
    }

    const sqlScript = fs.readFileSync(migrationFile, 'utf8');

    try {
      // Execute in strict transaction
      await db.exec('BEGIN TRANSACTION;');
      await db.exec(sqlScript);
      await db.exec(`
        INSERT INTO schema_metadata (version, applied_at, description)
        VALUES (${v}, datetime('now'), 'Applied migration V${v}');
      `);
      await db.exec('COMMIT;');
      console.log(`Migration V${v} applied successfully.`);
    } catch (error) {
      // 4. Failure Recovery / Rollback
      await db.exec('ROLLBACK TRANSACTION;');
      console.error(`FATAL: Migration V${v} failed! Rolled back transaction.`, error);

      // Restore backup if it existed
      if (fs.existsSync(backupPath)) {
          fs.copyFileSync(backupPath, dbPath);
          console.log("Restored previous database state from backup.");
      }

      process.exit(1); // Halt application to prevent silent corruption
    }
  }

  console.log("All migrations applied successfully.");
}

module.exports = runMigrations;
```

## How to use this template
1. In Phase 0 of a new project, copy this logic into a file like `src/db/migrate.js` or `src/db/migrate.py`.
2. Connect it to your actual database driver.
3. Call it right before starting your local server or API.
4. Delete this template from your project if you don't need to keep it in `governance/`.
