/**
 * Script for Carmichael DB Frontend
 * 
 * This file houses all of the functionality for the CN DB including:
 * - Event Listeners that read the user input, waiting for either a button
 *      click or pressing the enter button when in a text box.
 * - Fetch API calls, use the API_BASE_URL to call the api and await for
 *      the objects, handling the response and giving appropriate responses
 *      to the user.
 * - Navigation, based on the user click, hide or show the sections.
 * 
 * @author Gustavo Bravo
 * @date December 13, 2025
 */
const API_BASE_URL = 'https://thomas.butler.edu:5433'

// API Calls

/**
 * Fetch Carmichael Numbers from the API. Uses the API
 * link constant above to call and yield the carmichael numbers
 * passing that divisibility test.
 * @param {Number[]} factors - factors checking for divisibility
 * @param {Number} page - The page we are seeing
 * @param {Number} limit - The max amount of items to see in one page
 * @returns {Promise<Object|null>} data from the API call
 * @throws {Error} If HTTP call fails
 */
async function fetchCarmichaelNumber(factors, page=1, limit=100) {
    const baseUrl = `${API_BASE_URL}/api/carmichael_number`;
    const params = new URLSearchParams({
        factors: factors.join(','),
        page: page,
        limit: limit
    });

    try {
        const response = await fetch(`${baseUrl}?${params.toString()}`);
        if (!response.ok) throw new Error('HTTP error status:', response.status);

        const data = await response.json();
        return data;

    } catch (error) {
        console.error(
            'Failed to fetch Carmichael Number ' + 
            `with the factors: ${factors.toString()}. \n` +
            `Error: ${error}`
        );
        return null;
    }
}

/**
 * Get the factors for a carmichael number from the API
 * @param {Number} number - The carmichael number we are querying for
 * @returns {Promise<Object|null>} The API response object, null if failed
 * @throws {Error} If the HTTP request fails
 */
async function fetchFactors(number) {
    const baseUrl = `${API_BASE_URL}/api/numbers`;
    try {
        const response = await fetch(`${baseUrl}?number=${number.toString()}`)
        if (!response.ok) throw new Error('HTTP error status:', response.status);

        const data = await response.json();
        return data;
    } catch (error) {
        console.error(
            'Failed to fetch prime factors ' + 
            `for the Carmichael Number: ${number.toString()}. \n` +
            `Error: ${error}`
        );
        return null;
    }
}

// Page Functionality

// Nav Bar click handling
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.main-nav a');
    const sections = document.querySelectorAll('section');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
    
            const targedID = link.getAttribute('href').substring(1)
    
            // Switch all sections to be hidden
            sections.forEach(section => {
                section.classList.add('hidden');
            });
    
            document.getElementById(targedID).classList.remove('hidden');
    
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });
}

// Page Handling
function initializeDivisibility() {
    const searchBtn = document.querySelector('#divisibility .search-btn');
    const resultContainer = document.querySelector('#divisibility .result-container');

    // Add click event
    searchBtn.addEventListener('click', async function() {
        const inputs = document.querySelectorAll('#divisibility .number-input');
        const factors = Array.from(inputs)
            .map(input => input.value.trim())
            .filter(value => value !== '')
            .map(value => parseInt(value));

        if (factors.length === 0) {
            alert('Please add at least one factor');
            return;
        }

        resultContainer.classList.remove('hidden');
        resultContainer.innerHTML = '<p>Loading results...</p>';

        const data = await fetchCarmichaelNumber(factors);

        if (data && data.success) {
            displayCarmichaelResults(data, factors);
        } else {
            resultContainer.innerHTML =
                '<p>Error Retrieving Results. Is the server running?';
        }
    });

}

// Helper Functions
function displayCarmichaelResults(data, factors) {
    const resultContainer = document.querySelector('#divisibility .result-container');

    if (data.total === 0) {
        resultContainer.innerHTML =
            `<p>The factors ${factors.toString()} did not pass the divisibility test.</p>`;
        return;
    }

    let html = `
        <div class="results-header">
            <p>
                Showing ${data.count} of ${data.total} results 
                (Page ${data.page} of ${data.totalPages})
            </p>
        </div>
        <ul class="result-list">
    `;

    data.data.forEach(number => {
        html += `<li>${number}</li>`
    });

    html += '</li>';

    resultContainer.innerHTML = html;
}

// Document Wrapper
document.addEventListener('DOMContentLoaded', async function() {
    initializeNavigation();
    initializeDivisibility();
});