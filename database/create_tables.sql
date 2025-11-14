-- Run this command first
CREATE TABLE IF NOT EXISTS carmichael_number (
    number NUMERIC(24, 0) PRIMARY KEY,
    factors BIGINT[] NOT NULL
);

-- After the batch insert, run this command, prevent insert slowdown
CREATE INDEX IF NOT EXISTS factors_index ON carmichael_number USING GIN (factors);

-- 3 - 14
CREATE TABLE IF NOT EXISTS carmichael_number_3 (
    number NUMERIC(24, 0) PRIMARY KEY,
    factors BIGINT[] NOT NULL
);

CREATE TABLE IF NOT EXISTS carmichael_number_4 (
    number NUMERIC(24, 0) PRIMARY KEY,
    factors BIGINT[] NOT NULL
);

CREATE TABLE IF NOT EXISTS carmichael_number_5 (
    number NUMERIC(24, 0) PRIMARY KEY,
    factors BIGINT[] NOT NULL
);

CREATE TABLE IF NOT EXISTS carmichael_number_6 (
    number NUMERIC(24, 0) PRIMARY KEY,
    factors BIGINT[] NOT NULL
);

CREATE TABLE IF NOT EXISTS carmichael_number_7 (
    number NUMERIC(24, 0) PRIMARY KEY,
    factors BIGINT[] NOT NULL
);

CREATE TABLE IF NOT EXISTS carmichael_number_8 (
    number NUMERIC(24, 0) PRIMARY KEY,
    factors BIGINT[] NOT NULL
);

CREATE TABLE IF NOT EXISTS carmichael_number_9 (
    number NUMERIC(24, 0) PRIMARY KEY,
    factors BIGINT[] NOT NULL
);

CREATE TABLE IF NOT EXISTS carmichael_number_10 (
    number NUMERIC(24, 0) PRIMARY KEY,
    factors BIGINT[] NOT NULL
);

CREATE TABLE IF NOT EXISTS carmichael_number_11 (
    number NUMERIC(24, 0) PRIMARY KEY,
    factors BIGINT[] NOT NULL
);

CREATE TABLE IF NOT EXISTS carmichael_number_12 (
    number NUMERIC(24, 0) PRIMARY KEY,
    factors BIGINT[] NOT NULL
);

CREATE TABLE IF NOT EXISTS carmichael_number_13 (
    number NUMERIC(24, 0) PRIMARY KEY,
    factors BIGINT[] NOT NULL
);

CREATE TABLE IF NOT EXISTS carmichael_number_14 (
    number NUMERIC(24, 0) PRIMARY KEY,
    factors BIGINT[] NOT NULL
);