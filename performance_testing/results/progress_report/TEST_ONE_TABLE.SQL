-- Query with 1 prime
-- 5
EXPLAIN ANALYZE
SELECT number
FROM carmichael_number
WHERE factors @> ARRAY[5]::BIGINT[];

-- 14348909
EXPLAIN ANALYZE
SELECT number
FROM carmichael_number
WHERE factors @> ARRAY[14348909]::BIGINT[];

-- 2 Primes
-- 11 13
EXPLAIN ANALYZE
SELECT number
FROM carmichael_number
WHERE factors @> ARRAY[11, 13]::BIGINT[];

-- 21871 21881
EXPLAIN ANALYZE
SELECT number
FROM carmichael_number
WHERE factors @> ARRAY[21871, 21881]::BIGINT[];

-- 3 Primes
-- 11 13 17
EXPLAIN ANALYZE
SELECT number
FROM carmichael_number
WHERE factors @> ARRAY[11, 13, 17]::BIGINT[];

-- 271 277 281
EXPLAIN ANALYZE
SELECT number
FROM carmichael_number
WHERE factors @> ARRAY[271, 277, 281]::BIGINT[];

-- 4 primes
-- 29 31 37 41
EXPLAIN ANALYZE
SELECT number
FROM carmichael_number
WHERE factors @> ARRAY[29, 31, 37, 41]::BIGINT[];

-- 107 109 113 127
EXPLAIN ANALYZE
SELECT number
FROM carmichael_number
WHERE factors @> ARRAY[107, 109, 113, 127]::BIGINT[];

-- 5 primes
-- 53 59 61 67 71
EXPLAIN ANALYZE
SELECT number
FROM carmichael_number
WHERE factors @> ARRAY[53, 59, 61, 67, 71]::BIGINT[];

-- 79 83 89 97 101
EXPLAIN ANALYZE
SELECT number
FROM carmichael_number
WHERE factors @> ARRAY[79, 83, 89, 97, 101]::BIGINT[];

-- 2 prime unbalanced
-- 149 19603
EXPLAIN ANALYZE
SELECT number
FROM carmichael_number
WHERE factors @> ARRAY[149, 19603]::BIGINT[];

-- 251 59051
EXPLAIN ANALYZE
SELECT number
FROM carmichael_number
WHERE factors @> ARRAY[251, 59051]::BIGINT[];

-- 3 prime unbalanced
-- 17 197 2749
EXPLAIN ANALYZE
SELECT number
FROM carmichael_number
WHERE factors @> ARRAY[17, 197, 2749]::BIGINT[];

-- 23 401 8009
EXPLAIN ANALYZE
SELECT number
FROM carmichael_number
WHERE factors @> ARRAY[23, 401, 8009]::BIGINT[];