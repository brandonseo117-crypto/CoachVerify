document.getElementById('auditForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const submitBtn = document.getElementById('submitBtn');
    const payload = {
        profile: document.getElementById('profile').value,
        claim: document.getElementById('claim').value,
        routine: document.getElementById('routine').value
    };

    try {
        submitBtn.innerText = "Querying Database...";
        submitBtn.disabled = true;

        const response = await fetch('http://127.0.0.1:5000/api/audit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('Data drop failed');
        const data = await response.json();

        // 1. Populate elements safely
        document.getElementById('safetyScore').innerText = data.safety_score;
        document.getElementById('perfScore').innerText = data.performance_score;
        document.getElementById('matchedPaper').innerText = data.matched_paper;
        document.getElementById('translationText').innerText = data.translated_consensus;

        // 2. Target the element by its unique ID instead of querySelector to avoid crashing
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

        // 3. Handle Alternatives Checklist Generation
        const listContainer = document.getElementById('alternativesList');
        listContainer.innerHTML = "";
        data.alternative_steps.forEach(step => {
            const li = document.createElement('li');
            li.innerText = step;
            listContainer.appendChild(li);
        });

        // 4. Slide the track over smoothly!
        document.getElementById('analyticsTrack').style.transform = "translateX(-50%)";

    } catch (error) {
        // Log the actual structural error to the console instead of a generic connection message
        console.error("Application Runtime Exception:", error);
    } finally {
        submitBtn.innerText = "Execute Audit Matrix";
        submitBtn.disabled = false;
    }
});

// Global helper to allow sliding between view states manually
function slideToState(index) {
    const track = document.getElementById('analyticsTrack');
    if (index === 0) {
        track.style.transform = "translateX(0%)";
    } else if (index === 1) {
        track.style.transform = "translateX(-50%)";
    }
}