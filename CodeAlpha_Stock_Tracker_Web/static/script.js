document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const tickerSelect = document.getElementById('tickerSelect');
    const marketList = document.getElementById('marketList');
    const addStockForm = document.getElementById('addStockForm');
    const quantityInput = document.getElementById('quantityInput');
    const formError = document.getElementById('formError');
    const portfolioBody = document.getElementById('portfolioBody');
    const totalInvestmentEl = document.getElementById('totalInvestment');
    const resetBtn = document.getElementById('resetBtn');

    // Format currency
    const formatCurrency = (value) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(value);
    };

    // Initialize App
    async function init() {
        await loadMarketData();
        await loadPortfolio();
    }

    // Fetch and populate available stocks
    async function loadMarketData() {
        try {
            const res = await fetch('/api/stocks');
            const stocks = await res.json();
            
            tickerSelect.innerHTML = '<option value="" disabled selected>Select an asset</option>';
            marketList.innerHTML = '';
            
            for (const [ticker, price] of Object.entries(stocks)) {
                // Add to select dropdown
                const option = document.createElement('option');
                option.value = ticker;
                option.textContent = `${ticker} - ${formatCurrency(price)}`;
                tickerSelect.appendChild(option);
                
                // Add to market list
                const li = document.createElement('li');
                li.innerHTML = `<span>${ticker}</span><span class="price">${formatCurrency(price)}</span>`;
                marketList.appendChild(li);
            }
        } catch (error) {
            console.error("Failed to load market data", error);
        }
    }

    // Fetch and render portfolio
    async function loadPortfolio() {
        try {
            const res = await fetch('/api/portfolio');
            const data = await res.json();
            renderPortfolio(data);
        } catch (error) {
            console.error("Failed to load portfolio", error);
        }
    }

    // Render the portfolio table
    function renderPortfolio(data) {
        portfolioBody.innerHTML = '';
        
        // Update Total
        totalInvestmentEl.textContent = formatCurrency(data.total_investment);
        
        if (data.holdings.length === 0) {
            portfolioBody.innerHTML = `
                <tr id="emptyStateRow">
                    <td colspan="5" class="empty-state">No assets in portfolio. Execute a trade to get started!</td>
                </tr>
            `;
            return;
        }
        
        data.holdings.forEach(holding => {
            const tr = document.createElement('tr');
            tr.className = 'highlight-row';
            
            tr.innerHTML = `
                <td><span class="asset-name">${holding.ticker}</span></td>
                <td class="text-right">${holding.quantity.toFixed(2)}</td>
                <td class="text-right asset-price">${formatCurrency(holding.price)}</td>
                <td class="text-right asset-value">${formatCurrency(holding.value)}</td>
                <td class="text-center">
                    <button class="btn btn-small remove-btn" data-ticker="${holding.ticker}">Sell</button>
                </td>
            `;
            
            portfolioBody.appendChild(tr);
        });
        
        // Add event listeners to remove buttons
        document.querySelectorAll('.remove-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const ticker = e.target.getAttribute('data-ticker');
                await removeStock(ticker);
            });
        });
    }

    // Handle form submit
    addStockForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        formError.classList.add('hidden');
        
        const ticker = tickerSelect.value;
        const quantity = quantityInput.value;
        
        if (!ticker) {
            showError("Please select an asset");
            return;
        }
        
        try {
            const res = await fetch('/api/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ticker, quantity })
            });
            
            if (!res.ok) {
                const errorData = await res.json();
                showError(errorData.error || "Failed to add stock");
                return;
            }
            
            const data = await res.json();
            renderPortfolio(data);
            
            // Reset form
            quantityInput.value = '';
            tickerSelect.value = '';
            
        } catch (error) {
            showError("Network error occurred");
        }
    });

    // Remove a stock
    async function removeStock(ticker) {
        try {
            const res = await fetch('/api/remove', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ticker })
            });
            
            const data = await res.json();
            renderPortfolio(data);
        } catch (error) {
            console.error("Failed to remove stock", error);
        }
    }

    // Reset portfolio
    resetBtn.addEventListener('click', async () => {
        if (!confirm("Are you sure you want to clear your entire portfolio?")) return;
        
        try {
            const res = await fetch('/api/reset', { method: 'POST' });
            const data = await res.json();
            renderPortfolio(data);
        } catch (error) {
            console.error("Failed to reset portfolio", error);
        }
    });

    function showError(msg) {
        formError.textContent = msg;
        formError.classList.remove('hidden');
    }

    // Boot
    init();
});
