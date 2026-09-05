// AgriPredict AI Engine Frontend Scaffolding

document.addEventListener('DOMContentLoaded', () => {
    console.log("AgriPredict frontend initialized.");
    
    fetchHealthStatus();
});

async function fetchHealthStatus() {
    const statusCard = document.getElementById('status-card');
    try {
        const response = await fetch('/health');
        const data = await response.json();
        if (statusCard) {
            statusCard.innerHTML = `
                <p>🟢 <strong>Status:</strong> ${data.status}</p>
                <p>⚡ <strong>Service:</strong> ${data.service}</p>
                <p>📦 <strong>Version:</strong> ${data.version}</p>
            `;
        }
    } catch (error) {
        if (statusCard) {
            statusCard.innerHTML = `<p>🔴 <strong>Status:</strong> Error connecting to backend (${error.message})</p>`;
        }
    }
}
