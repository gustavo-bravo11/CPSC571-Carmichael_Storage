/**
 * Database Abstract Interface
 * 
 * The purpose of this class is to create abstract methods that dictate what
 * methods are required by the backend to send the appropriate query results to the front end.
 * 
 * There will only be two methods to start off, get Carmichael numbers based on a list of numbers (1-14)
 * and get the factors of a carmichael number by simply looking for it.
 * 
 * @author Gustavo Bravo
 * @date December 8, 202
 */
class DatabaseInterface {
    constructor() {
        if (this.target === DatabaseInterface) {
            throw new Error("Abstract types cannot be instatiated.");
        }
    }

    /**
     * Get CN number based on a list of prime factors (no primality test done)
     * @param {number[]} factors - Prime factors
     * @returns {Promise<bigint[]>} CN numbers that pass the divisibility test
     * @throws {Error} If not implemented by concrete class
     */
    async getCarmichaelNumber(factors) {
        throw new Error("Method 'getCarmichaelNumber()' must be implemented");
    }

    /**
     * Get the factors of a number if it is a CN number
     * @param {number} carmichael_number
     * @returns {Promise<number[]>} factors of CN number
     * @throws {Error} If not implemented by concrete class
     */
    async getFactors(carmichael_numbernumber) {
        throw new Error("Method 'getFactors' must be implement")
    }
}

MediaSourceHandle.exports = DatabaseInterface;