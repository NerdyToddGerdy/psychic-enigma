/**
 * Main Application Controller
 * Coordinates all UI components and API interactions
 */

// Initialize components
const gameClient = new GameClient();
const hexRenderer = new HexRenderer(document.getElementById('hexGrid'));
const questManager = new QuestManager(
    document.getElementById('questList'),
    document.getElementById('activeQuest'),
    document.getElementById('completedQuestList')
);
const characterManager = new CharacterManager(gameClient);
const combatManager = new CombatManager(gameClient, characterManager);

// State
let currentState = null;

// Expose refresh function for combat manager
window.refreshGameState = async function() {
    try {
        const response = await gameClient.getState();
        updateUI(response.state);
    } catch (error) {
        console.error('Failed to refresh state:', error);
    }
};

/**
 * Initialize application
 */
async function init() {
    try {
        // Load current game state
        const response = await gameClient.getState();
        updateUI(response.state);

        // Setup event handlers
        setupEventHandlers();

        // Check if player has a character, if not show character modal
        if (!response.state.player) {
            setTimeout(() => characterManager.showModal(), 500);
        } else {
            // Update character manager with existing character
            characterManager.currentCharacter = response.state.player;
        }

        console.log('Game initialized');
    } catch (error) {
        console.error('Initialization error:', error);
        showError('Failed to initialize game');
    }
}

/**
 * Render character stats in main UI
 */
function renderCharacterStats(player, state = null) {
    const container = document.getElementById('characterStats');

    if (!player) {
        container.innerHTML = '<p class="no-character">No character - <a href="#" id="createCharacterLink">Create one</a></p>';

        // Re-add event listener for create link
        const createLink = document.getElementById('createCharacterLink');
        if (createLink) {
            createLink.addEventListener('click', (e) => {
                e.preventDefault();
                characterManager.showModal();
            });
        }
        return;
    }

    const hpPercent = (player.hp_current / player.hp_max) * 100;
    const inventoryCount = player.inventory ? player.inventory.length : 0;
    const silver = player.silver || 0;
    const gold = player.gold || 0;

    // Get day counter from state
    const currentDay = state ? (state.current_day || 1) : 1;
    const movementCount = state ? (state.movement_count || 0) : 0;

    // Calculate ability bonuses using Single Sheet Game System (14+ threshold)
    const calculateBonus = (score) => score >= 14 ? 1 : 0;
    const formatModifier = (mod) => mod >= 0 ? `+${mod}` : `${mod}`;

    const strMod = calculateBonus(player.strength || 10);
    const dexMod = calculateBonus(player.dexterity || 10);
    const wilMod = calculateBonus(player.willpower || 10);
    const touMod = calculateBonus(player.toughness || 10);

    // Level and XP
    const level = player.level || 1;
    const xpCurrent = player.xp_current || 0;

    // Single Sheet Game System: Flat 20 XP per level
    const xpForNextLevel = level * 20;
    const xpForCurrentLevel = (level - 1) * 20;
    const xpProgress = xpCurrent - xpForCurrentLevel;
    const xpNeeded = xpForNextLevel - xpForCurrentLevel;
    const xpPercent = (xpProgress / xpNeeded) * 100;

    // Build inventory HTML
    let inventoryHTML = '';
    if (inventoryCount > 0) {
        inventoryHTML = '<div class="inventory-details"><div class="inventory-items">';
        player.inventory.forEach((item, index) => {
            const isItemObject = typeof item === 'object' && item.item_type;
            const itemName = isItemObject ? item.name : item;
            const isConsumable = isItemObject && item.item_type === 'consumable';
            const itemType = isItemObject ? item.item_type : 'unknown';

            // Get rarity color if available
            let rarityClass = '';
            let rarityColor = '#888888';  // Default dark gray for visibility
            if (isItemObject && item.rarity) {
                const rarityColors = {
                    'COMMON': '#888888',  // Dark gray for visibility on light backgrounds
                    'UNCOMMON': '#1EFF00',
                    'RARE': '#0070DD',
                    'EPIC': '#A335EE',
                    'LEGENDARY': '#FF8000'
                };
                rarityColor = rarityColors[item.rarity] || '#888888';
                rarityClass = ` rarity-${item.rarity.toLowerCase()}`;
            }

            inventoryHTML += `
                <div class="inventory-item${rarityClass}" data-item-index="${index}">
                    <div class="item-name" style="color: ${rarityColor}">${itemName}</div>
                    ${isConsumable ? `<button class="btn btn-small use-item-btn" data-item-name="${itemName}">Use</button>` : ''}
                </div>
            `;
        });
        inventoryHTML += '</div></div>';
    }

    container.innerHTML = `
        <div class="character-name">
            <span>${player.name}</span>
            <span style="font-size: 14px; color: #888; margin-left: 8px;">Level ${level}</span>
        </div>
        <div class="character-class">
            ${player.race} ${player.character_type}
        </div>

        <!-- XP Progress Bar -->
        <div class="stat-item hp-display" style="margin-bottom: 10px;">
            <div style="width: 100%;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 11px;">
                    <span class="stat-label">XP</span>
                    <span class="stat-value">${xpCurrent} / ${xpForNextLevel}</span>
                </div>
                <div class="hp-bar-mini" style="background: #444;">
                    <div class="hp-fill-mini" style="width: ${xpPercent}%; background: linear-gradient(90deg, #4CAF50, #8BC34A);"></div>
                </div>
            </div>
        </div>

        <!-- Ability Scores Grid (Single Sheet: STR/DEX/WIL/TOU) -->
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; margin-bottom: 10px;">
            <div class="ability-score">
                <div class="ability-label">STR</div>
                <div class="ability-value">${player.strength || 10}</div>
                <div class="ability-mod">${formatModifier(strMod)}</div>
            </div>
            <div class="ability-score">
                <div class="ability-label">DEX</div>
                <div class="ability-value">${player.dexterity || 10}</div>
                <div class="ability-mod">${formatModifier(dexMod)}</div>
            </div>
            <div class="ability-score">
                <div class="ability-label">WIL</div>
                <div class="ability-value">${player.willpower || 10}</div>
                <div class="ability-mod">${formatModifier(wilMod)}</div>
            </div>
            <div class="ability-score">
                <div class="ability-label">TOU</div>
                <div class="ability-value">${player.toughness || 10}</div>
                <div class="ability-mod">${formatModifier(touMod)}</div>
            </div>
        </div>

        <!-- Core Stats Grid -->
        <div class="stat-grid">
            <div class="stat-item hp-display">
                <div style="width: 100%;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span class="stat-label">HP</span>
                        <span class="stat-value">${player.hp_current}/${player.hp_max}</span>
                    </div>
                    <div class="hp-bar-mini">
                        <div class="hp-fill-mini" style="width: ${hpPercent}%"></div>
                    </div>
                </div>
            </div>
            <div class="stat-item">
                <span class="stat-label">AC</span>
                <span class="stat-value">${player.ac}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Attack</span>
                <span class="stat-value">+${player.attack_bonus}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Currency</span>
                <span class="stat-value">${gold}gp ${silver}sp</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Day</span>
                <span class="stat-value">${currentDay} (${movementCount}/5)</span>
            </div>
        </div>
        ${inventoryCount > 0 ? `
            <div class="inventory-summary" style="cursor: pointer;" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none';">
                <strong>Inventory:</strong> ${inventoryCount} item${inventoryCount !== 1 ? 's' : ''} ▼
            </div>
            ${inventoryHTML}
        ` : '<div class="inventory-summary"><strong>Inventory:</strong> Empty</div>'}
    `;

    // Add event listeners for use item buttons
    document.querySelectorAll('.use-item-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.stopPropagation();
            const itemName = btn.getAttribute('data-item-name');
            await useConsumableItem(itemName);
        });
    });
}

/**
 * Setup event handlers
 */
function setupEventHandlers() {
    // Create character link handler (initial render)
    const createLink = document.getElementById('createCharacterLink');
    if (createLink) {
        createLink.addEventListener('click', (e) => {
            e.preventDefault();
            characterManager.showModal();
        });
    }

    // Grid tabs
    document.querySelectorAll('.grid-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all grid tabs and panes
            document.querySelectorAll('.grid-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.grid-tab-pane').forEach(p => p.classList.remove('active'));

            // Add active class to clicked tab
            tab.classList.add('active');

            // Show corresponding tab pane
            const tabName = tab.getAttribute('data-tab');
            if (tabName === 'grid') {
                document.getElementById('gridTab').classList.add('active');
            } else if (tabName === 'settings') {
                document.getElementById('settingsTab').classList.add('active');
            }
        });
    });

    // Quest tabs
    document.querySelectorAll('.quest-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs and panes
            document.querySelectorAll('.quest-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

            // Add active class to clicked tab
            tab.classList.add('active');

            // Show corresponding tab pane
            const tabName = tab.getAttribute('data-tab');
            if (tabName === 'available') {
                document.getElementById('availableQuestsTab').classList.add('active');
            } else if (tabName === 'completed') {
                document.getElementById('completedQuestsTab').classList.add('active');
            }
        });
    });

    // New Game button
    document.getElementById('newGameBtn').addEventListener('click', async () => {
        const confirmed = await showConfirm('Start a new game? Current progress will be lost if not saved.');
        if (confirmed) {
            try {
                const response = await gameClient.newGame();
                updateUI(response.state);
                showMessage('New game started!');
            } catch (error) {
                showError('Failed to start new game: ' + error.message);
            }
        }
    });

    // Save Game button
    document.getElementById('saveGameBtn').addEventListener('click', () => {
        showModal('saveGameModal');
    });

    // Load Game button
    document.getElementById('loadGameBtn').addEventListener('click', async () => {
        try {
            const response = await gameClient.listSaves();
            renderSavesList(response.saves);
            showModal('loadGameModal');
        } catch (error) {
            showError('Failed to load saves list: ' + error.message);
        }
    });

    // Generate Quest button
    document.getElementById('generateQuestBtn').addEventListener('click', async () => {
        try {
            const response = await gameClient.generateQuest();

            // Refresh state to get updated hex grid
            const stateResponse = await gameClient.getState();
            updateUI(stateResponse.state);

            showMessage(`New quest generated: ${response.quest.action} ${response.quest.target}`);
        } catch (error) {
            showError('Failed to generate quest: ' + error.message);
        }
    });

    // Heal button
    document.getElementById('healBtn').addEventListener('click', async () => {
        try {
            const response = await gameClient.healPlayer();

            if (response.success) {
                // Refresh state to update character display
                const stateResponse = await gameClient.getState();

                // Use fresh state for success message
                const maxHp = stateResponse.state.player ? stateResponse.state.player.hp_max : 0;
                const costDisplay = response.silver_cost > 0 ? `${response.gold_cost}gp ${response.silver_cost}sp` : `${response.gold_cost}gp`;
                showMessage(`Healed ${response.hp_healed} HP for ${costDisplay}. Current HP: ${response.current_hp}/${maxHp}`);

                updateUI(stateResponse.state);
            }
        } catch (error) {
            showError('Failed to heal: ' + error.message);
        }
    });

    // Confirm save button
    document.getElementById('confirmSaveBtn').addEventListener('click', async () => {
        const filename = document.getElementById('saveFilename').value.trim() || null;
        try {
            const response = await gameClient.saveGame(filename);
            showMessage(response.message);
            closeModal('saveGameModal');
            document.getElementById('saveFilename').value = '';
        } catch (error) {
            showError('Failed to save game: ' + error.message);
        }
    });

    // Hex click handler
    hexRenderer.onHexClick = async (q, r, hexData) => {
        if (hexData.revealed || hexData.explored) {
            try {
                const response = await gameClient.movePlayer(q, r);

                if (response.success) {
                    // Check exploration results for dangers
                    if (response.explorations && response.explorations.length > 0) {
                        const hasDangers = response.explorations.some(exp =>
                            exp.results.dangers && exp.results.dangers.length > 0
                        );

                        if (hasDangers) {
                            // Show modal for dangers
                            showExplorationResults(response.explorations);
                        } else {
                            // Show brief notification for discoveries/spoor
                            showNonDangerNotifications(response.explorations);
                        }
                    }

                    // Check if dungeon was generated
                    if (response.dungeon_generated) {
                        // Show dungeon discovered modal
                        showDungeonDiscovered(response.dungeon_generated);
                    }

                    // Check if day advanced
                    if (response.day_advanced) {
                        showMessage(`☀️ A new day has begun! Day ${response.current_day}`);
                    }

                    // Check if ration prompt should be shown
                    if (response.ration_prompt_available && response.ration_heal_amount > 0) {
                        showRationPrompt(response.ration_heal_amount);
                    }

                    // Refresh state
                    const stateResponse = await gameClient.getState();
                    updateUI(stateResponse.state);
                }
            } catch (error) {
                showError('Cannot move there: ' + error.message);
            }
        }
    };

    // Quest accept handler
    questManager.onQuestAccept = async (questIndex) => {
        try {
            const response = await gameClient.acceptQuest(questIndex);

            // Refresh state
            const stateResponse = await gameClient.getState();
            updateUI(stateResponse.state);

            showMessage(response.message);
        } catch (error) {
            showError('Failed to accept quest: ' + error.message);
        }
    };

    // Dungeon re-entry handler
    questManager.onDungeonReenter = async () => {
        try {
            const response = await gameClient.enterDungeon();

            if (response.success) {
                // Get current room and show dungeon modal
                const roomResponse = await gameClient.getCurrentRoom();
                if (roomResponse.success) {
                    showDungeonRoom(roomResponse);
                }
            }
        } catch (error) {
            showError('Failed to re-enter dungeon: ' + error.message);
        }
    };

    // Modal close handlers
    setupModalHandlers();
}

/**
 * Update UI with new state
 */
function updateUI(state) {
    if (!state) {
        console.error('State is null or undefined');
        return;
    }

    currentState = state;

    // Update hex grid
    if (state.hex_grid && state.hex_grid.visible_hexes) {
        hexRenderer.renderGrid(state.hex_grid.visible_hexes, state.hex_grid.player_position);

        // Update player position display
        document.getElementById('playerPosition').textContent =
            `Position: (${state.hex_grid.player_position[0]}, ${state.hex_grid.player_position[1]})`;
    } else {
        console.error('hex_grid or visible_hexes missing from state:', state);
    }

    // Update character stats in main UI
    renderCharacterStats(state.player, state);

    // Update quests
    if (state.quests) {
        questManager.renderQuests(state.quests);
    }
    if (state.active_quest !== undefined) {
        const playerPosition = state.hex_grid ? state.hex_grid.player_position : null;
        questManager.renderActiveQuest(state.active_quest, playerPosition);
    }
    if (state.completed_quests) {
        questManager.renderCompletedQuests(state.completed_quests);
    }

    // Update current hex info
    if (state.hex_grid && state.hex_grid.player_position) {
        updateCurrentHexInfo(state.hex_grid.player_position);
    }

    // Highlight active quest destination
    if (state.active_quest && state.active_quest.coordinates) {
        hexRenderer.highlightHex(state.active_quest.coordinates[0], state.active_quest.coordinates[1]);
    }

    // Update Generate Quest button state based on settlement status
    if (state.hex_grid) {
        updateGenerateQuestButton(state);
    }

    // Update Heal button state based on settlement and HP
    if (state.hex_grid) {
        updateHealButton(state);
    }

    // Update character display if character exists
    if (state.player) {
        characterManager.updateCharacterDisplay(state.player);
    }

    // Handle combat if active
    if (state.active_combat && !state.active_combat.is_over) {
        // Only show/update combat if it's not already over

        // Show combat modal if not already shown and not manually closing
        if (!combatManager.isManuallyClosing && (!combatManager.currentCombat || combatManager.modal.style.display !== 'block')) {
            combatManager.showCombat(state.active_combat);
        } else if (!combatManager.isManuallyClosing && combatManager.modal.style.display === 'block') {
            // Update existing combat display only if modal is visible
            combatManager.renderCombat(state.active_combat);
        }
    }
}

/**
 * Update Generate Quest button enabled/disabled state
 */
function updateGenerateQuestButton(state) {
    const generateQuestBtn = document.getElementById('generateQuestBtn');

    // Find current hex
    const currentHex = state.hex_grid.visible_hexes.find(
        hex => hex.q === state.hex_grid.player_position[0] && hex.r === state.hex_grid.player_position[1]
    );

    // Check if at settlement
    const atSettlement = currentHex && currentHex.is_settlement;

    // Enable button only if at settlement
    if (atSettlement) {
        generateQuestBtn.disabled = false;
        generateQuestBtn.title = 'Generate a new quest';
    } else {
        generateQuestBtn.disabled = true;
        generateQuestBtn.title = 'Must be in a settlement to generate quests';
    }
}

/**
 * Update Heal button enabled/disabled state
 */
function updateHealButton(state) {
    const healBtn = document.getElementById('healBtn');

    // Check if player exists
    if (!state.player) {
        healBtn.disabled = true;
        healBtn.title = 'No character';
        return;
    }

    // Check if in combat - cannot heal during combat
    if (state.active_combat && state.active_combat.is_over === false) {
        healBtn.disabled = true;
        healBtn.title = 'Cannot heal during combat';
        return;
    }

    // Find current hex
    const currentHex = state.hex_grid.visible_hexes.find(
        hex => hex.q === state.hex_grid.player_position[0] && hex.r === state.hex_grid.player_position[1]
    );

    // Debug logging
    console.log('Heal Button Check:', {
        currentHex: currentHex,
        is_settlement: currentHex?.is_settlement,
        settlement_type: currentHex?.settlement_type,
        player_hp: `${state.player.hp_current}/${state.player.hp_max}`,
        player_currency: `${state.player.gold}gp ${state.player.silver}sp`
    });

    // Check if at settlement
    const atSettlement = currentHex && currentHex.is_settlement;

    // Check if HP is below max
    const needsHealing = state.player.hp_current < state.player.hp_max;

    // Calculate healing cost if needed
    if (atSettlement && needsHealing) {
        const missingHp = state.player.hp_max - state.player.hp_current;
        const goldCost = Math.ceil(missingHp / 10) * 5;

        // Check total currency (10 silver = 1 gold)
        const totalCurrencyInSilver = (state.player.gold * 10) + state.player.silver;
        const costInSilver = goldCost * 10;
        const hasEnoughCurrency = totalCurrencyInSilver >= costInSilver;

        if (hasEnoughCurrency) {
            healBtn.disabled = false;
            healBtn.title = `Heal ${missingHp} HP for ${goldCost}gp`;
        } else {
            healBtn.disabled = true;
            healBtn.title = `Not enough currency (need ${goldCost}gp, have ${state.player.gold}gp ${state.player.silver}sp)`;
        }
    } else if (!atSettlement) {
        healBtn.disabled = true;
        healBtn.title = 'Must be at a settlement to heal';
    } else if (!needsHealing) {
        healBtn.disabled = true;
        healBtn.title = 'Already at full health';
    }
}

/**
 * Update current hex information display
 */
function updateCurrentHexInfo(position) {
    const hexInfoDiv = document.getElementById('currentHexInfo');

    if (!currentState) {
        hexInfoDiv.innerHTML = '<p>No game state</p>';
        return;
    }

    // Find current hex in visible hexes
    const currentHex = currentState.hex_grid.visible_hexes.find(
        hex => hex.q === position[0] && hex.r === position[1]
    );

    if (!currentHex) {
        hexInfoDiv.innerHTML = '<p>Hex not loaded</p>';
        return;
    }

    let html = '<div class="hex-info">';
    html += `<div class="hex-info-item"><span class="hex-info-label">Coordinates:</span><span class="hex-info-value">(${currentHex.q}, ${currentHex.r})</span></div>`;
    html += `<div class="hex-info-item"><span class="hex-info-label">Terrain:</span><span class="hex-info-value">${currentHex.terrain}</span></div>`;
    html += `<div class="hex-info-item"><span class="hex-info-label">Water:</span><span class="hex-info-value">${currentHex.water ? 'Yes' : 'No'}</span></div>`;

    if (currentHex.explored) {
        html += `<div class="hex-info-item"><span class="hex-info-label">Weather:</span><span class="hex-info-value">${currentHex.weather}</span></div>`;

        if (currentHex.discoveries && currentHex.discoveries.length > 0) {
            html += '<div class="hex-discoveries"><h4>Discoveries:</h4><ul>';
            currentHex.discoveries.forEach(disc => {
                html += `<li>${disc.type}: ${disc.detail}</li>`;
            });
            html += '</ul></div>';
        }

        if (currentHex.dangers && currentHex.dangers.length > 0) {
            html += '<div class="hex-dangers"><h4>Dangers:</h4><ul>';
            currentHex.dangers.forEach(danger => {
                // Handle danger.detail which can be a string or an object with monsters
                let detailText = danger.detail;
                if (typeof danger.detail === 'object' && danger.detail !== null) {
                    // If detail is an object with monsters array, extract monster names
                    if (danger.detail.monsters && Array.isArray(danger.detail.monsters)) {
                        const monsterNames = danger.detail.monsters.map(m => m.name || 'Unknown Monster').join(', ');
                        detailText = monsterNames;
                    } else {
                        // Fallback: try to stringify the object
                        detailText = JSON.stringify(danger.detail);
                    }
                }
                html += `<li>${danger.type}: ${detailText}</li>`;
            });
            html += '</ul></div>';
        }
    }

    html += '</div>';
    hexInfoDiv.innerHTML = html;
}

/**
 * Handle quest completion when arriving at destination
 */
async function handleQuestCompletion(activeQuest) {
    if (!activeQuest) {
        return;
    }

    const confirmed = await showConfirm(`Complete quest: ${activeQuest.action} ${activeQuest.target}?`);
    if (!confirmed) {
        return;
    }

    // Check if index is available
    if (activeQuest.index === undefined || activeQuest.index === null) {
        showError('Quest index not available. Please refresh the page and try again.');
        console.error('Active quest missing index:', activeQuest);
        return;
    }

    try {
        const response = await gameClient.completeQuest(activeQuest.index);

        if (response.success) {
            // Show quest completion results
            showQuestCompletionResults(response);

            // Refresh state
            const stateResponse = await gameClient.getState();
            updateUI(stateResponse.state);
        }
    } catch (error) {
        showError('Failed to complete quest: ' + error.message);
    }
}

/**
 * Show quest completion results modal
 */
function showQuestCompletionResults(results) {
    const resultsDiv = document.getElementById('questCompletionResults');
    let html = '';

    // Show completed quest
    html += '<div class="quest-completed">';
    html += `<h3>Quest Completed!</h3>`;
    html += `<p class="quest-description"><strong>${results.quest.action} ${results.quest.target}</strong></p>`;
    html += '</div>';

    // Show CLUE_FOUND result
    html += '<div class="clue-found">';
    html += '<h4>Clue Found Roll:</h4>';
    html += `<p class="clue-result"><strong>${results.clue_found}</strong></p>`;
    html += '</div>';

    // Show new quest if generated
    if (results.new_quest) {
        html += '<div class="new-quest-generated">';
        html += '<h4>New Quest Generated!</h4>';
        html += `<p class="quest-description">${results.new_quest.action} ${results.new_quest.target}</p>`;
        html += `<p class="quest-location">${results.new_quest.direction_name} ${results.new_quest.distance} hexes</p>`;
        html += '</div>';
    }

    resultsDiv.innerHTML = html;
    showModal('questCompletionModal');
}

/**
 * Show exploration results modal (dangers only)
 */
function showExplorationResults(explorations) {
    const resultsDiv = document.getElementById('explorationResults');
    let html = '';

    explorations.forEach((exp, index) => {
        const hex = exp.hex;
        const results = exp.results;

        // Only show hexes with dangers
        if (results.dangers && results.dangers.length > 0) {
            html += `<div class="exploration-hex">`;
            html += `<h3>Hex (${hex.q}, ${hex.r})</h3>`;
            html += `<div class="exploration-detail"><strong>Terrain:</strong> ${hex.terrain}</div>`;
            html += `<div class="exploration-detail"><strong>Weather:</strong> ${hex.weather}</div>`;

            html += '<div class="exploration-dangers"><h4>Dangers!</h4><ul>';
            results.dangers.forEach(danger => {
                // Handle danger.detail which can be a string or an object with monsters
                let detailText = danger.detail;
                if (typeof danger.detail === 'object' && danger.detail !== null) {
                    // If detail is an object with monsters array, extract monster names
                    if (danger.detail.monsters && Array.isArray(danger.detail.monsters)) {
                        const monsterNames = danger.detail.monsters.map(m => m.name || 'Unknown Monster').join(', ');
                        detailText = monsterNames;
                    } else {
                        // Fallback: try to stringify the object
                        detailText = JSON.stringify(danger.detail);
                    }
                }
                html += `<li>${danger.type}: ${detailText}</li>`;
            });
            html += '</ul></div>';

            html += `</div>`;
        }
    });

    resultsDiv.innerHTML = html;
    showModal('explorationModal');
}

/**
 * Show brief notifications for non-danger explorations
 */
function showNonDangerNotifications(explorations) {
    let messages = [];

    explorations.forEach(exp => {
        const results = exp.results;
        const hex = exp.hex;

        if (results.discoveries && results.discoveries.length > 0) {
            results.discoveries.forEach(disc => {
                messages.push(`Discovery at (${hex.q}, ${hex.r}): ${disc.type} - ${disc.detail}`);
            });
        }

        if (results.spoor) {
            messages.push(`Spoor at (${hex.q}, ${hex.r}): ${results.spoor}`);
        }
    });

    if (messages.length > 0) {
        showMessage(messages.join('\n'));
    }
}

/**
 * Render saves list in load modal
 */
function renderSavesList(saves) {
    const savesListDiv = document.getElementById('savesList');

    if (!saves || saves.length === 0) {
        savesListDiv.innerHTML = '<p>No saved games found</p>';
        return;
    }

    let html = '';
    saves.forEach(save => {
        const date = new Date(save.timestamp).toLocaleString();
        html += `<div class="save-item" onclick="loadSave('${save.filename}')">`;
        html += `<div class="save-info">`;
        html += `<h4>${save.filename}</h4>`;
        html += `<p>Saved: ${date}</p>`;
        html += `<p>Position: ${save.player_position}, Hexes: ${save.num_hexes}, Quests: ${save.num_quests}</p>`;
        html += `</div>`;
        html += `<button class="btn btn-primary">Load</button>`;
        html += `</div>`;
    });

    savesListDiv.innerHTML = html;
}

/**
 * Load a save file
 */
async function loadSave(filename) {
    try {
        const response = await gameClient.loadGame(filename);
        updateUI(response.state);
        closeModal('loadGameModal');
        showMessage('Game loaded successfully!');
    } catch (error) {
        showError('Failed to load game: ' + error.message);
    }
}

/**
 * Setup modal handlers
 */
function setupModalHandlers() {
    // Close buttons
    document.querySelectorAll('.modal .close, .modal-close-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const modal = e.target.closest('.modal');
            if (modal) {
                modal.classList.remove('show');
            }
        });
    });

    // Click outside modal to close
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('show');
            }
        });
    });
}

/**
 * Show modal
 */
function showModal(modalId) {
    document.getElementById(modalId).classList.add('show');
}

/**
 * Close modal
 */
function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('show');
}

/**
 * Show notification message
 */
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    // Fade in
    setTimeout(() => notification.classList.add('show'), 10);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/**
 * Show confirmation dialog
 * @param {string} message - Message to display
 * @returns {Promise<boolean>} - Resolves to true if confirmed, false if cancelled
 */
function showConfirm(message) {
    return new Promise((resolve) => {
        const modal = document.getElementById('confirmModal');
        const messageEl = document.getElementById('confirmMessage');
        const yesBtn = document.getElementById('confirmYesBtn');
        const noBtn = document.getElementById('confirmNoBtn');

        messageEl.textContent = message;
        modal.classList.add('show');

        // Remove any existing event listeners
        const newYesBtn = yesBtn.cloneNode(true);
        const newNoBtn = noBtn.cloneNode(true);
        yesBtn.parentNode.replaceChild(newYesBtn, yesBtn);
        noBtn.parentNode.replaceChild(newNoBtn, noBtn);

        // Add new event listeners
        newYesBtn.addEventListener('click', () => {
            modal.classList.remove('show');
            resolve(true);
        });

        newNoBtn.addEventListener('click', () => {
            modal.classList.remove('show');
            resolve(false);
        });
    });
}

/**
 * Show item selection dialog
 * @param {Array<string>} items - Array of item names
 * @returns {Promise<string|null>} - Resolves to selected item name or null if cancelled
 */
function showItemSelection(items) {
    return new Promise((resolve) => {
        const modal = document.getElementById('itemSelectionModal');
        const listEl = document.getElementById('itemSelectionList');
        const cancelBtn = document.getElementById('itemSelectionCancelBtn');

        // Clear previous items
        listEl.innerHTML = '';

        // Create item buttons
        items.forEach(item => {
            const button = document.createElement('button');
            button.className = 'btn btn-primary item-selection-btn';
            button.textContent = item;
            button.addEventListener('click', () => {
                modal.classList.remove('show');
                resolve(item);
            });
            listEl.appendChild(button);
        });

        modal.classList.add('show');

        // Remove any existing event listeners on cancel button
        const newCancelBtn = cancelBtn.cloneNode(true);
        cancelBtn.parentNode.replaceChild(newCancelBtn, cancelBtn);

        // Add cancel handler
        newCancelBtn.addEventListener('click', () => {
            modal.classList.remove('show');
            resolve(null);
        });
    });
}

/**
 * Show success message
 */
function showMessage(message) {
    showNotification(message, 'success');
}

/**
 * Show error message
 */
function showError(message) {
    showNotification('Error: ' + message, 'error');
}

/**
 * Show dungeon discovered modal
 */
function showDungeonDiscovered(dungeon) {
    const dungeonInfoDiv = document.getElementById('dungeonInfo');

    let html = '';
    html += `<div class="dungeon-discovered">`;
    html += `<h3 class="dungeon-name">${dungeon.name}</h3>`;
    html += `<div class="dungeon-details">`;
    html += `<div class="dungeon-detail"><span class="label">Theme:</span><span class="value">${dungeon.theme}</span></div>`;
    html += `<div class="dungeon-detail"><span class="label">Type:</span><span class="value">${dungeon.dungeon_type}</span></div>`;
    html += `<div class="dungeon-detail"><span class="label">Size:</span><span class="value">${dungeon.total_rooms} rooms</span></div>`;
    html += `<div class="dungeon-detail"><span class="label">Builder:</span><span class="value">${dungeon.builder}</span></div>`;
    html += `<div class="dungeon-detail"><span class="label">Purpose:</span><span class="value">${dungeon.purpose}</span></div>`;
    html += `<div class="dungeon-detail"><span class="label">Destruction:</span><span class="value">${dungeon.destruction}</span></div>`;
    html += `</div>`;
    html += `</div>`;

    dungeonInfoDiv.innerHTML = html;
    showModal('dungeonDiscoveredModal');
}

/**
 * Handle entering dungeon
 */
async function handleEnterDungeon() {
    try {
        const response = await gameClient.enterDungeon();

        if (response.success) {
            closeModal('dungeonDiscoveredModal');

            // Get first room
            const roomResponse = await gameClient.getCurrentRoom();
            if (roomResponse.success) {
                // Check if entering the first room triggers combat
                if (roomResponse.combat_started && roomResponse.combat) {
                    // Show combat modal instead of room info
                    combatManager.showCombat(roomResponse.combat);
                    return;  // Don't show room info yet, wait for combat to resolve
                }

                showDungeonRoom(roomResponse);
            }
        }
    } catch (error) {
        showError('Failed to enter dungeon: ' + error.message);
    }
}

/**
 * Show ration consumption prompt at day's end
 */
function showRationPrompt(healAmount) {
    const healTextDiv = document.getElementById('rationHealText');
    healTextDiv.textContent = `Would you like to consume a ration to recover ${healAmount} HP?`;
    showModal('rationPromptModal');
}

/**
 * Handle consuming day ration
 */
async function handleConsumeRation() {
    try {
        const response = await gameClient.consumeDayRation();

        if (response.success) {
            closeModal('rationPromptModal');
            showMessage(`🍖 Consumed ration and recovered ${response.heal_amount} HP!`);

            // Refresh state to update HP display
            const stateResponse = await gameClient.getState();
            updateUI(stateResponse.state);
        }
    } catch (error) {
        closeModal('rationPromptModal');
        showError('Failed to consume ration: ' + error.message);
    }
}

/**
 * Handle declining ration
 */
function handleDeclineRation() {
    closeModal('rationPromptModal');
    showMessage('Rested without consuming a ration.');
}

/**
 * Show dungeon room
 */
function showDungeonRoom(roomData) {
    const roomInfoDiv = document.getElementById('dungeonRoomInfo');

    let html = '';
    html += `<div class="room-header">`;
    html += `<h3>Room ${roomData.room_number} of ${roomData.total_rooms}</h3>`;
    html += `<div class="room-progress">${roomData.dungeon.current_room + 1}/${roomData.total_rooms} explored</div>`;
    html += `</div>`;

    const contents = roomData.room.contents || {};
    const roomType = contents.type || 'Empty';
    html += `<div class="room-contents">`;
    html += `<div class="room-type"><strong>Room Type:</strong> ${roomType}</div>`;

    if (contents.type === 'Spoor') {
        html += `<div class="room-spoor"><strong>Spoor Found:</strong> ${contents.spoor}</div>`;
    } else if (contents.type === 'Discovery') {
        html += `<div class="room-discovery">`;
        const discoveryType = contents.discovery || contents.discovery_type || 'Unknown';
        html += `<strong>Discovery:</strong> ${discoveryType}`;
        if (contents.special) {
            html += ` - ${contents.special}`;
        } else if (contents.item) {
            html += ` - Item: ${contents.item}`;
        } else if (contents.discovery_detail) {
            html += ` - ${contents.discovery_detail}`;
        }
        html += `</div>`;

        if (contents.also_danger) {
            html += `<div class="room-danger alert">`;
            const dangerType = contents.danger || contents.danger_type || 'Unknown';
            html += `<strong>Also Danger!</strong> ${dangerType}`;
            if (contents.danger_detail) {
                html += ` - ${contents.danger_detail}`;
            }
            html += `</div>`;
        }
    } else if (contents.type === 'Danger') {
        html += `<div class="room-danger alert">`;
        const dangerType = contents.danger || contents.danger_type || 'Unknown';
        html += `<strong>Danger:</strong> ${dangerType}`;
        if (contents.danger_detail) {
            html += ` - ${contents.danger_detail}`;
        }
        html += `</div>`;
    }

    html += `</div>`;

    roomInfoDiv.innerHTML = html;

    // Show/hide buttons based on progress
    const nextBtn = document.getElementById('nextRoomBtn');
    const completeBtn = document.getElementById('completeDungeonBtn');

    if (roomData.room_number >= roomData.total_rooms) {
        nextBtn.style.display = 'none';
        completeBtn.style.display = 'block';
    } else {
        nextBtn.style.display = 'block';
        completeBtn.style.display = 'none';
    }

    showModal('dungeonRoomModal');
}

/**
 * Show treasure overflow modal when inventory is full
 */
function showTreasureOverflow(treasureOverflow, currentState) {
    const treasureFoundText = document.getElementById('treasureFoundText');
    const newTreasureDisplay = document.getElementById('newTreasureDisplay');
    const currentInventoryList = document.getElementById('currentInventoryList');

    const item = treasureOverflow.item;
    const slotsNeeded = treasureOverflow.requires_slots;
    const slotsAvailable = treasureOverflow.available_slots;

    treasureFoundText.textContent = `You found ${item.name} but your inventory is full! (Need ${slotsNeeded} slots, have ${slotsAvailable})`;

    // Display new treasure
    newTreasureDisplay.innerHTML = `
        <div class="treasure-item">
            <div class="item-name">${item.name}</div>
            <div class="item-details">
                <span class="item-rarity">${item.rarity || 'Common'}</span>
                ${item.is_bulky ? '<span class="item-bulky">(Bulky - 2 slots)</span>' : ''}
            </div>
            <div class="item-description">${item.description || ''}</div>
            ${item.value ? `<div class="item-value">Value: ${item.value} gold</div>` : ''}
        </div>
    `;

    // Display current inventory with click handlers
    if (currentState && currentState.player && currentState.player.inventory) {
        let inventoryHTML = '';
        currentState.player.inventory.forEach((invItem, index) => {
            const isBulky = invItem.is_bulky || invItem.name.toLowerCase().includes('plate') || invItem.name.toLowerCase().includes('chain');
            inventoryHTML += `
                <div class="inventory-item clickable" data-item-name="${invItem.name}">
                    <div class="item-name">${invItem.name}</div>
                    ${isBulky ? '<div class="item-bulky">(2 slots)</div>' : '<div>(1 slot)</div>'}
                </div>
            `;
        });
        currentInventoryList.innerHTML = inventoryHTML;

        // Add click handlers for replacement
        document.querySelectorAll('.inventory-item').forEach(itemDiv => {
            itemDiv.addEventListener('click', () => handleReplaceTreasure(itemDiv.dataset.itemName));
        });
    }

    showModal('treasureOverflowModal');
}

/**
 * Handle replacing an inventory item with treasure
 */
async function handleReplaceTreasure(itemName) {
    try {
        const response = await gameClient.collectDungeonTreasure(itemName);

        if (response.success) {
            closeModal('treasureOverflowModal');
            showMessage(`Collected ${response.collected.name}, dropped ${itemName}`);

            // Refresh state
            const stateResponse = await gameClient.getState();
            updateUI(stateResponse.state);
        }
    } catch (error) {
        showError('Failed to collect treasure: ' + error.message);
    }
}

/**
 * Handle declining treasure
 */
async function handleDeclineTreasure() {
    try {
        const response = await gameClient.collectDungeonTreasure(null);

        if (response.success) {
            closeModal('treasureOverflowModal');
            showMessage('Left treasure behind');
        }
    } catch (error) {
        showError('Failed to decline treasure: ' + error.message);
    }
}

/**
 * Handle advancing to next room
 */
async function handleNextRoom() {
    try {
        const advanceResponse = await gameClient.advanceRoom();

        if (advanceResponse.success) {
            // Check for combat
            if (advanceResponse.combat_started && advanceResponse.combat) {
                // Close dungeon modal and show combat
                closeModal('dungeonRoomModal');
                combatManager.showCombat(advanceResponse.combat);
                return;  // Don't show room info yet, wait for combat to resolve
            }

            // Check for treasure overflow
            if (advanceResponse.treasure_overflow) {
                // Get current state for inventory display
                const stateResponse = await gameClient.getState();
                showTreasureOverflow(advanceResponse.treasure_overflow, stateResponse.state);
            }

            // Show collected treasures
            if (advanceResponse.treasure_collected && advanceResponse.treasure_collected.length > 0) {
                const treasures = advanceResponse.treasure_collected.map(t => t.name).join(', ');
                showMessage(`Collected treasure: ${treasures}`);
            }

            // Show trap/hazard save results
            if (advanceResponse.trap_saves && advanceResponse.trap_saves.length > 0) {
                advanceResponse.trap_saves.forEach(save => {
                    const result = save.success ? 'avoided' : `failed (${save.damage} damage)`;
                    showMessage(`Trap: ${save.trap} - ${result}`);
                });
            }

            if (advanceResponse.hazard_saves && advanceResponse.hazard_saves.length > 0) {
                advanceResponse.hazard_saves.forEach(save => {
                    const result = save.success ? 'resisted' : `failed (${save.damage} damage)`;
                    showMessage(`Hazard: ${save.hazard} - ${result}`);
                });
            }

            const roomResponse = await gameClient.getCurrentRoom();
            if (roomResponse.success) {
                showDungeonRoom(roomResponse);
            }
        } else if (advanceResponse.can_complete) {
            // At the end, show complete button
            document.getElementById('nextRoomBtn').style.display = 'none';
            document.getElementById('completeDungeonBtn').style.display = 'block';
        }
    } catch (error) {
        showError('Failed to advance: ' + error.message);
    }
}

/**
 * Handle completing dungeon
 */
async function handleCompleteDungeon() {
    try {
        const response = await gameClient.completeDungeon();

        if (response.success) {
            closeModal('dungeonRoomModal');

            // Show quest completion results
            showQuestCompletionResults(response);

            // Refresh state
            const stateResponse = await gameClient.getState();
            updateUI(stateResponse.state);
        }
    } catch (error) {
        showError('Failed to complete dungeon: ' + error.message);
    }
}

/**
 * Use a consumable item from inventory
 */
async function useConsumableItem(itemName) {
    try {
        const response = await gameClient.useItem(itemName);

        if (response.success) {
            showMessage(`Used ${itemName}: ${response.effects.join(', ')}`);

            // Refresh state to show updated HP and inventory
            const stateResponse = await gameClient.getState();
            updateUI(stateResponse.state);
        }
    } catch (error) {
        showError('Failed to use item: ' + error.message);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', init);

// Setup dungeon event handlers
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('enterDungeonBtn').addEventListener('click', handleEnterDungeon);
    document.getElementById('nextRoomBtn').addEventListener('click', handleNextRoom);
    document.getElementById('completeDungeonBtn').addEventListener('click', handleCompleteDungeon);

    // Setup ration prompt handlers
    document.getElementById('consumeRationBtn').addEventListener('click', handleConsumeRation);
    document.getElementById('declineRationBtn').addEventListener('click', handleDeclineRation);

    // Setup treasure overflow handlers
    document.getElementById('declineTreasureBtn').addEventListener('click', handleDeclineTreasure);
});
