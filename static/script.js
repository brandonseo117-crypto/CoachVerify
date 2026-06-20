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

// Chat Console Interface Management
document.getElementById('chatConsoleForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const inputField = document.getElementById('athleteMessageInput');
    const userMessage = inputField.value.trim();
    if (!userMessage) return;

    // Display the Athlete message in the chat feed instantly
    appendMessage(userMessage, 'athlete');
    inputField.value = ''; // Clear out the input box

    // Reveal the loading indicator and scroll down
    const loader = document.getElementById('inlineChatLoader');
    loader.style.display = 'flex';
    const thread = document.getElementById('chatThread');
    thread.scrollTop = thread.scrollHeight;

    // Format payload. Defaulting profile directly to 'Varsity Athlete'
    const payload = {
        profile: 'Varsity Athlete',
        claim: userMessage, // Send the conversation line directly to the AI
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
            console.error("Raw response:", textResponse);
            throw new Error(`Invalid response format: ${textResponse.substring(0, 200)}`);
        }

        // Check if API returned an error response
        if (data.error) {
            console.error("API Error:", data.error, data.details);
            appendMessage(`Error: ${data.error}. Details: ${data.details || 'Unknown error'}`, 'coach');
        } else if (!response.ok) {
            throw new Error(`Server returned HTTP code ${response.status}`);
        } else if (!data.audit_text) {
            console.error("Missing audit_text in response:", data);
            appendMessage("Error: Incomplete response from analysis engine. Please try again.", 'coach');
        } else {
            // 4️⃣ Append Coach response along with structured data telemetry mapping
            appendMessage(data.audit_text, 'coach', data);
        }

    } catch (error) {
        console.error("Error communicating with verification pipeline:", error);
        console.error("Full error details:", error.message, error.stack);
        appendMessage(`Transmission error: ${error.message}`, 'coach');
    } finally {
        // 5️⃣ Hide loader state completely
        loader.style.display = 'none';
    }
});

// 🎨 Structural Bubble & Bibliography Rendering Engine
function appendMessage(text, sender, data = null) {
    const thread = document.getElementById('chatThread');
    const bubble = document.createElement('div');
    bubble.className = `message-bubble ${sender}`;

    if (sender === 'athlete') {
        bubble.innerText = text; // Keeps user-entered strings raw and protected from scripting injection
    } else {
        // 🔬 Accept and parse multi-modular HTML containers directly from the updated AI pipeline
        let content = `${text}`;

        // If the backend passes telemetry metrics, inject the premium index badge
        if (data && typeof data.safety_score !== 'undefined') {
            const safety = parseInt(data.safety_score);
            let indicatorColor = 'var(--neon-green)';

            if (safety < 40) {
                indicatorColor = 'var(--neon-red)';
            } else if (safety < 75) {
                indicatorColor = 'var(--neon-cyan)';
            }

            content += `
                <div class="coach-meta-badge" style="border-left: 2px solid ${indicatorColor}; margin-top: 14px;">
                    <span style="color: ${indicatorColor}; font-weight: 700; font-family: monospace;">⚡ TELEMETRY AUDIT VERIFIED</span><br>
                    <span style="font-size: 0.8rem; margin-top: 4px; display: block;">
                        Safety Index: <strong>${data.safety_score}/100</strong> | Performance Tier: <strong>${data.performance_score}/100</strong>
                    </span>
                    <span style="font-size: 0.8rem; display: block; margin-top: 4px; color: var(--text-sub);">
                        Primary Reference: ${data.matched_paper || 'General Guidelines'}
                    </span>
                </div>
            `;

            // If the AI provides an explicit clinical alternative, parse and append its structural UI widget
            if (data.alternative) {
                content += `
                    <div class="clinical-pivot-box" style="margin-top: 12px; padding: 12px; background: rgba(0, 223, 250, 0.05); border: 1px dashed var(--neon-cyan); border-radius: 8px;">
                        <span style="color: var(--neon-cyan); font-weight: 700; font-size: 0.8rem; font-family: monospace;">🔬 RECOMMENDED CLINICAL PIVOT</span>
                        <p style="margin: 6px 0 0 0; font-size: 0.85rem; color: var(--text-main); line-height: 1.4;">${data.alternative}</p>
                    </div>
                `;
            }

            // 📚 UPDATE SIDEBAR BIBLIOGRAPHY DYNAMICALLY (30% WIDTH PANEL)
            const sidebarContainer = document.getElementById('sidebarSourcesContainer');
            if (sidebarContainer) {
                sidebarContainer.innerHTML = ''; // Clear out empty placeholder telemetry status frames

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

                        // Support flexible URL routing schema (Handles generic source_link or fallback pubmed_link fields smoothly)
                        const destinationLink = paper.source_link || paper.pubmed_link || '#';

                        const card = document.createElement('div');
                        card.className = 'source-sidebar-card';
                        card.innerHTML = `
                            <a class="source-title-link" href="${destinationLink}" target="_blank" rel="noopener noreferrer">
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
                    // Fallback reference card if explicit individual array metrics are absent from backend return packets
                    const destinationLink = data.source_link || data.pubmed_link || '#';
                    sidebarContainer.innerHTML = `
                        <div class="source-sidebar-card">
                            <a class="source-title-link" href="${destinationLink}" target="_blank" rel="noopener noreferrer">
                                ${data.matched_paper || 'Clinical Consensus Reference'}
                            </a>
                            <div class="source-meta-row">
                                <span class="source-journal">Core Grounding Database</span>
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