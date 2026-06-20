// Single page navigation
function navigateTo(stateId) {
    document.querySelectorAll('.view-state').forEach(state => {
        state.classList.remove('active-state');
    });

    const targetState = document.getElementById(stateId);
    if (targetState) {
        targetState.classList.add('active-state');
    }
}

// chat interface
document.getElementById('chatConsoleForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const inputField = document.getElementById('athleteMessageInput');
    const userMessage = inputField.value.trim();
    if (!userMessage) return;

    appendMessage(userMessage, 'athlete');
    inputField.value = ''; // Clear out the input box

    const loader = document.getElementById('inlineChatLoader');
    loader.style.display = 'flex';
    const thread = document.getElementById('chatThread');
    thread.scrollTop = thread.scrollHeight;

    const payload = {
        profile: 'Varsity Athlete',
        claim: userMessage,
        routine: 'Context requested within chat dialogue flow'
    };

    try {
        const response = await fetch('/api/audit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        let data;
        try {
            data = await response.json();
        } catch (jsonError) {
            console.error("Failed to parse JSON response:", jsonError);
            const textResponse = await response.text();
            throw new Error(`Invalid response format: ${textResponse.substring(0, 200)}`);
        }

        if (data.error) {
            console.error("API Error:", data.error, data.details);
            appendMessage(`Error: ${data.error}. Details: ${data.details || 'Unknown error'}`, 'coach');
        } else if (!response.ok) {
            throw new Error(`Server returned HTTP code ${response.status}`);
        } else if (!data.audit_text) {
            console.error("Missing audit_text in response:", data);
            appendMessage("Error: Incomplete response from analysis engine. Please try again.", 'coach');
        } else {
            appendMessage(data.audit_text, 'coach', data);
        }

    } catch (error) {
        console.error("Error communicating with verification pipeline:", error);
        appendMessage(`Transmission error: ${error.message}`, 'coach');
    } finally {
        loader.style.display = 'none';
    }
});

function appendMessage(text, sender, data = null) {
    const thread = document.getElementById('chatThread');
    const bubble = document.createElement('div');
    bubble.className = `message-bubble ${sender}`;

    if (sender === 'athlete') {
        bubble.innerText = text;
    } else {
        let content = '';

        if (data && typeof data.safety_score !== 'undefined') {
            const safety = parseInt(data.safety_score);
            let indicatorColor = 'var(--neon-green)';

            if (safety < 40) {
                indicatorColor = 'var(--neon-red)';
            } else if (safety < 75) {
                indicatorColor = 'var(--neon-cyan)';
            }

            // Construct Consensus-Style Layout modules cleanly on the client side
            content += `
                <div class="scientific-response-block" style="display: flex; flex-direction: column; gap: 16px; width: 100%;">
                    <div class="consensus-summary-card" style="background: rgba(255, 255, 255, 0.02); border-left: 3px solid ${indicatorColor}; padding: 16px; border-radius: 4px 12px 12px 4px;">
                        <span class="summary-header" style="font-family: monospace; font-size: 0.75rem; color: ${indicatorColor}; letter-spacing: 1px; font-weight: 700; display: block; margin-bottom: 6px;">SYSTEM SYNTHESIS CONSENSUS</span>
                        <p class="consensus-main-paragraph" style="margin: 0; font-size: 0.95rem; line-height: 1.5; color: var(--text-main);">${data.audit_text || ''}</p>
                    </div>

                    <div class="study-badge-row" style="display: flex; flex-wrap: wrap; gap: 8px;">
                        <span class="study-pill design-chip" style="font-size: 0.7rem; font-family: monospace; padding: 4px 10px; background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border-subtle); border-radius: 100px; color: var(--text-sub);">DESIGN: ${data.study_type || 'Clinical Evaluation'}</span>
                        <span class="study-pill journal-chip" style="font-size: 0.7rem; font-family: monospace; padding: 4px 10px; background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border-subtle); border-radius: 100px; color: var(--text-sub);">JOURNAL: ${data.journal_authority || 'Sports Medicine'}</span>
                        <span class="study-pill year-chip" style="font-size: 0.7rem; font-family: monospace; padding: 4px 10px; background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border-subtle); border-radius: 100px; color: var(--text-sub);">YEAR: ${data.publication_year || 'N/A'}</span>
                    </div>

                    <div class="clinical-data-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px;">
                        <div class="data-metric-tile" style="background: rgba(7, 9, 19, 0.6); border: 1px solid var(--border-subtle); padding: 10px 14px; border-radius: 8px; display: flex; flex-direction: column; gap: 4px;">
                            <span class="tile-label" style="font-size: 0.7rem; color: var(--text-muted); font-family: monospace; text-transform: uppercase;">Sample Size</span>
                            <span class="tile-value sample-tile" style="font-size: 0.9rem; font-weight: 700; color: var(--text-main);">N = ${data.sample_size || 'N/A'}</span>
                        </div>
                        <div class="data-metric-tile" style="background: rgba(7, 9, 19, 0.6); border: 1px solid var(--border-subtle); padding: 10px 14px; border-radius: 8px; display: flex; flex-direction: column; gap: 4px;">
                            <span class="tile-label" style="font-size: 0.7rem; color: var(--text-muted); font-family: monospace; text-transform: uppercase;">Target Cohort</span>
                            <span class="tile-value cohort-tile" style="font-size: 0.9rem; font-weight: 700; color: var(--text-main);">${data.target_cohort || 'General Population'}</span>
                        </div>
                    </div>
                </div>

                <div class="coach-meta-badge research-summary-panel" style="border-left: 2px solid ${indicatorColor}; margin-top: 14px; padding-left: 10px; background: rgba(255,255,255,0.01); padding: 12px; border-radius: 0 8px 8px 0;">
                    <span class="summary-panel-title" style="color: ${indicatorColor}; font-weight: 700; font-family: monospace; font-size: 0.75rem; letter-spacing: 0.5px;"> RESEARCH SUMMARY: PRIMARY SELECTION</span><br>
                    <span style="font-size: 0.8rem; margin-top: 6px; display: block; color: var(--text-main);">
                        Safety Index: <strong class="safety-label">${data.safety_score}/100</strong> | Evidence Quality: <strong class="reliability-label">${data.reliability_score || data.performance_score}/100</strong>
                    </span>
                    <span class="reference-label" style="font-size: 0.8rem; display: block; margin-top: 6px; color: var(--text-sub); line-height: 1.3;">
                        Active Reference: ${data.matched_paper || 'General Guidelines'}
                    </span>
                </div>
            `;

            if (data.alternative) {
                content += `
                    <div class="clinical-pivot-box" style="margin-top: 12px; padding: 12px; background: rgba(0, 223, 250, 0.05); border: 1px dashed var(--neon-cyan); border-radius: 8px;">
                        <span style="color: var(--neon-cyan); font-weight: 700; font-size: 0.8rem; font-family: monospace;">RECOMMENDED CLINICAL PIVOT</span>
                        <p style="margin: 6px 0 0 0; font-size: 0.85rem; color: var(--text-main); line-height: 1.4;">${data.alternative}</p>
                    </div>
                `;
            }

            // data source sidebar
            const sidebarContainer = document.getElementById('sidebarSourcesContainer');
            if (sidebarContainer) {
                sidebarContainer.innerHTML = '';

                if (Array.isArray(data.individual_papers) && data.individual_papers.length > 0) {
                    data.individual_papers.forEach((paper, index) => {
                        const reliability = parseInt(paper.paper_reliability || 80);
                        let badgeColor = 'rgba(0, 255, 135, 0.15)';
                        let textColor = 'var(--neon-green)';

                        if (reliability < 50) {
                            badgeColor = 'rgba(255, 51, 102, 0.15)';
                            textColor = 'var(--neon-red)';
                        } else if (reliability < 75) {
                            badgeColor = 'rgba(0, 223, 250, 0.15)';
                            textColor = 'var(--neon-cyan)';
                        }

                        const card = document.createElement('div');
                        card.className = 'source-sidebar-card';
                        card.style.cursor = 'pointer';
                        card.style.transition = 'all 0.2s ease';
                        card.style.border = index === 0 ? `1px solid ${textColor}` : '1px solid var(--border-subtle)';

                        card.innerHTML = `
                            <div class="source-title-link" style="font-weight:600; color:var(--text-main); margin-bottom:4px; font-size:0.85rem; line-height:1.3;">
                                ${paper.title}
                            </div>
                            <div class="source-meta-row">
                                <span class="source-journal" style="font-size:0.7rem; color:var(--text-muted);">${paper.journal || 'Sports Med Journal'}</span>
                                <span class="source-reliability-tag" style="background: ${badgeColor}; color: ${textColor}; padding: 2px 6px; border-radius: 4px; font-size: 0.65rem; font-family: monospace;">
                                    RIGOR: ${reliability}%
                                </span>
                            </div>
                        `;

                        card.addEventListener('click', (e) => {
                            e.preventDefault();

                            const responseBlock = bubble.querySelector('.scientific-response-block');
                            const summaryPanel = bubble.querySelector('.research-summary-panel');

                            if (responseBlock) {

                                responseBlock.querySelector('.design-chip').innerText = `DESIGN: ${paper.study_type || 'Clinical Trial'}`;
                                responseBlock.querySelector('.journal-chip').innerText = `JOURNAL: ${paper.journal || 'Sports Med Journal'}`;
                                responseBlock.querySelector('.year-chip').innerText = `YEAR: ${paper.publication_year || 'N/A'}`;


                                responseBlock.querySelector('.sample-tile').innerText = `N = ${paper.sample_size || 'N/A'}`;
                                responseBlock.querySelector('.cohort-tile').innerText = `${paper.target_cohort || 'Monitored Cohort'}`;
                            }

                            if (summaryPanel) {

                                summaryPanel.querySelector('.summary-panel-title').innerText = `RESEARCH SUMMARY: ${paper.journal ? paper.journal.toUpperCase() : 'SELECTION'}`;
                                summaryPanel.querySelector('.reliability-label').innerText = `${reliability}/100`;
                                summaryPanel.querySelector('.reference-label').innerText = `Active Reference: ${paper.title}`;


                                summaryPanel.style.borderLeft = `2px solid ${textColor}`;
                                summaryPanel.querySelector('.summary-panel-title').style.color = textColor;
                            }

                            // Update active sidebar border status
                            bubble.querySelectorAll('.source-sidebar-card').forEach(c => c.style.border = '1px solid var(--border-subtle)');
                            card.style.border = `1px solid ${textColor}`;
                        });

                        sidebarContainer.appendChild(card);
                    });
                } else {
                    const destinationLink = data.source_link || data.pubmed_link || '#';
                    sidebarContainer.innerHTML = `
                        <div class="source-sidebar-card">
                            <a class="source-title-link" href="${destinationLink}" target="_blank" rel="noopener noreferrer">${data.matched_paper || 'Clinical Consensus Reference'}</a>
                            <div class="source-meta-row">
                                <span class="source-journal">Core Database Evidence</span>
                                <span class="source-reliability-tag" style="background: rgba(0, 223, 250, 0.15); color: var(--neon-cyan);">VERIFIED</span>
                            </div>
                        </div>
                    `;
                }
            }
        } else {
            content = text ? `${text}` : 'System failure processing message context.';
        }

        bubble.innerHTML = content;
    }

    thread.appendChild(bubble);
    thread.scrollTop = thread.scrollHeight;
}