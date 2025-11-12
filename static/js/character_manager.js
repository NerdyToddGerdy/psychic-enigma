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
    showModal() {
        this.modal.style.display = 'block';
        this.loadSavedCharacters();

        // Show current character if exists, otherwise show options
        if (this.currentCharacter) {
            this.displayCurrentCharacter();
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
                this.displayCurrentCharacter();
                this.showNotification('Random character created!', 'success');

                // Refresh game state to update everything
                if (window.refreshGameState) {
                    await window.refreshGameState();
                }
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

        const characterData = {
            name: name,
            race: document.getElementById('customCharRace').value.trim() || 'Human',
            character_type: document.getElementById('customCharClass').value.trim() || 'Adventurer',
            hp: parseInt(document.getElementById('customCharHP').value) || 10,
            ac: parseInt(document.getElementById('customCharAC').value) || 10,
            attack_bonus: parseInt(document.getElementById('customCharAttack').value) || 0,
            weapon: document.getElementById('customCharWeapon').value.trim() || undefined,
            armor: document.getElementById('customCharArmor').value.trim() || undefined
        };

        try {
            const response = await this.gameClient.createCustomCharacter(characterData);

            if (response.success) {
                this.currentCharacter = response.character;
                this.displayCurrentCharacter();
                this.showNotification('Custom character created!', 'success');

                // Clear form
                this.clearCustomForm();

                // Refresh game state to update everything
                if (window.refreshGameState) {
                    await window.refreshGameState();
                }
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
     * Display the current character stats
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

        // Show character display, hide options
        document.getElementById('currentCharacter').style.display = 'block';
        document.getElementById('characterOptions').style.display = 'none';
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
        document.getElementById('customCharHP').value = '';
        document.getElementById('customCharAC').value = '';
        document.getElementById('customCharAttack').value = '';
        document.getElementById('customCharWeapon').value = '';
        document.getElementById('customCharArmor').value = '';
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
