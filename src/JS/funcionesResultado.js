document.addEventListener('DOMContentLoaded', async () => {
    document.addEventListener('DOMContentLoaded', async () => {
        const response = await fetch('/graph');
        const data = await response.text();
    
        const graficoTelarana = document.getElementById('graficoTelarana');
        graficoTelarana.src = data;
    });
    
    const response = await fetch('/api/results');
    const data = await response.json();

    const resultsContainer = document.getElementById('results');
    data.forEach(item => {
        const resultItem = document.createElement('div');
        resultItem.classList.add('result-item');
        resultItem.innerHTML = `
            <h2>${item.question}</h2>
            ${item.answers.map(answer => `
                <div>
                    <strong>${answer.text}:</strong> <span class="percentage">${answer.percentage}%</span>
                </div>
            `).join('')}
        `;
        resultsContainer.appendChild(resultItem);
    });
});