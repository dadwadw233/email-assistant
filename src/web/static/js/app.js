// Global variables
let showProcessed = false;

// DOM elements
const refreshBtn = document.getElementById('refreshBtn');
const showProcessedBtn = document.getElementById('showProcessedBtn');
const configInfo = document.getElementById('configInfo');
const accountsList = document.getElementById('accountsList');
const emailsList = document.getElementById('emailsList');

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    loadConfig();
    loadAccounts();
    loadEmails();
});

refreshBtn.addEventListener('click', () => {
    loadConfig();
    loadAccounts();
    loadEmails();
});

showProcessedBtn.addEventListener('click', () => {
    showProcessed = !showProcessed;
    showProcessedBtn.textContent = showProcessed ? 'Show Unprocessed' : 'Show Processed';
    loadEmails();
});

// Load configuration
async function loadConfig() {
    try {
        const response = await fetch('/api/config');
        const data = await response.json();
        
        if (data.success) {
            const config = data.config;
            configInfo.innerHTML = `
                <p><strong>App Name:</strong> ${config.app_name}</p>
                <p><strong>Version:</strong> ${config.version}</p>
                <p><strong>Log Level:</strong> ${config.log_level}</p>
                <p><strong>Check Interval:</strong> ${config.email_check_interval}s</p>
                <p><strong>Importance Threshold:</strong> ${config.importance_threshold}</p>
            `;
        } else {
            configInfo.innerHTML = `<p class="text-danger">Error loading config: ${data.error}</p>`;
        }
    } catch (error) {
        configInfo.innerHTML = `<p class="text-danger">Error loading config: ${error.message}</p>`;
    }
}

// Load accounts
async function loadAccounts() {
    try {
        const response = await fetch('/api/accounts');
        const data = await response.json();
        
        if (data.success) {
            const accounts = data.accounts;
            if (accounts.length === 0) {
                accountsList.innerHTML = '<p>No accounts configured</p>';
                return;
            }
            
            let html = '<ul class="list-group">';
            accounts.forEach(account => {
                html += `
                    <li class="list-group-item">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <strong>${account.email_address}</strong>
                                <br>
                                <small class="text-muted">${account.imap_server}</small>
                            </div>
                            <span class="badge bg-secondary">Active</span>
                        </div>
                    </li>
                `;
            });
            html += '</ul>';
            accountsList.innerHTML = html;
        } else {
            accountsList.innerHTML = `<p class="text-danger">Error loading accounts: ${data.error}</p>`;
        }
    } catch (error) {
        accountsList.innerHTML = `<p class="text-danger">Error loading accounts: ${error.message}</p>`;
    }
}

// Load emails
async function loadEmails() {
    try {
        const response = await fetch(`/api/emails?processed=${showProcessed}`);
        const data = await response.json();
        
        if (data.success) {
            const emails = data.emails;
            if (emails.length === 0) {
                emailsList.innerHTML = '<p>No emails found</p>';
                return;
            }
            
            let html = '';
            emails.forEach(email => {
                // Determine importance class
                let importanceClass = 'importance-low';
                if (email.importance >= 0.7) {
                    importanceClass = 'importance-high';
                } else if (email.importance >= 0.4) {
                    importanceClass = 'importance-medium';
                }
                
                // Format date
                const date = new Date(email.date).toLocaleString();
                
                html += `
                    <div class="card email-card mb-3 ${importanceClass}">
                        <div class="card-body">
                            <div class="d-flex justify-content-between">
                                <h6 class="card-title">${email.subject}</h6>
                                <span class="badge bg-primary category-badge">${email.category}</span>
                            </div>
                            <h6 class="card-subtitle mb-2 text-muted">From: ${email.from}</h6>
                            <p class="card-text">${email.summary}</p>
                            <div class="d-flex justify-content-between align-items-center">
                                <small class="text-muted">${date}</small>
                                <div>
                                    <span class="badge bg-secondary">Importance: ${email.importance.toFixed(2)}</span>
                                    <span class="badge bg-info">${email.action}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            });
            emailsList.innerHTML = html;
        } else {
            emailsList.innerHTML = `<p class="text-danger">Error loading emails: ${data.error}</p>`;
        }
    } catch (error) {
        emailsList.innerHTML = `<p class="text-danger">Error loading emails: ${error.message}</p>`;
    }
}