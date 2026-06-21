function navigateTo(stateId) {
    document.querySelectorAll('.view-state').forEach(state => {
        state.classList.remove('active-state');
        state.style.display = 'none';
    });

    const targetState = document.getElementById(stateId);
    if (targetState) {
        targetState.classList.add('active-state');
        targetState.style.display = (stateId === 'state-chat') ? 'flex' : 'block';
    }
}

function fillClaim(text) {
    document.getElementById('claimInput').value = text;
}

async function submitAudit(event) {
    event.preventDefault();
    const inputElement = document.getElementById('claimInput');
    const claimText = inputElement.value.trim();
    if (!claimText) return;

    const chatHistory = document.getElementById('chatHistory');
    const userBubble = document.createElement('div');
    userBubble.className = 'chat-bubble user';
    userBubble.textContent = claimText;
    chatHistory.appendChild(userBubble);

    inputElement.value = '';
    chatHistory.scrollTop = chatHistory.scrollHeight;

    const loader = document.getElementById('chatLoader');
    if (loader) loader.style.display = 'flex';

    try {
        const response = await fetch('/api/audit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ claim: claimText })
        });

        const data = await response.json();

        if (loader) loader.style.display = 'none';

        const aiBubble = document.createElement('div');
        aiBubble.className = 'chat-bubble ai';
        aiBubble.textContent = data.audit_text || "Analysis complete.";
        chatHistory.appendChild(aiBubble);
        chatHistory.scrollTop = chatHistory.scrollHeight;

        renderMetrics(data);

    } catch (err) {
        if (loader) loader.style.display = 'none';
        console.error("Network analysis error:", err);
    }
}

function renderMetrics(data) {
    const sVal = document.getElementById('safetyVal');
    const pVal = document.getElementById('perfVal');

    // Output integers explicitly structured out of 100 for readability
    sVal.textContent = data.safety_score !== undefined ? `${data.safety_score}/100` : '--';
    pVal.textContent = data.performance_score !== undefined ? `${data.performance_score}/100` : '--';

    sVal.style.color = (data.safety_score >= 70) ? 'var(--color-safe)' : (data.safety_score >= 40) ? 'var(--color-warning)' : 'var(--color-danger)';
    pVal.style.color = 'var(--color-accent)';

    document.getElementById('metaGrid').innerHTML = `
        <strong>Journal:</strong> ${data.journal_authority || 'N/A'}<br>
        <strong>Design Frame:</strong> ${data.study_type || 'N/A'}<br>
        <strong>Year:</strong> ${data.publication_year || 'N/A'}<br>
        <strong>Sample Metric:</strong> N = ${data.sample_size || 'N/A'}
    `;

    const stream = document.getElementById('papersStream');
    stream.innerHTML = '';

    if (data.individual_papers && data.individual_papers.length > 0) {
        data.individual_papers.forEach((paper, index) => {
            const card = document.createElement('div');
            card.className = `source-card ${index === 0 ? 'active' : ''}`;

            const linkUrl = paper.pubmed_link || "https://pubmed.ncbi.nlm.nih.gov/";

            // Extract the reliability integer or default to '--'
            const qualityRating = paper.paper_reliability !== undefined ? `${paper.paper_reliability}% Quality` : '--';

            // Dynamic color selection for the badge depending on evidence rigor thresholds
            const badgeColor = (paper.paper_reliability >= 85) ? 'var(--color-safe)' : 'var(--color-warning)';

            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; margin-bottom: 6px;">
                    <div class="source-title" style="margin: 0; flex: 1;">
                        <a href="${linkUrl}" target="_blank" rel="noopener noreferrer" style="color: var(--color-accent); text-decoration: none; border-bottom: 1px dashed transparent;" onclick="event.stopPropagation()" onmouseover="this.style.borderBottom='1px solid var(--color-accent)'" onmouseout="this.style.borderBottom='1px dashed transparent'">
                            ${paper.title}
                        </a>
                    </div>
                    <span style="font-size: 0.75rem; font-weight: 700; color: ${badgeColor}; background: #f8fafc; border: 1px solid var(--border-subtle); padding: 2px 6px; border-radius: 4px; white-space: nowrap;">
                        ${qualityRating}
                    </span>
                </div>
                <div class="source-meta">${paper.journal} • ${paper.publication_year} • N=${paper.sample_size}</div>
            `;

            card.onclick = () => {
                document.querySelectorAll('.source-card').forEach(c => c.classList.remove('active'));
                card.classList.add('active');

                document.getElementById('metaGrid').innerHTML = `
                    <strong>Journal:</strong> ${paper.journal}<br>
                    <strong>Design Frame:</strong> ${paper.study_type}<br>
                    <strong>Year:</strong> ${paper.publication_year}<br>
                    <strong>Sample Metric:</strong> N = ${paper.sample_size}
                `;
            };

            stream.appendChild(card);
        });
    } else {
        stream.innerHTML = '<div style="font-size:0.85rem; color:var(--text-muted);">No independent references attached.</div>';
    }
}