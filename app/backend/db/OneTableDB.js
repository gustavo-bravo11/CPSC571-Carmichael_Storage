/**
 * Concrete implementation of abstract class DatabaseInterface for
 * the OneTable Schema in the Carmichael Database.
 * 
 * Along with implementing the methods from DatabaseInterface, we
 * will have to concern ourselves with loading our .env, and SQL 
 * injection prevention.
 * 
 * @author Gustavo Bravo
 * @date December 8th
 */

const DatabaseInterface = require('./DatabaseInterface');
const pg = require('pg');
const { Pool} = pg;


class OneTableDB extends DatabaseInterface {
    #pool;

    constructor(config) {
        super();
        this.#pool = new Pool(config);
    }

    /**
     * Get the CN, convert to string array of just numbers, and return
     * @param {Number[]} factors - Prime factors to perform divisibility test on.
     * @returns {Promise<String[]>} result - The results CN or empty if no matches.
     */
    async getCarmichaelNumber(factors) {
        const query = `
            SELECT number
            FROM carmichael_number
            WHERE factors @> $1;
        `;

        const query_result = await this.#pool.query(query, [factors]);
        if (query_result.rows.length === 0) return [];
        
        let cm_numbers = [];
        query_result.rows.forEach((row) => 
            cm_numbers.push(row['number'])
        );
        
        return cm_numbers;
    }

    /**
     * Get the factors of a CN number, empty if not a CN number
     * @param {Number} carmichael_number 
     * @returns {Promise<Number[]>} Array of factors for the CN 
     */
    async getFactors(carmichael_number) {
        const query = `
            SELECT factors
            FROM carmichael_number
            WHERE number = $1
        `;

        const query_result = await this.#pool.query(query, [carmichael_number]);
        if (query_result.rows.length === 0) return [];

        return query_result.rows[0]['factors'].map(x => Number(x));
    }

    /**
     * Disconnect the database instatiated in the constructor
     */
    async disconnect() {
        await this.#pool.end();
    }
}

module.exports = OneTableDB;

// TEST METHODS FOR DEVELOPMENT
// async function testerMethod() {
//     if (require.main === module) {
//         console.log("Testing OneTable Implementation...");
//         try {
//             const config = {
//                 user: process.env.PQ_USER,
//                 password: process.env.PQ_USER_PASSWORD,
//                 host: process.env.HOST,
//                 port: process.env.PQ_PORT,
//                 database: process.env.DATABASE,
//             }
//             const db = new OneTableDB(config);
//             const query = await db.getFactors('561');

//             // const query = await db.getCarmichaelNumber([
                // 4
                // 11, 37, 61,
                // 97, 163, 173,
                // 211, 1483, 4297, 7741
                // 11,37,61,97,163,173,211,1483,4297,7741
//             // ]);

//             console.log(query);
//             db.disconnect();

//         } catch (error) {
//             console.log("Threw error:", error.message);
//         }
//     }
// }

// testerMethod();