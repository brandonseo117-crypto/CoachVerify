function navigateTo(stateId) {
    document.querySelectorAll('.view-state').forEach(state => {
        state.classList.remove('active-state');
    });

    const targetState = document.getElementById(stateId);
    if (targetState) {
        targetState.classList.add('active-state');
    }
}

document.getElementById('auditForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const submitBtn = document.getElementById('submitBtn');
    const payload = {
        profile: document.getElementById('profile').value,
        claim: document.getElementById('claim').value,
        routine: document.getElementById('routine').value
    };

    try {
        navigateTo('state-loader');

        const response = await fetch('/api/audit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('Data drop matrix failed response check');
        const data = await response.json();

        document.getElementById('safetyScore').innerText = data.safety_score;
        document.getElementById('perfScore').innerText = data.performance_score;
        document.getElementById('matchedPaper').innerText = data.matched_paper;
        document.getElementById('translationText').innerText = data.translated_consensus;

        const safetyCard = document.getElementById('safetyCard');
        if (safetyCard) {
            if (data.safety_score < 40) {
                safetyCard.style.color = 'var(--neon-red)';
                safetyCard.style.borderColor = 'rgba(255, 51, 102, 0.3)';
            } else {
                safetyCard.style.color = 'var(--neon-green)';
                safetyCard.style.borderColor = 'var(--border-glow)';
            }
        }

        const listContainer = document.getElementById('alternativesList');
        listContainer.innerHTML = "";
        data.alternative_steps.forEach(step => {
            const li = document.createElement('li');
            li.innerText = step;
            listContainer.appendChild(li);
        });

        navigateTo('state-results');

    } catch (error) {
        console.error("Application Runtime Exception:", error);
        // Fallback interface management on system exceptions
        alert("System Execution Fault. Reverting setup context parameters.");
        navigateTo('state-query');
    }
});

function resetAuditFlow() {
    document.getElementById('claim').value = '';
    document.getElementById('routine').value = '';

    navigateTo('state-query');
}