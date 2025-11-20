/**
 * Combat UI Manager
 * Handles combat interface and interactions
 */

class CombatManager {
    constructor(gameClient, characterManager) {
        this.gameClient = gameClient;
        this.characterManager = characterManager;
        this.modal = document.getElementById('combatModal');
        this.currentCombat = null;
        this.selectedTarget = 0;
        this.isManuallyClosing = false; // Flag to prevent auto-reopen
        this.setupEventListeners();
    }

    /**
     * Setup event listeners for combat UI
     */
    setupEventListeners() {
        // Attack button
        document.getElementById('combatAttackBtn').addEventListener('click', () => {
            this.attack();
        });

        // Use item button
        document.getElementById('combatItemBtn').addEventListener('click', () => {
            this.showItemSelection();
        });

        // Flee button
        document.getElementById('combatFleeBtn').addEventListener('click', () => {
            this.flee();
        });

        // Continue button (after combat ends)
        document.getElementById('combatContinueBtn').addEventListener('click', () => {
            this.closeCombat();
        });

        // Escape key to close modal (when combat is over)
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal.style.display === 'block' && this.currentCombat && this.currentCombat.is_over) {
                this.closeCombat();
            }
        });
    }

    /**
     * Show the combat modal with combat data
     */
    showCombat(combatData) {
        this.currentCombat = combatData;
        this.modal.style.display = 'block';

        // Show action buttons initially
        const actionsDiv = document.querySelector('.combat-actions');
        if (actionsDiv) {
            actionsDiv.style.display = 'flex';
        }

        // Hide result section initially
        document.getElementById('combatResult').style.display = 'none';

        this.renderCombat(combatData);
    }

    /**
     * Close the combat modal
     */
    async closeCombat() {
        this.isManuallyClosing = true; // Set flag to prevent auto-close loop

        // Update character display with final combat data before clearing
        if (this.currentCombat && this.currentCombat.player) {
            this.characterManager.updateCharacterDisplay(this.currentCombat.player);
        }

        this.modal.style.display = 'none';
        this.currentCombat = null;
        this.selectedTarget = 0;

        // Show action buttons again for next combat
        const actionsDiv = document.querySelector('.combat-actions');
        if (actionsDiv) {
            actionsDiv.style.display = 'flex';
        }

        // Hide result section
        const resultDiv = document.getElementById('combatResult');
        if (resultDiv) {
            resultDiv.style.display = 'none';
        }

        // Refresh game state to update UI (including heal button)
        if (window.refreshGameState) {
            window.refreshGameState();
        }

        // Check if we're in a dungeon and show room info after combat
        try {
            const stateResponse = await this.gameClient.getState();
            if (stateResponse.success && stateResponse.state.active_quest?.dungeon?.entered) {
                // We're in a dungeon, show the current room
                const roomResponse = await this.gameClient.getCurrentRoom();
                if (roomResponse.success && window.showDungeonRoom) {
                    window.showDungeonRoom(roomResponse);
                }
            }
        } catch (error) {
            console.error('Error checking dungeon state after combat:', error);
        }

        // Trigger state refresh after a longer delay to ensure backend has cleared combat
        setTimeout(() => {
            if (window.refreshGameState) {
                window.refreshGameState();
            }
            // Clear flag after state refresh completes
            setTimeout(() => {
                this.isManuallyClosing = false;
            }, 500);
        }, 200);
    }

    /**
     * Render combat UI with current combat data
     */
    renderCombat(combatData) {
        // Render party status (all members if party exists, otherwise single player)
        if (combatData.party && combatData.party.length > 0) {
            this.renderPartyStatus(combatData.party);
        } else {
            // Legacy single player
            this.renderPlayerStatus(combatData.player);
        }

        // Render monsters
        this.renderMonsters(combatData.monsters);

        // Render combat log
        this.renderCombatLog(combatData.combat_log);

        // Render player status effects (for active character)
        if (combatData.player) {
            this.renderStatusEffects(combatData.player);
        }

        // Check if combat is over
        if (combatData.is_over) {
            this.showCombatResult(combatData);
        }
    }

    /**
     * Render party status (all party members)
     */
    renderPartyStatus(party) {
        const container = document.getElementById('playerStatusContainer');

        let partyHTML = '<h3 style="margin: 0 0 10px 0;">Party</h3>';

        party.forEach((character, index) => {
            const hpPercent = (character.hp_current / character.hp_max) * 100;
            let hpColor = '#4CAF50';
            if (hpPercent <= 25) {
                hpColor = '#f44336';
            } else if (hpPercent <= 50) {
                hpColor = '#FF9800';
            }

            partyHTML += `
                <div class="party-member-combat" style="margin-bottom: 10px; padding: 8px; background: #1e1e1e; border-radius: 4px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                        <strong style="font-size: 14px;">${character.name}</strong>
                        <span style="font-size: 12px; color: #888;">AC ${character.ac}</span>
                    </div>
                    <div class="hp-bar-container">
                        <div class="hp-bar">
                            <div class="hp-fill" style="width: ${hpPercent}%; background: ${hpColor};"></div>
                        </div>
                        <span class="hp-text">${character.hp_current}/${character.hp_max} HP</span>
                    </div>
                </div>
            `;
        });

        container.innerHTML = partyHTML;
    }

    /**
     * Render player status (HP bar) - Legacy single player
     */
    renderPlayerStatus(player) {
        document.getElementById('combatPlayerName').textContent = player.name;

        const hpPercent = (player.hp_current / player.hp_max) * 100;
        const hpBar = document.getElementById('playerHpBar');
        const hpText = document.getElementById('playerHpText');

        hpBar.style.width = `${hpPercent}%`;
        hpText.textContent = `${player.hp_current}/${player.hp_max} HP`;

        // Color code HP bar
        if (hpPercent > 50) {
            hpBar.style.background = '#4CAF50';
        } else if (hpPercent > 25) {
            hpBar.style.background = '#FF9800';
        } else {
            hpBar.style.background = '#f44336';
        }
    }

    /**
     * Render monsters in combat
     */
    renderMonsters(monsters) {
        const container = document.getElementById('monstersContainer');
        container.innerHTML = '';

        monsters.forEach((monster, index) => {
            const monsterCard = document.createElement('div');
            monsterCard.className = 'monster-card';
            if (index === this.selectedTarget && monster.is_alive) {
                monsterCard.classList.add('selected');
            }
            if (!monster.is_alive) {
                monsterCard.classList.add('defeated');
            }

            const hpPercent = (monster.hp_current / monster.hp_max) * 100;

            monsterCard.innerHTML = `
                <div class="monster-header">
                    <h4>${monster.name}</h4>
                    <span class="monster-ac">AC ${monster.ac}</span>
                </div>
                <div class="hp-bar-container">
                    <div class="hp-bar">
                        <div class="hp-fill" style="width: ${hpPercent}%; background: ${monster.is_alive ? '#f44336' : '#999'};"></div>
                    </div>
                    <span class="hp-text">${monster.hp_current}/${monster.hp_max} HP</span>
                </div>
                <div class="monster-status">
                    ${monster.is_alive ? 'Alive' : 'Defeated'}
                </div>
            `;

            // Click to select target
            if (monster.is_alive) {
                monsterCard.style.cursor = 'pointer';
                monsterCard.addEventListener('click', () => {
                    this.selectTarget(index);
                });
            }

            container.appendChild(monsterCard);
        });
    }

    /**
     * Render combat log messages
     */
    renderCombatLog(logMessages) {
        const logContainer = document.getElementById('combatLog');
        logContainer.innerHTML = '';

        // Safety check: ensure logMessages is an array
        if (!logMessages || !Array.isArray(logMessages)) {
            logMessages = [];
        }

        // Show last 10 messages
        const recentMessages = logMessages.slice(-10);

        recentMessages.forEach(msg => {
            const logEntry = document.createElement('div');
            logEntry.className = `log-entry log-${msg.type}`;
            logEntry.textContent = msg.message;
            logContainer.appendChild(logEntry);
        });

        // Auto-scroll to bottom
        logContainer.scrollTop = logContainer.scrollHeight;
    }

    /**
     * Render player status effects
     */
    renderStatusEffects(player) {
        const container = document.getElementById('playerStatusEffects');
        container.innerHTML = '';

        if (player.status_effects && player.status_effects.length > 0) {
            player.status_effects.forEach(effect => {
                const effectBadge = document.createElement('span');
                effectBadge.className = `status-badge status-${effect.type}`;
                effectBadge.textContent = `${effect.type} (${effect.duration})`;
                effectBadge.title = effect.description || '';
                container.appendChild(effectBadge);
            });
        }
    }

    /**
     * Select a monster as attack target
     */
    selectTarget(index) {
        this.selectedTarget = index;
        this.renderMonsters(this.currentCombat.monsters);
    }

    /**
     * Perform attack action
     */
    async attack() {
        if (!this.currentCombat || this.currentCombat.is_over) return;

        try {
            const response = await this.gameClient.combatAttack(this.selectedTarget);

            if (response.success) {
                this.currentCombat = response.combat_status;
                this.renderCombat(this.currentCombat);

                // Update character HP
                this.characterManager.updateCharacterDisplay(this.currentCombat.player);
            } else if (response.combat_ended) {
                // Combat has already ended (race condition)
                this.closeCombat();
            } else {
                this.showNotification('Attack failed: ' + response.error, 'error');
            }
        } catch (error) {
            this.showNotification('Error during attack: ' + error.message, 'error');
        }
    }

    /**
     * Show item selection dialog
     */
    async showItemSelection() {
        const player = this.currentCombat?.player;
        if (!player || !player.inventory || player.inventory.length === 0) {
            this.showNotification('No items in inventory', 'error');
            return;
        }

        // Use the item selection modal
        const itemName = await showItemSelection(player.inventory);

        if (itemName) {
            this.useItem(itemName);
        }
    }

    /**
     * Use an item in combat
     */
    async useItem(itemName) {
        if (!this.currentCombat || this.currentCombat.is_over) return;

        try {
            const response = await this.gameClient.combatUseItem(itemName);

            if (response.success) {
                this.currentCombat = response.combat_status;
                this.renderCombat(this.currentCombat);

                // Update character
                this.characterManager.updateCharacterDisplay(this.currentCombat.player);
                this.showNotification(`Used ${itemName}`, 'success');
            } else if (response.combat_ended) {
                // Combat has already ended (race condition)
                this.closeCombat();
            } else {
                this.showNotification('Failed to use item: ' + response.error, 'error');
            }
        } catch (error) {
            this.showNotification('Error using item: ' + error.message, 'error');
        }
    }

    /**
     * Attempt to flee from combat
     */
    async flee() {
        if (!this.currentCombat || this.currentCombat.is_over) return;

        const confirmed = await showConfirm('Attempt to flee from combat?');
        if (!confirmed) return;

        try {
            const response = await this.gameClient.combatFlee();

            if (response.success && response.flee_result) {
                const fleeResult = response.flee_result;

                if (fleeResult.fled) {
                    // Successfully fled
                    this.showNotification(`Fled successfully! (Rolled ${fleeResult.roll} vs ${fleeResult.flee_chance}%)`, 'success');
                    this.closeCombat();
                } else {
                    // Failed to flee
                    this.showNotification(`Failed to flee! (Rolled ${fleeResult.roll} vs ${fleeResult.flee_chance}%)`, 'error');

                    // Update combat state if provided
                    if (response.combat_status) {
                        this.currentCombat = response.combat_status;
                        this.renderCombat(this.currentCombat);

                        // Update character HP
                        if (this.currentCombat.player) {
                            this.characterManager.updateCharacterDisplay(this.currentCombat.player);
                        }
                    }
                }
            } else if (response.combat_ended) {
                // Combat has already ended (race condition)
                this.closeCombat();
            } else {
                this.showNotification('Error fleeing: ' + (response.error || 'Unknown error'), 'error');
            }
        } catch (error) {
            console.error('Flee error:', error);
            this.showNotification('Error fleeing: ' + error.message, 'error');
        }
    }

    /**
     * Show combat result (victory/defeat)
     */
    showCombatResult(combatData) {
        const resultDiv = document.getElementById('combatResult');
        const titleEl = document.getElementById('combatResultTitle');
        const contentEl = document.getElementById('combatResultContent');

        // Hide action buttons
        const actionsDiv = document.querySelector('.combat-actions');
        if (actionsDiv) {
            actionsDiv.style.display = 'none';
        }

        // Show result
        resultDiv.style.display = 'block';

        // Make sure continue button is visible
        const continueBtn = document.getElementById('combatContinueBtn');
        if (continueBtn) {
            continueBtn.style.display = 'block';
        }

        if (combatData.combat_result === 'victory') {
            titleEl.textContent = 'Victory!';
            titleEl.style.color = '#4CAF50';

            let content = '<p>All enemies defeated!</p>';

            // Show loot if any
            if (combatData.loot && combatData.loot.length > 0) {
                content += '<h4>Loot:</h4><ul>';
                combatData.loot.forEach(item => {
                    content += `<li>${item}</li>`;
                });
                content += '</ul>';
            }

            contentEl.innerHTML = content;
        } else if (combatData.combat_result === 'defeat') {
            titleEl.textContent = 'Defeated...';
            titleEl.style.color = '#f44336';

            let content = '<p>You have been defeated!</p>';

            // Check for death save information in combat log
            const deathSaveMessages = this.extractDeathSaveInfo(combatData.combat_log);

            if (deathSaveMessages.length > 0) {
                content += '<div style="margin: 15px 0; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 5px;">';
                content += '<h4 style="margin-top: 0; color: #FFA000;">Death Save:</h4>';
                deathSaveMessages.forEach(msg => {
                    if (msg.includes('Survived with 1 HP')) {
                        content += `<p style="color: #4CAF50; font-weight: bold;">${msg}</p>`;
                    } else if (msg.includes('Dying')) {
                        content += `<p style="color: #f44336; font-weight: bold;">${msg}</p>`;
                    } else {
                        content += `<p>${msg}</p>`;
                    }
                });
                content += '</div>';
            }

            // Check dying status
            if (combatData.player && combatData.player.is_dying) {
                content += '<div style="margin: 15px 0; padding: 15px; background: rgba(244, 67, 54, 0.2); border: 2px solid #f44336; border-radius: 5px;">';
                content += '<p style="color: #f44336; font-size: 20px; font-weight: bold; text-align: center; margin: 0;">💀 GAME OVER</p>';
                content += '<p style="text-align: center; margin: 10px 0;">You have died from your wounds.</p>';
                content += '<p style="text-align: center; margin: 0;"><em>The adventure ends here...</em></p>';
                content += '</div>';
            } else {
                content += '<p><em>You manage to escape and recover some health...</em></p>';
            }

            contentEl.innerHTML = content;
        }
    }

    /**
     * Extract death save information from combat log
     */
    extractDeathSaveInfo(combatLog) {
        if (!combatLog || !Array.isArray(combatLog)) {
            return [];
        }

        const deathSaveMessages = [];
        const deathSaveKeywords = [
            'death save',
            'Death save',
            'Survived with 1 HP',
            'Dying!',
            'HP dropped to 0'
        ];

        combatLog.forEach(logEntry => {
            const message = logEntry.message || '';
            // Check if this is a death save related message
            const isDeathSave = deathSaveKeywords.some(keyword =>
                message.includes(keyword)
            );

            if (isDeathSave) {
                deathSaveMessages.push(message);
            }
        });

        return deathSaveMessages;
    }

    /**
     * Show notification message
     */
    showNotification(message, type = 'info') {
        // Use characterManager's notification system
        if (this.characterManager && this.characterManager.showNotification) {
            this.characterManager.showNotification(message, type);
        }
    }

    /**
     * Check if combat is currently active
     */
    isCombatActive() {
        return this.currentCombat !== null && !this.currentCombat.is_over;
    }
}
