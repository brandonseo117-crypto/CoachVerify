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

        // --- Core Metric Updates ---
        document.getElementById('safetyScore').innerText = data.safety_score;
        document.getElementById('perfScore').innerText = data.performance_score;
        document.getElementById('matchedPaper').innerText = data.matched_paper;
        document.getElementById('translationText').innerText = data.translated_consensus;

        const reliability = parseInt(data.reliability_score);
        document.getElementById('reliabilityScore').innerText = reliability;

        // --- Safety Card Styling Mapping ---
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

        const relCard = document.getElementById('reliabilityCard');
        const relDisplay = document.getElementById('reliabilityScore');
        const relBadge = document.getElementById('reliabilityBadge');
        if (relBadge && relDisplay) {
            if (reliability >= 80) {
                relDisplay.style.color = 'var(--neon-green)';
                relBadge.innerText = "Gold Standard Evidence";
                relBadge.style.color = 'var(--bg-dark)';
                relBadge.style.backgroundColor = 'var(--neon-green)';
            } else if (reliability >= 50) {
                relDisplay.style.color = 'var(--neon-cyan)';
                relBadge.innerText = "Limited / Adult Cohort";
                relBadge.style.color = 'var(--bg-dark)';
                relBadge.style.backgroundColor = 'var(--neon-cyan)';
            } else {
                relDisplay.style.color = 'var(--neon-red)';
                relBadge.innerText = "Low Rigor / Anecdotal";
                relBadge.style.color = '#FFF';
                relBadge.style.backgroundColor = 'var(--neon-red)';
            }
        }

        // --- Upgraded Blueprint Checklist Generation with Research Rationales ---
        const listContainer = document.getElementById('alternativesList');
        listContainer.innerHTML = "";

        if (data.alternative_steps && data.alternative_steps.length > 0) {
            data.alternative_steps.forEach(step => {
                const li = document.createElement('li');
                li.style.display = 'flex';
                li.style.flexDirection = 'column';
                li.style.gap = '4px';

                li.innerHTML = `
                    <strong style="color: var(--text-main); font-size: 0.95rem;">
                        ${step.actionable_tip}
                    </strong>
                    <span style="color: var(--text-sub); font-size: 0.85rem; line-height: 1.4;">
                        🔬 Rationale: ${step.scientific_rationale}
                    </span>
                `;
                listContainer.appendChild(li);
            });
        } else {
            listContainer.innerHTML = '<li style="color: var(--text-sub);">No alternative metrics compiled for this matrix segment.</li>';
        }

        // --- Literature Breakdown Section ---
        const sourcesContainer = document.getElementById('sourcesContainer');
        if (sourcesContainer) {
            sourcesContainer.innerHTML = ""; // Wipe the template placeholder

            if (data.individual_papers && data.individual_papers.length > 0) {
                data.individual_papers.forEach(paper => {
                    const paperCard = document.createElement('div');
                    paperCard.className = 'source-paper-card';

                    const leftMeta = document.createElement('div');
                    leftMeta.className = 'paper-left-meta';

                    const paperLink = document.createElement('a');
                    paperLink.className = 'paper-row-title';
                    paperLink.href = paper.pubmed_link;
                    paperLink.target = '_blank';
                    paperLink.innerText = paper.title;

                    const subtext = document.createElement('span');
                    subtext.className = 'paper-row-subtext';
                    subtext.innerText = paper.journal;

                    leftMeta.appendChild(paperLink);
                    leftMeta.appendChild(subtext);

                    const scorePill = document.createElement('div');
                    scorePill.className = 'paper-row-badge';
                    scorePill.innerText = `Rigor: ${paper.paper_reliability}%`;

                    if (paper.paper_reliability >= 80) {
                        scorePill.style.color = 'var(--bg-dark)';
                        scorePill.style.backgroundColor = 'var(--neon-green)';
                    } else if (paper.paper_reliability >= 50) {
                        scorePill.style.color = 'var(--bg-dark)';
                        scorePill.style.backgroundColor = 'var(--neon-cyan)';
                    } else {
                        scorePill.style.color = '#FFF';
                        scorePill.style.backgroundColor = 'var(--neon-red)';
                    }

                    paperCard.appendChild(leftMeta);
                    paperCard.appendChild(scorePill);
                    sourcesContainer.appendChild(paperCard);
                });
            } else {
                sourcesContainer.innerHTML = `<p class="empty-feed-text">No distinct sub-literature paths derived from current query model.</p>`;
            }
        }

        navigateTo('state-results');

    } catch (error) {
        console.error("Application Runtime Exception:", error);
        alert("System Execution Fault. Reverting setup context parameters.");
        navigateTo('state-query');
    }
});

function resetAuditFlow() {
    document.getElementById('claim').value = '';
    document.getElementById('routine').value = '';

    // Clear dynamic lists so old data doesn't flash on the next run
    document.getElementById('alternativesList').innerHTML = "";
    document.getElementById('sourcesContainer').innerHTML = '<p class="empty-feed-text">Awaiting clinical verification matrix sequence...</p>';

    navigateTo('state-query');
}