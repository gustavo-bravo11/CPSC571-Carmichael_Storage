/**
 * Database Abstract Interface
 * 
 * The purpose of this class is to create abstract methods that dictate what
 * methods are required by the backend to send the appropriate query results to the front end.
 * 
 * There will only be two methods to start off, get Carmichael numbers based on a list of numbers (1-14)
 * and get the factors of a carmichael number by simply looking for it.
 * 
 * For safety, we have to concern ourselves with SQL injection, as our final DB my be a SQL database.
 */