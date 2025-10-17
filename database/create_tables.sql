-- Run this command first
CREATE TABLE carmichael_number (
    number NUMERIC(24, 0) PRIMARY KEY,
    factors BIGINT[] NOT NULL
);

-- After the batch insert, run this command, prevent insert slowdown
CREATE INDEX factors_index ON carmichael_number USING GIN (factors);

-- In case you need a reset
DROP TABLE IF EXISTS carmichael_number;