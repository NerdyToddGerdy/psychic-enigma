/**
 * Character Manager
 * Handles character creation, loading, and display
 */

class CharacterManager {
    constructor(gameClient) {
        this.gameClient = gameClient;
        this.currentCharacter = null;
        this.modal = document.getElementById('characterModal');
        this.setupEventListeners();
    }

    /**
     * Setup event listeners for character modal
     */
    setupEventListeners() {
        // Modal close buttons
        const closeButtons = this.modal.querySelectorAll('.close, .modal-close-btn');
        closeButtons.forEach(btn => {
            btn.addEventListener('click', () => this.closeModal());
        });

        // Random character creation
        document.getElementById('createRandomBtn').addEventListener('click', () => {
            this.createRandomCharacter();
        });

        // Custom character creation
        document.getElementById('createCustomBtn').addEventListener('click', () => {
            this.createCustomCharacter();
        });

        // Save character button
        document.getElementById('saveCharacterBtn').addEventListener('click', () => {
            this.saveCurrentCharacter();
        });

        // Close modal on outside click
        window.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.closeModal();
            }
        });
    }

    /**
     * Show the character modal
     */
    async showModal() {
        this.modal.style.display = 'block';
        this.loadSavedCharacters();

        // Get current game state to check party size
        const state = await this.gameClient.getGameState();
        const party = state?.party || [];
        const partySize = party.length;

        // Show party members and creation options based on party size
        if (partySize > 0) {
            this.displayParty(party, partySize);
            // Show/hide creation options based on party size
            if (partySize < 3) {
                document.getElementById('characterOptions').style.display = 'block';
            } else {
                document.getElementById('characterOptions').style.display = 'none';
            }
        } else {
            document.getElementById('currentCharacter').style.display = 'none';
            document.getElementById('characterOptions').style.display = 'block';
        }
    }

    /**
     * Close the character modal
     */
    closeModal() {
        this.modal.style.display = 'none';
    }

    /**
     * Create a random character
     */
    async createRandomCharacter() {
        const name = document.getElementById('randomCharName').value.trim();

        try {
            const response = await this.gameClient.createRandomCharacter(name || undefined);

            if (response.success) {
                this.currentCharacter = response.character;

                // Show success with party size info
                const partySize = response.party_size || 1;
                this.showNotification(`Character created! Party: ${partySize}/3`, 'success');

                // Refresh game state to update everything
                if (window.refreshGameState) {
                    await window.refreshGameState();
                }

                // Refresh modal to show updated party
                await this.showModal();
            } else {
                this.showNotification('Failed to create character: ' + response.error, 'error');
            }
        } catch (error) {
            this.showNotification('Error creating character: ' + error.message, 'error');
        }
    }

    /**
     * Create a custom character
     */
    async createCustomCharacter() {
        const name = document.getElementById('customCharName').value.trim();

        if (!name) {
            this.showNotification('Character name is required', 'error');
            return;
        }

        // Collect ability scores with validation (3-18 range)
        const strength = parseInt(document.getElementById('customCharSTR').value) || 10;
        const dexterity = parseInt(document.getElementById('customCharDEX').value) || 10;
        const willpower = parseInt(document.getElementById('customCharWIL').value) || 10;
        const toughness = parseInt(document.getElementById('customCharTOU').value) || 10;

        // Validate ability scores are in range
        const abilityScores = [
            { name: 'Strength', value: strength },
            { name: 'Dexterity', value: dexterity },
            { name: 'Willpower', value: willpower },
            { name: 'Toughness', value: toughness }
        ];

        for (const ability of abilityScores) {
            if (ability.value < 3 || ability.value > 18) {
                this.showNotification(`${ability.name} must be between 3 and 18`, 'error');
                return;
            }
        }

        const characterData = {
            name: name,
            race: document.getElementById('customCharRace').value.trim() || 'Human',
            character_type: document.getElementById('customCharClass').value.trim() || 'Adventurer',

            // Core ability scores (will auto-calculate HP, AC, attack)
            strength: strength,
            dexterity: dexterity,
            willpower: willpower,
            toughness: toughness,

            // Special skill
            special_skill: document.getElementById('customCharSkill').value || undefined,

            // Equipment
            weapon: document.getElementById('customCharWeapon').value.trim() || undefined,
            armor: document.getElementById('customCharArmor').value.trim() || undefined,
            shield: document.getElementById('customCharShield').value.trim() || undefined,
            helmet: document.getElementById('customCharHelmet').value.trim() || undefined,

            // Progression
            level: parseInt(document.getElementById('customCharLevel').value) || 1,
            xp: parseInt(document.getElementById('customCharXP').value) || 0,

            // Currency
            gold: parseInt(document.getElementById('customCharGold').value) || 0,
            silver: parseInt(document.getElementById('customCharSilver').value) || 0
        };

        try {
            const response = await this.gameClient.createCustomCharacter(characterData);

            if (response.success) {
                this.currentCharacter = response.character;

                // Show success with party size info
                const partySize = response.party_size || 1;
                this.showNotification(`Character created! Party: ${partySize}/3`, 'success');

                // Clear form
                this.clearCustomForm();

                // Refresh game state to update everything
                if (window.refreshGameState) {
                    await window.refreshGameState();
                }

                // Refresh modal to show updated party
                await this.showModal();
            } else {
                this.showNotification('Failed to create character: ' + response.error, 'error');
            }
        } catch (error) {
            this.showNotification('Error creating character: ' + error.message, 'error');
        }
    }

    /**
     * Load a saved character
     */
    async loadCharacter(filename) {
        try {
            const response = await this.gameClient.loadCharacter(filename);

            if (response.success) {
                this.currentCharacter = response.character;
                this.displayCurrentCharacter();
                this.showNotification('Character loaded!', 'success');

                // Refresh game state to update everything
                if (window.refreshGameState) {
                    await window.refreshGameState();
                }
            } else {
                this.showNotification('Failed to load character: ' + response.error, 'error');
            }
        } catch (error) {
            this.showNotification('Error loading character: ' + error.message, 'error');
        }
    }

    /**
     * Save the current character
     */
    async saveCurrentCharacter() {
        if (!this.currentCharacter) {
            this.showNotification('No character to save', 'error');
            return;
        }

        try {
            const response = await this.gameClient.saveCharacter();

            if (response.success) {
                this.showNotification('Character saved!', 'success');
                this.loadSavedCharacters(); // Refresh list
            } else {
                this.showNotification('Failed to save character: ' + response.error, 'error');
            }
        } catch (error) {
            this.showNotification('Error saving character: ' + error.message, 'error');
        }
    }

    /**
     * Load and display list of saved characters
     */
    async loadSavedCharacters() {
        const container = document.getElementById('savedCharactersList');

        try {
            const response = await this.gameClient.listCharacters();

            if (response.success && response.characters.length > 0) {
                container.innerHTML = '';

                response.characters.forEach(char => {
                    const charItem = document.createElement('div');
                    charItem.className = 'saved-character-item';
                    charItem.innerHTML = `
                        <div class="char-info">
                            <strong>${char.name}</strong>
                            <span>${char.race} ${char.character_type}</span>
                            <span>HP: ${char.hp_current}/${char.hp_max}, AC: ${char.ac}</span>
                        </div>
                        <button class="btn btn-small btn-primary load-char-btn" data-filename="${char.filename}">
                            Load
                        </button>
                    `;

                    const loadBtn = charItem.querySelector('.load-char-btn');
                    loadBtn.addEventListener('click', () => {
                        this.loadCharacter(char.filename);
                    });

                    container.appendChild(charItem);
                });
            } else {
                container.innerHTML = '<p class="no-characters">No saved characters found</p>';
            }
        } catch (error) {
            container.innerHTML = '<p class="error-text">Error loading characters</p>';
        }
    }

    /**
     * Display the party members
     */
    displayParty(party, partySize) {
        const container = document.getElementById('currentCharacter');

        if (!party || party.length === 0) {
            container.style.display = 'none';
            return;
        }

        // Build HTML for all party members
        let partyHTML = `<h3>Party (${partySize}/3)</h3>`;

        party.forEach((char, index) => {
            partyHTML += `
                <div class="party-member" style="margin-bottom: 15px; padding: 10px; background: #2a2a2a; border-radius: 5px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>${char.name}</strong> - Level ${char.level || 1}
                            <div style="font-size: 12px; color: #888;">
                                ${char.race} ${char.character_type}
                            </div>
                        </div>
                        <div style="text-align: right; font-size: 12px;">
                            <div>HP: ${char.hp_current}/${char.hp_max}</div>
                            <div>AC: ${char.ac} | ATK: +${char.attack_bonus}</div>
                        </div>
                    </div>
                </div>
            `;
        });

        if (partySize < 3) {
            partyHTML += `<p style="color: #888; font-size: 12px; margin-top: 10px;">You can add ${3 - partySize} more character${3 - partySize !== 1 ? 's' : ''} to your party.</p>`;
        } else {
            partyHTML += `<p style="color: #888; font-size: 12px; margin-top: 10px;">Your party is full (3/3).</p>`;
        }

        container.innerHTML = partyHTML;
        container.style.display = 'block';
        document.getElementById('saveCharacterBtn').style.display = 'inline-block';
    }

    /**
     * Display the current character stats (legacy, now uses displayParty)
     */
    displayCurrentCharacter() {
        if (!this.currentCharacter) return;

        const char = this.currentCharacter;

        // Update character display
        document.getElementById('charName').textContent = char.name;
        document.getElementById('charRace').textContent = char.race;
        document.getElementById('charClass').textContent = char.character_type;
        document.getElementById('charHP').textContent = `${char.hp_current}/${char.hp_max}`;
        document.getElementById('charAC').textContent = char.ac;
        document.getElementById('charAttack').textContent = `+${char.attack_bonus}`;
        document.getElementById('charWeapon').textContent = char.equipment?.weapon || '-';
        document.getElementById('charArmor').textContent = char.equipment?.armor || '-';

        // Show character display, don't hide options anymore (party system handles it)
        document.getElementById('currentCharacter').style.display = 'block';
        document.getElementById('saveCharacterBtn').style.display = 'inline-block';
    }

    /**
     * Update character display (for HP changes, etc.)
     */
    updateCharacterDisplay(character) {
        if (character) {
            this.currentCharacter = character;
        }
        this.displayCurrentCharacter();
    }

    /**
     * Clear custom character form
     */
    clearCustomForm() {
        document.getElementById('customCharName').value = '';
        document.getElementById('customCharRace').value = '';
        document.getElementById('customCharClass').value = '';

        // Clear ability scores
        document.getElementById('customCharSTR').value = '';
        document.getElementById('customCharDEX').value = '';
        document.getElementById('customCharWIL').value = '';
        document.getElementById('customCharTOU').value = '';

        // Clear special skill
        document.getElementById('customCharSkill').value = '';

        // Clear equipment
        document.getElementById('customCharWeapon').value = '';
        document.getElementById('customCharArmor').value = '';
        document.getElementById('customCharShield').value = '';
        document.getElementById('customCharHelmet').value = '';

        // Clear progression
        document.getElementById('customCharLevel').value = '';
        document.getElementById('customCharXP').value = '';

        // Clear currency
        document.getElementById('customCharGold').value = '';
        document.getElementById('customCharSilver').value = '';
    }

    /**
     * Show notification message
     */
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;

        // Add to document
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
     * Check if player has a character
     */
    hasCharacter() {
        return this.currentCharacter !== null;
    }

    /**
     * Get current character
     */
    getCharacter() {
        return this.currentCharacter;
    }
}
