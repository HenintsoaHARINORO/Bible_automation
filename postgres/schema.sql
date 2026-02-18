-- Bible Automation Database Schema
-- Run this file once to initialize your PostgreSQL database

-- ── Table: bible_verses ───────────────────────────────────────────────────────
-- Stores all Bible verses/passages

CREATE TABLE IF NOT EXISTS bible_verses (
    id          SERIAL PRIMARY KEY,
    book        VARCHAR(100)    NOT NULL,
    chapter     INTEGER         NOT NULL,
    verse_start INTEGER         NOT NULL,
    verse_end   INTEGER         NOT NULL,
    passage     TEXT            NOT NULL,
    created_at  TIMESTAMP       DEFAULT NOW()
);

-- ── Table: bible_indexes ──────────────────────────────────────────────────────
-- Tracks which verse was last sent so each day picks up where it left off

CREATE TABLE IF NOT EXISTS bible_indexes (
    id              SERIAL PRIMARY KEY,
    current_book    VARCHAR(100)    NOT NULL DEFAULT 'Genesis',
    current_chapter INTEGER         NOT NULL DEFAULT 1,
    current_verse   INTEGER         NOT NULL DEFAULT 1,
    last_sent       TIMESTAMP       DEFAULT NOW(),
    updated_at      TIMESTAMP       DEFAULT NOW()
);

-- ── Seed: start from Genesis 1:1 ─────────────────────────────────────────────
-- Only inserts if the table is empty

INSERT INTO bible_indexes (current_book, current_chapter, current_verse)
SELECT 'Genesis', 1, 1
WHERE NOT EXISTS (SELECT 1 FROM bible_indexes);
