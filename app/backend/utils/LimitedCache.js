/**
 * This class creates a map that is limited by its size.
 * The goal of creating a cache like this is to prevent the server from
 * craching by making the map too big. A cache is also used to improve the
 * user experience. If a user runs the same query back to back, the cache will be able
 * to find it and return the results immediatly. This also allows for paginated results
 * to work seemlessly.
 * 
 * @param max_size: The max (estimated) size in bytes allowed for the cache map.
 * @author Gustavo Bravo
 * @Date December 9, 2025
 */
class LimitedCache {
    constructor(max_size) {
        this.max_size = max_size;
        this.cache = new Map();
        this.current_size = 0;
    }

    /**
     * Estimate the size by using a factor of 100 based on each element in the array.
     * @param {String[]} data - A string array representing query results.
     * @returns The length as a number.
     */
    #estimateSize(data_array) {
        return data_array.length * 100;
    }

    /**
     * Return a value from the cache based on a key.
     * Uses Last Recently Used, so the LRU is always pushed to the front.
     * @param {String} key - Represent a list of factors joined together.
     * @returns The data in the cache - The query results stored in cache.
     */
    get(key) {
        if (!this.cache.has(key)) return undefined;

        // PUSH the latest retrieved to the front of the map
        const entry = this.cache.get(key);
        this.cache.delete(key);
        this.cache.set(key, entry);

        return entry.data;
    }

    /**
     * Add data to the cache, uses the estimated size to `kick` members
     * out of the map. Using the LRU startegy explained in the get method.
     * We remove the last element in the map, this is the oldest element.
     * @param {String} key - Cache key, the numbers being queried
     * @param {*} data - The results of the query
     */
    set(key, data) {
        const size = this.#estimateSize(data);

        if (size > this.max_size) {
            console.log(`Entry ${key} results are too big to fit in the cache.`);
            return;
        }

        // If the key is already here, we have to move it back to the top
        // So we remove it here.
        if (this.cache.has(key)) {
            const old = this.cache.get(key);
            this.current_size -= old.size;
            this.cache.delete(key);
        }

        // Remove any members necessary for the new item to fit in the cache
        while (this.current_size + size > this.max_size && this.cache.size > 0) {
            const oldest = this.cache.keys().next().value;
            const entry = this.cache.get(oldest);
            this.current_size -= entry.size;
            this.cache.delete(oldest);
            console.log(`Evicted ${oldest} from cache.`);
        }

        this.cache.set(key, { data, size });
        this.current_size += size;
        console.log(`Cached results for ${key}.`)
    }

    /**
     * Check the map to see if the element is in there already.
     * @param {String} key - Cache key
     * @returns {boolean}
     */
    has(key) {
        return this.cache.has(key);
    }
}

module.exports = LimitedCache;