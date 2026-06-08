import sqlite3
from contextlib import closing
from pathlib import Path

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS facts (
    fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL UNIQUE,
    category TEXT DEFAULT 'general',
    tags TEXT DEFAULT '',
    trust_score REAL DEFAULT 0.5,
    retrieval_count INTEGER DEFAULT 0,
    helpful_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    hrr_vector BLOB
);

CREATE TABLE IF NOT EXISTS entities (
    entity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    entity_type TEXT DEFAULT 'unknown',
    aliases TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fact_entities (
    fact_id INTEGER REFERENCES facts(fact_id),
    entity_id INTEGER REFERENCES entities(entity_id),
    PRIMARY KEY (fact_id, entity_id)
);

CREATE INDEX IF NOT EXISTS idx_facts_trust ON facts(trust_score DESC);
CREATE INDEX IF NOT EXISTS idx_facts_category ON facts(category);
CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name);

CREATE VIRTUAL TABLE IF NOT EXISTS facts_fts
    USING fts5(content, tags, content=facts, content_rowid=fact_id);

CREATE TRIGGER IF NOT EXISTS facts_ai AFTER INSERT ON facts BEGIN
    INSERT INTO facts_fts(rowid, content, tags)
        VALUES (new.fact_id, new.content, new.tags);
END;

CREATE TRIGGER IF NOT EXISTS facts_ad AFTER DELETE ON facts BEGIN
    INSERT INTO facts_fts(facts_fts, rowid, content, tags)
        VALUES ('delete', old.fact_id, old.content, old.tags);
END;

CREATE TRIGGER IF NOT EXISTS facts_au AFTER UPDATE ON facts BEGIN
    INSERT INTO facts_fts(facts_fts, rowid, content, tags)
        VALUES ('delete', old.fact_id, old.content, old.tags);
    INSERT INTO facts_fts(rowid, content, tags)
        VALUES (new.fact_id, new.content, new.tags);
END;

CREATE TABLE IF NOT EXISTS memory_banks (
    bank_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bank_name TEXT NOT NULL UNIQUE,
    vector BLOB NOT NULL,
    dim INTEGER NOT NULL,
    fact_count INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS problem_patterns (
    pattern_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fingerprint TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    symptoms TEXT NOT NULL,
    context TEXT,
    root_cause TEXT,
    status TEXT NOT NULL DEFAULT 'observed'
        CHECK(status IN ('observed', 'investigating', 'resolved', 'accepted')),
    severity TEXT,
    occurrence_count INTEGER NOT NULL DEFAULT 0,
    first_seen_at TEXT NOT NULL DEFAULT (datetime('now')),
    last_seen_at TEXT NOT NULL DEFAULT (datetime('now')),
    resolution_id INTEGER
);

CREATE TABLE IF NOT EXISTS problem_occurrences (
    occurrence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern_id INTEGER NOT NULL REFERENCES problem_patterns(pattern_id),
    session_id TEXT,
    observed_at TEXT NOT NULL DEFAULT (datetime('now')),
    cwd TEXT,
    evidence TEXT NOT NULL,
    attempted_action TEXT,
    outcome TEXT
);

CREATE INDEX IF NOT EXISTS idx_problem_occurrences_pattern
    ON problem_occurrences(pattern_id, observed_at);

CREATE TRIGGER IF NOT EXISTS problem_occurrences_ai
AFTER INSERT ON problem_occurrences
BEGIN
    UPDATE problem_patterns
    SET occurrence_count = occurrence_count + 1,
        last_seen_at = NEW.observed_at
    WHERE pattern_id = NEW.pattern_id;
END;

CREATE TRIGGER IF NOT EXISTS problem_occurrences_ad
AFTER DELETE ON problem_occurrences
BEGIN
    UPDATE problem_patterns
    SET occurrence_count = MAX(0, occurrence_count - 1),
        last_seen_at = COALESCE(
            (
                SELECT MAX(observed_at)
                FROM problem_occurrences
                WHERE pattern_id = OLD.pattern_id
            ),
            first_seen_at
        )
    WHERE pattern_id = OLD.pattern_id;
END;

CREATE TABLE IF NOT EXISTS resolutions (
    resolution_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern_id INTEGER NOT NULL REFERENCES problem_patterns(pattern_id),
    root_cause TEXT NOT NULL,
    solution TEXT NOT NULL,
    verification TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'proposed'
        CHECK(status IN ('proposed', 'verified', 'failed', 'superseded')),
    skill_path TEXT,
    instruction_path TEXT,
    follow_up TEXT,
    verified_at TEXT
);
"""


def initialize_memory_store(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(path)) as connection:
        connection.executescript(SCHEMA_SQL)
