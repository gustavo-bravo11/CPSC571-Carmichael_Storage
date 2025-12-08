// ONLY FOR TESTING ENTIRELY VIBE CODED
// Connects to database and performs some tests

const { Client } = require('pg');
require('dotenv').config({ path: '../../.env' }); // Load from project root

class PSQLClient {
    constructor(config = {}) {
        this.config = {
            host: config.host || process.env.HOST,
            database: config.database || process.env.DATABASE,
            user: config.user || process.env.PQ_USER,
            password: config.password || process.env.PQ_USER_PASSWORD || '',
            port: config.port || process.env.PQ_PORT || 5432,
        };

        this._validateConnection();
        this.client = null;
    }

    _validateConnection() {
        const required = ['host', 'database', 'user', 'port'];
        const missing = required.filter(param => !this.config[param]);

        if (missing.length > 0) {
            throw new Error(
                `Missing required connection parameters: ${missing.join(', ')}. ` +
                'Provide them as arguments or set environment variables.'
            );
        }
    }

    async connect() {
        try {
            this.client = new Client(this.config);
            await this.client.connect();
            console.log('✓ Database connection established');
            return true;
        } catch (error) {
            console.error('✗ Connection error:', error.message);
            throw error;
        }
    }

    async disconnect() {
        if (this.client) {
            await this.client.end();
            console.log('✓ Database connection closed');
        }
    }

    async executeQuery(query, params = []) {
        try {
            const result = await this.client.query(query, params);
            return result.rows;
        } catch (error) {
            console.error('✗ Query execution error:', error.message);
            throw error;
        }
    }

    async executeMultipleQueries(queries) {
        const results = [];
        for (const query of queries) {
            const result = await this.executeQuery(query);
            results.push(result);
        }
        return results;
    }

    async tableExists(tableName) {
        const query = `
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = $1
            );
        `;
        const result = await this.executeQuery(query, [tableName]);
        return result[0].exists;
    }

    async getTableSchema(tableName) {
        const query = `
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = $1
            ORDER BY ordinal_position;
        `;
        return await this.executeQuery(query, [tableName]);
    }

    async getRowCount(tableName) {
        const query = `SELECT COUNT(*) FROM ${tableName};`;
        const result = await this.executeQuery(query);
        return parseInt(result[0].count);
    }
}

// Test script
async function runTests() {
    console.log('='.repeat(60));
    console.log('PostgreSQL Connection Test');
    console.log('='.repeat(60));
    
    // Debug: Show what environment variables were loaded
    console.log('\nEnvironment variables loaded:');
    console.log('  HOST:', process.env.HOST || '(not set)');
    console.log('  DATABASE:', process.env.DATABASE || '(not set)');
    console.log('  PQ_USER:', process.env.PQ_USER || '(not set)');
    console.log('  PQ_USER_PASSWORD:', process.env.PQ_USER_PASSWORD ? '***' : '(not set)');
    console.log('  PQ_PORT:', process.env.PQ_PORT || '(not set)');
    console.log();

    const db = new PSQLClient();

    try {
        // Connect
        await db.connect();
        console.log();

        // Test 1: Simple query
        console.log('Test 1: Current timestamp');
        console.log('-'.repeat(60));
        const timeResult = await db.executeQuery('SELECT NOW() as current_time;');
        console.log('Current time:', timeResult[0].current_time);
        console.log();

        // Test 2: Database version
        console.log('Test 2: PostgreSQL version');
        console.log('-'.repeat(60));
        const versionResult = await db.executeQuery('SELECT version();');
        console.log(versionResult[0].version.substring(0, 50) + '...');
        console.log();

        // Test 3: List all tables
        console.log('Test 3: List all tables in database');
        console.log('-'.repeat(60));
        const tablesQuery = `
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        `;
        const tables = await db.executeQuery(tablesQuery);
        if (tables.length > 0) {
            console.log('Tables found:');
            tables.forEach(table => console.log(`  - ${table.table_name}`));
        } else {
            console.log('No tables found in public schema');
        }
        console.log();

        // Test 4: Check if specific table exists
        console.log('Test 4: Check if table exists');
        console.log('-'.repeat(60));
        const testTableName = 'carmichael_number'; // Your table name
        const exists = await db.tableExists(testTableName);
        console.log(`Table '${testTableName}' exists: ${exists}`);
        console.log();

        // Test 5: If table exists, get schema and row count
        if (exists) {
            console.log(`Test 5: Schema for '${testTableName}'`);
            console.log('-'.repeat(60));
            const schema = await db.getTableSchema(testTableName);
            console.log('Columns:');
            schema.forEach(col => {
                console.log(`  ${col.column_name} (${col.data_type}) ${col.is_nullable === 'YES' ? 'NULL' : 'NOT NULL'}`);
            });
            console.log();

            console.log(`Test 6: Row count for '${testTableName}'`);
            console.log('-'.repeat(60));
            const count = await db.getRowCount(testTableName);
            console.log(`Total rows: ${count}`);
            console.log();

            // Test 7: Sample data from table
            if (count > 0) {
                console.log(`Test 7: Sample data from '${testTableName}'`);
                console.log('-'.repeat(60));
                const sampleQuery = `SELECT * FROM ${testTableName} LIMIT 3;`;
                const sampleData = await db.executeQuery(sampleQuery);
                console.log(JSON.stringify(sampleData, null, 2));
                console.log();
            }
        }

        // Test 8: Multiple queries
        console.log('Test 8: Execute multiple queries');
        console.log('-'.repeat(60));
        const multiResults = await db.executeMultipleQueries([
            'SELECT 1 + 1 as sum;',
            'SELECT 10 * 5 as product;',
            'SELECT CURRENT_DATE as today;'
        ]);
        console.log('Sum:', multiResults[0][0].sum);
        console.log('Product:', multiResults[1][0].product);
        console.log('Today:', multiResults[2][0].today);
        console.log();

        console.log('='.repeat(60));
        console.log('✓ All tests completed successfully!');
        console.log('='.repeat(60));

    } catch (error) {
        console.error('✗ Test failed:', error.message);
        console.error(error.stack);
        process.exit(1);
    } finally {
        await db.disconnect();
    }
}

// Run tests if this file is executed directly
if (require.main === module) {
    runTests().catch(console.error);
}

// Export for use in other files
module.exports = PSQLClient;