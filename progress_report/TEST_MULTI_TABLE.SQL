-- Query with 1 prime (search tables 3-14)
-- 5
EXPLAIN ANALYZE
SELECT number FROM carmichael_number_3 WHERE factors @> ARRAY[5]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_4 WHERE factors @> ARRAY[5]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_5 WHERE factors @> ARRAY[5]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_6 WHERE factors @> ARRAY[5]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_7 WHERE factors @> ARRAY[5]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_8 WHERE factors @> ARRAY[5]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_9 WHERE factors @> ARRAY[5]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_10 WHERE factors @> ARRAY[5]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_11 WHERE factors @> ARRAY[5]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_12 WHERE factors @> ARRAY[5]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_13 WHERE factors @> ARRAY[5]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_14 WHERE factors @> ARRAY[5]::BIGINT[];

-- 14348909
EXPLAIN ANALYZE
SELECT number FROM carmichael_number_3 WHERE factors @> ARRAY[14348909]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_4 WHERE factors @> ARRAY[14348909]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_5 WHERE factors @> ARRAY[14348909]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_6 WHERE factors @> ARRAY[14348909]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_7 WHERE factors @> ARRAY[14348909]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_8 WHERE factors @> ARRAY[14348909]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_9 WHERE factors @> ARRAY[14348909]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_10 WHERE factors @> ARRAY[14348909]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_11 WHERE factors @> ARRAY[14348909]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_12 WHERE factors @> ARRAY[14348909]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_13 WHERE factors @> ARRAY[14348909]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_14 WHERE factors @> ARRAY[14348909]::BIGINT[];

-- 2 Primes (search tables 3-14, must have at least 2 factors)
-- 11 13
EXPLAIN ANALYZE
SELECT number FROM carmichael_number_3 WHERE factors @> ARRAY[11, 13]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_4 WHERE factors @> ARRAY[11, 13]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_5 WHERE factors @> ARRAY[11, 13]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_6 WHERE factors @> ARRAY[11, 13]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_7 WHERE factors @> ARRAY[11, 13]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_8 WHERE factors @> ARRAY[11, 13]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_9 WHERE factors @> ARRAY[11, 13]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_10 WHERE factors @> ARRAY[11, 13]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_11 WHERE factors @> ARRAY[11, 13]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_12 WHERE factors @> ARRAY[11, 13]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_13 WHERE factors @> ARRAY[11, 13]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_14 WHERE factors @> ARRAY[11, 13]::BIGINT[];

-- 21871 21881
EXPLAIN ANALYZE
SELECT number FROM carmichael_number_3 WHERE factors @> ARRAY[21871, 21881]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_4 WHERE factors @> ARRAY[21871, 21881]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_5 WHERE factors @> ARRAY[21871, 21881]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_6 WHERE factors @> ARRAY[21871, 21881]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_7 WHERE factors @> ARRAY[21871, 21881]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_8 WHERE factors @> ARRAY[21871, 21881]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_9 WHERE factors @> ARRAY[21871, 21881]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_10 WHERE factors @> ARRAY[21871, 21881]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_11 WHERE factors @> ARRAY[21871, 21881]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_12 WHERE factors @> ARRAY[21871, 21881]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_13 WHERE factors @> ARRAY[21871, 21881]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_14 WHERE factors @> ARRAY[21871, 21881]::BIGINT[];

-- 3 Primes (search tables 3-14)
-- 11 13 17
EXPLAIN ANALYZE
SELECT number FROM carmichael_number_3 WHERE factors @> ARRAY[11, 13, 17]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_4 WHERE factors @> ARRAY[11, 13, 17]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_5 WHERE factors @> ARRAY[11, 13, 17]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_6 WHERE factors @> ARRAY[11, 13, 17]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_7 WHERE factors @> ARRAY[11, 13, 17]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_8 WHERE factors @> ARRAY[11, 13, 17]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_9 WHERE factors @> ARRAY[11, 13, 17]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_10 WHERE factors @> ARRAY[11, 13, 17]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_11 WHERE factors @> ARRAY[11, 13, 17]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_12 WHERE factors @> ARRAY[11, 13, 17]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_13 WHERE factors @> ARRAY[11, 13, 17]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_14 WHERE factors @> ARRAY[11, 13, 17]::BIGINT[];

-- 271 277 281
EXPLAIN ANALYZE
SELECT number FROM carmichael_number_3 WHERE factors @> ARRAY[271, 277, 281]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_4 WHERE factors @> ARRAY[271, 277, 281]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_5 WHERE factors @> ARRAY[271, 277, 281]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_6 WHERE factors @> ARRAY[271, 277, 281]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_7 WHERE factors @> ARRAY[271, 277, 281]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_8 WHERE factors @> ARRAY[271, 277, 281]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_9 WHERE factors @> ARRAY[271, 277, 281]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_10 WHERE factors @> ARRAY[271, 277, 281]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_11 WHERE factors @> ARRAY[271, 277, 281]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_12 WHERE factors @> ARRAY[271, 277, 281]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_13 WHERE factors @> ARRAY[271, 277, 281]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_14 WHERE factors @> ARRAY[271, 277, 281]::BIGINT[];

-- 4 primes (search tables 4-14)
-- 29 31 37 41
EXPLAIN ANALYZE
SELECT number FROM carmichael_number_4 WHERE factors @> ARRAY[29, 31, 37, 41]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_5 WHERE factors @> ARRAY[29, 31, 37, 41]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_6 WHERE factors @> ARRAY[29, 31, 37, 41]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_7 WHERE factors @> ARRAY[29, 31, 37, 41]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_8 WHERE factors @> ARRAY[29, 31, 37, 41]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_9 WHERE factors @> ARRAY[29, 31, 37, 41]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_10 WHERE factors @> ARRAY[29, 31, 37, 41]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_11 WHERE factors @> ARRAY[29, 31, 37, 41]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_12 WHERE factors @> ARRAY[29, 31, 37, 41]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_13 WHERE factors @> ARRAY[29, 31, 37, 41]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_14 WHERE factors @> ARRAY[29, 31, 37, 41]::BIGINT[];

-- 107 109 113 127
EXPLAIN ANALYZE
SELECT number FROM carmichael_number_4 WHERE factors @> ARRAY[107, 109, 113, 127]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_5 WHERE factors @> ARRAY[107, 109, 113, 127]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_6 WHERE factors @> ARRAY[107, 109, 113, 127]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_7 WHERE factors @> ARRAY[107, 109, 113, 127]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_8 WHERE factors @> ARRAY[107, 109, 113, 127]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_9 WHERE factors @> ARRAY[107, 109, 113, 127]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_10 WHERE factors @> ARRAY[107, 109, 113, 127]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_11 WHERE factors @> ARRAY[107, 109, 113, 127]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_12 WHERE factors @> ARRAY[107, 109, 113, 127]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_13 WHERE factors @> ARRAY[107, 109, 113, 127]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_14 WHERE factors @> ARRAY[107, 109, 113, 127]::BIGINT[];

-- 5 primes (search tables 5-14)
-- 53 59 61 67 71
EXPLAIN ANALYZE
SELECT number FROM carmichael_number_5 WHERE factors @> ARRAY[53, 59, 61, 67, 71]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_6 WHERE factors @> ARRAY[53, 59, 61, 67, 71]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_7 WHERE factors @> ARRAY[53, 59, 61, 67, 71]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_8 WHERE factors @> ARRAY[53, 59, 61, 67, 71]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_9 WHERE factors @> ARRAY[53, 59, 61, 67, 71]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_10 WHERE factors @> ARRAY[53, 59, 61, 67, 71]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_11 WHERE factors @> ARRAY[53, 59, 61, 67, 71]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_12 WHERE factors @> ARRAY[53, 59, 61, 67, 71]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_13 WHERE factors @> ARRAY[53, 59, 61, 67, 71]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_14 WHERE factors @> ARRAY[53, 59, 61, 67, 71]::BIGINT[];

-- 79 83 89 97 101
EXPLAIN ANALYZE
SELECT number FROM carmichael_number_5 WHERE factors @> ARRAY[79, 83, 89, 97, 101]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_6 WHERE factors @> ARRAY[79, 83, 89, 97, 101]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_7 WHERE factors @> ARRAY[79, 83, 89, 97, 101]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_8 WHERE factors @> ARRAY[79, 83, 89, 97, 101]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_9 WHERE factors @> ARRAY[79, 83, 89, 97, 101]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_10 WHERE factors @> ARRAY[79, 83, 89, 97, 101]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_11 WHERE factors @> ARRAY[79, 83, 89, 97, 101]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_12 WHERE factors @> ARRAY[79, 83, 89, 97, 101]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_13 WHERE factors @> ARRAY[79, 83, 89, 97, 101]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_14 WHERE factors @> ARRAY[79, 83, 89, 97, 101]::BIGINT[];

-- 2 prime unbalanced (search tables 3-14)
-- 149 19603
EXPLAIN ANALYZE
SELECT number FROM carmichael_number_3 WHERE factors @> ARRAY[149, 19603]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_4 WHERE factors @> ARRAY[149, 19603]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_5 WHERE factors @> ARRAY[149, 19603]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_6 WHERE factors @> ARRAY[149, 19603]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_7 WHERE factors @> ARRAY[149, 19603]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_8 WHERE factors @> ARRAY[149, 19603]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_9 WHERE factors @> ARRAY[149, 19603]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_10 WHERE factors @> ARRAY[149, 19603]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_11 WHERE factors @> ARRAY[149, 19603]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_12 WHERE factors @> ARRAY[149, 19603]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_13 WHERE factors @> ARRAY[149, 19603]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_14 WHERE factors @> ARRAY[149, 19603]::BIGINT[];

-- 251 59051
EXPLAIN ANALYZE
SELECT number FROM carmichael_number_3 WHERE factors @> ARRAY[251, 59051]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_4 WHERE factors @> ARRAY[251, 59051]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_5 WHERE factors @> ARRAY[251, 59051]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_6 WHERE factors @> ARRAY[251, 59051]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_7 WHERE factors @> ARRAY[251, 59051]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_8 WHERE factors @> ARRAY[251, 59051]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_9 WHERE factors @> ARRAY[251, 59051]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_10 WHERE factors @> ARRAY[251, 59051]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_11 WHERE factors @> ARRAY[251, 59051]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_12 WHERE factors @> ARRAY[251, 59051]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_13 WHERE factors @> ARRAY[251, 59051]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_14 WHERE factors @> ARRAY[251, 59051]::BIGINT[];

-- 3 prime unbalanced (search tables 3-14)
-- 17 197 2749
EXPLAIN ANALYZE
SELECT number FROM carmichael_number_3 WHERE factors @> ARRAY[17, 197, 2749]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_4 WHERE factors @> ARRAY[17, 197, 2749]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_5 WHERE factors @> ARRAY[17, 197, 2749]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_6 WHERE factors @> ARRAY[17, 197, 2749]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_7 WHERE factors @> ARRAY[17, 197, 2749]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_8 WHERE factors @> ARRAY[17, 197, 2749]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_9 WHERE factors @> ARRAY[17, 197, 2749]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_10 WHERE factors @> ARRAY[17, 197, 2749]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_11 WHERE factors @> ARRAY[17, 197, 2749]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_12 WHERE factors @> ARRAY[17, 197, 2749]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_13 WHERE factors @> ARRAY[17, 197, 2749]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_14 WHERE factors @> ARRAY[17, 197, 2749]::BIGINT[];

-- 23 401 8009
EXPLAIN ANALYZE
SELECT number FROM carmichael_number_3 WHERE factors @> ARRAY[23, 401, 8009]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_4 WHERE factors @> ARRAY[23, 401, 8009]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_5 WHERE factors @> ARRAY[23, 401, 8009]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_6 WHERE factors @> ARRAY[23, 401, 8009]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_7 WHERE factors @> ARRAY[23, 401, 8009]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_8 WHERE factors @> ARRAY[23, 401, 8009]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_9 WHERE factors @> ARRAY[23, 401, 8009]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_10 WHERE factors @> ARRAY[23, 401, 8009]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_11 WHERE factors @> ARRAY[23, 401, 8009]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_12 WHERE factors @> ARRAY[23, 401, 8009]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_13 WHERE factors @> ARRAY[23, 401, 8009]::BIGINT[]
UNION ALL
SELECT number FROM carmichael_number_14 WHERE factors @> ARRAY[23, 401, 8009]::BIGINT[];