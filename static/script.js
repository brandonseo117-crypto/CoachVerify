// 🔄 Simple Single-Page Navigation
function navigateTo(stateId) {
    document.querySelectorAll('.view-state').forEach(state => {
        state.classList.remove('active-state');
    });

    const targetState = document.getElementById(stateId);
    if (targetState) {
        targetState.classList.add('active-state');
    }
}

// 💬 Chat Console Interface Management
document.getElementById('chatConsoleForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const inputField = document.getElementById('athleteMessageInput');
    const userMessage = inputField.value.trim();
    if (!userMessage) return;

    // 1️⃣ Display the Athlete message in the chat feed instantly
    appendMessage(userMessage, 'athlete');
    inputField.value = ''; // Clear out the input box

    // 2️⃣ Reveal the loading indicator and scroll down
    const loader = document.getElementById('inlineChatLoader');
    loader.style.display = 'flex';
    const thread = document.getElementById('chatThread');
    thread.scrollTop = thread.scrollHeight;

    // 3️⃣ Format payload. Defaulting profile directly to 'Varsity Athlete'
    const payload = {
        profile: 'Varsity Athlete',
        claim: userMessage, // Send the conversation line directly to the AI
        routine: 'Context requested within chat dialogue flow'
    };

    try {
        const response = await fetch('/api/audit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('Network payload resolution failed.');
        const data = await response.json();

        // 4️⃣ Append the Coach's textual analysis and structural medical tags
        appendMessage(data.translated_consensus, 'coach', data);

    } catch (error) {
        console.error("Error:", error);
        appendMessage("System link failure. Unable to contact clinical sports medicine databases right now.", 'coach');
    } finally {
        // 5️⃣ Dismiss the loader icon
        loader.style.display = 'none';
        thread.scrollTop = thread.scrollHeight;
    }
});

// 🎨 Structural Bubble Rendering Engine
// 🎨 Structural Bubble & Bibliography Rendering Engine
function appendMessage(text, sender, data = null) {
    const thread = document.getElementById('chatThread');
    const bubble = document.createElement('div');
    bubble.className = `message-bubble ${sender}`;

    if (sender === 'athlete') {
        bubble.innerText = text;
    } else {
        let content = `<p>${text}</p>`;

        // If the AI matches data and passes scoring parameters, inject the HUD component inline
        if (data && typeof data.safety_score !== 'undefined') {
            const safety = parseInt(data.safety_score);
            let indicatorColor = 'var(--neon-green)';

            if (safety < 40) {
                indicatorColor = 'var(--neon-red)';
            } else if (safety < 75) {
                indicatorColor = 'var(--neon-cyan)';
            }

            content += `
                <div class="coach-meta-badge" style="border-left: 2px solid ${indicatorColor}">
                    <span style="color: ${indicatorColor}; font-weight: 700; font-family: monospace;">⚡ TELEMETRY AUDIT VERIFIED</span><br>
                    <span style="font-size: 0.8rem; margin-top: 4px; display: block;">
                        Safety Index: <strong>${data.safety_score}/100</strong> | Performance Tier: <strong>${data.performance_score}/100</strong>
                    </span>
                    <span style="font-size: 0.8rem; display: block; margin-top: 4px; color: var(--text-sub);">
                        📚 Source Reference: ${data.matched_paper || 'General Sports Medicine Guidelines'}
                    </span>
                </div>
            `;

            // 📚 UPDATE SIDEBAR BIBLIOGRAPHY DYNAMICALLY
            const sidebarContainer = document.getElementById('sidebarSourcesContainer');
            if (sidebarContainer) {
                // Clear out initial empty text states or previous query parameters
                sidebarContainer.innerHTML = '';

                // Safely iterate through database-grounded papers if the AI payload parsed them
                if (data.individual_papers && data.individual_papers.length > 0) {
                    data.individual_papers.forEach(paper => {
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
                        card.innerHTML = `
                            <a class="source-title-link" href="${paper.pubmed_link || '#'}" target="_blank" rel="noopener noreferrer">
                                ${paper.title}
                            </a>
                            <div class="source-meta-row">
                                <span class="source-journal">${paper.journal || 'Sports Med Journal'}</span>
                                <span class="source-reliability-tag" style="background: ${badgeColor}; color: ${textColor};">
                                    RIGOR: ${reliability}%
                                </span>
                            </div>
                        `;
                        sidebarContainer.appendChild(card);
                    });
                } else {
                    // Fallback reference card if individual items array is omitted
                    sidebarContainer.innerHTML = `
                        <div class="source-sidebar-card">
                            <span class="source-title-link">${data.matched_paper || 'Clinical Consensus Reference'}</span>
                            <div class="source-meta-row">
                                <span class="source-journal">Core Database Evidence</span>
                                <span class="source-reliability-tag" style="background: rgba(0, 223, 250, 0.15); color: var(--neon-cyan);">
                                    VERIFIED
                                </span>
                            </div>
                        </div>
                    `;
                }
            }
        }
        bubble.innerHTML = content;
    }

    thread.appendChild(bubble);
    thread.scrollTop = thread.scrollHeight; // Keep view locked to recent transmissions
}