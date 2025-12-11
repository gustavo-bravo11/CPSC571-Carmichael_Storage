/**
 * Main entry point using express.js
 * Create a server to host the backend queries and return from the database.
 * 
 * This server will implement a class that inherits from DatabaseInterface
 * into a concrete object. This is done so the methods are always the same
 * even if the implementation of the database changes.
 * 
 * As it's running on the butler servers, the endpoint can always
 * be found at http://thomas.butler.edu:<PORT>/<API-ENDPOINT>.
 * 
 * This file must be in the same directory as /db, /utils, and .env.
 * 
 * Note: The caching implementing here is on the SERVE SIDE, which
 * is not best practice. However, in this project, we are not expecting
 * thouasands of users, so it's fine for now and we will refactor
 * after the deadline. 
 * 
 * Usage:
 *  `node server.js`
 * 
 * @author Gustavo Bravo
 * @date December 9, 2025
 * 
 */
require('dotenv').config({ path: './.env'});

const DBInterface = require('./db/OneTableDB');
const db = new DBInterface({
    user: process.env.PQ_USER,
    password: process.env.PQ_USER_PASSWORD,
    host: process.env.HOST,
    port: process.env.PQ_PORT,
    database: process.env.DATABASE,
});

const MAX_CACHE_SIZE = 5 * 1024 * 1024 * 1024           // 5GB Cache
const LimitedCache = require('./utils/LimitedCache');
const query_cache = new LimitedCache(MAX_CACHE_SIZE);

const express = require ('express');
const app = express();
const port = process.env.WEB_PORT;


// Helper functions

// Validate that the query input is indeed a string
function validateStringInput(input) {
    return (input && typeof(input) === 'string');
}

/**
 * Ensure the factors being passed in are positive numbers.
 * Checks type, and then checks if its a positive number.
 * @param {String} input_string - Contains numbers on a list separated by ','
 * @returns {Number[]} Passed to the database for querying
 * @throws {Error} If the function fails to validate
 */
function validateFactorArray(input_string) {
    if (!validateStringInput(input_string)) {
        throw new Error("Invalid 'factors' parameter");
    }

    const string_array = input_string.split(',');
    const factors = [];

    for (const s of string_array) {
        const factor = Number(s);

        if (!Number.isInteger(factor) || factor < 1)
            throw new Error(`Not a positive integer '${s}' parameter`);
        factors.push(factor);
    }

    return factors;
}

// Middleware
app.use(express.json());

app.use((req, res, next) => {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] ${req.method} request on ${req.url}`);
    next();
});

// API Endpoints

/**
 * Get Carmichael Numbers API Endpoint
 * Expects request query with the following parameters:
 *      - factors: A list of factors separated by a comma.
 *      - page: The current page number to return for the paginated report.
 *      - limit: The max number of numbers to display on the page (max is 100).
 * 
 * Example api urls:
 * 
 * Query for numbers with factors 17, 19, 20
 *  Page 1
 *  Limit 50
 * http://thomas.butler.edu:5433/api/carmichael_number?factors=17,19,23&page=1&limit=50
 * 
 * Query for numbers with factors 37, 61, 97, 163, 173, 211
 *  Page 1
 *  Limit 100
 * http://thomas.butler.edu:5433/api/carmichael_number?factors=37,61,97,163,173,211&page=1&limit=200
 * 
 */
app.get('/api/carmichael_number', async (req, res) => {
    try {
        const factors = validateFactorArray(req.query.factors?.trim());
        const cache_key = factors.sort((a, b) => a - b).join(',');

        // Check cache
        let all_results;
        if (query_cache.has(cache_key)) {
            console.log(`Cache HIT for factors: ${cache_key}`);
            all_results = query_cache.get(cache_key);
        } else { // Query if not in cache.
            console.log(`Cache MISS for factors: ${cache_key}`);
            all_results = await db.getCarmichaelNumber(factors);
            query_cache.set(cache_key, all_results);
        }

        // Paginate results (Don't overwhelm UI)
        const page = parseInt(req.query.page) || 1;
        const limit = Math.min(parseInt(req.query.limit) || 50, 200);
        const start = (page - 1) * limit;
        const end = start + limit;
        const paginated_results = all_results.slice(start, end);

        res.json({
            success: true,
            page: page,
            limit: limit,
            total: all_results.length,
            count: paginated_results.length,
            totalPages: Math.ceil(all_results.length / limit),
            data: paginated_results
        });

    } catch (error) {
        res.status(400).json({
            success: false,
            message: error.message
        });
    }
});

/**
 * Get Prime Factors API Enpoint
 * 
 * Example api urls:
 * http://thomas.butler.edu:5433/api/factors?number=561
 */
app.get('/api/factors', async (req, res) => {
    try {
        const input_string = req.query.number?.trim();
        
        // Validate that its a string and that it only contains number characters
        if (!validateStringInput(input_string)) throw new Error("Not a string 'carmichael number' parameter");
        if (!/^\d+$/.test(input_string)) throw new Error("Non-numeric 'carmichael number' parameter");

        const factors = await db.getFactors(input_string);

        res.json({
            success: true,
            data: factors
        });
    } catch (error) {
        res.status(400).json({
            success: false,
            message: error
        });
    }
});

app.listen(port, () => {
    console.log(`server.js running on port: ${port}`);
});