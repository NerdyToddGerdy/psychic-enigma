/**
 * Game API Client
 * Handles communication with Flask backend
 */

class GameClient {
    constructor(baseUrl = '/api') {
        this.baseUrl = baseUrl;
    }

    /**
     * Make API request
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json'
            }
        };

        const response = await fetch(url, {...defaultOptions, ...options});
        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || 'API request failed');
        }

        return data;
    }

    /**
     * Start a new game
     */
    async newGame() {
        return await this.request('/game/new', {
            method: 'POST'
        });
    }

    /**
     * Get current game state
     */
    async getState() {
        return await this.request('/game/state');
    }

    /**
     * Save current game
     */
    async saveGame(filename = null) {
        return await this.request('/game/save', {
            method: 'POST',
            body: JSON.stringify({filename})
        });
    }

    /**
     * Load a saved game
     */
    async loadGame(filename) {
        return await this.request('/game/load', {
            method: 'POST',
            body: JSON.stringify({filename})
        });
    }

    /**
     * List all save files
     */
    async listSaves() {
        return await this.request('/game/saves');
    }

    /**
     * Generate a new quest
     */
    async generateQuest() {
        return await this.request('/quest/generate', {
            method: 'POST'
        });
    }

    /**
     * Accept a quest
     */
    async acceptQuest(questIndex) {
        return await this.request('/quest/accept', {
            method: 'POST',
            body: JSON.stringify({quest_index: questIndex})
        });
    }

    /**
     * Complete a quest
     */
    async completeQuest(questIndex) {
        return await this.request('/quest/complete', {
            method: 'POST',
            body: JSON.stringify({quest_index: questIndex})
        });
    }

    /**
     * Move player to hex
     */
    async movePlayer(q, r) {
        return await this.request('/player/move', {
            method: 'POST',
            body: JSON.stringify({q, r})
        });
    }

    /**
     * Get hex information
     */
    async getHexInfo(q, r) {
        return await this.request(`/hex/${q}/${r}`);
    }

    /**
     * Enter dungeon
     */
    async enterDungeon() {
        return await this.request('/dungeon/enter', {
            method: 'POST'
        });
    }

    /**
     * Get current room
     */
    async getCurrentRoom() {
        return await this.request('/dungeon/room');
    }

    /**
     * Advance to next room
     */
    async advanceRoom() {
        return await this.request('/dungeon/advance', {
            method: 'POST'
        });
    }

    /**
     * Complete dungeon
     */
    async completeDungeon() {
        return await this.request('/dungeon/complete', {
            method: 'POST'
        });
    }

    /**
     * Collect treasure from dungeon room with optional item replacement
     */
    async collectDungeonTreasure(itemToDropName = null) {
        return await this.request('/dungeon/treasure/collect', {
            method: 'POST',
            body: JSON.stringify({item_to_drop_name: itemToDropName})
        });
    }

    // Character Management Methods

    /**
     * Create a custom character
     */
    async createCustomCharacter(characterData) {
        return await this.request('/character/create', {
            method: 'POST',
            body: JSON.stringify(characterData)
        });
    }

    /**
     * Generate a random character
     */
    async createRandomCharacter(name = null) {
        return await this.request('/character/random', {
            method: 'POST',
            body: JSON.stringify({name})
        });
    }

    /**
     * Save current character
     */
    async saveCharacter(filename = null) {
        return await this.request('/character/save', {
            method: 'POST',
            body: JSON.stringify({filename})
        });
    }

    /**
     * Load a saved character
     */
    async loadCharacter(filename) {
        return await this.request('/character/load', {
            method: 'POST',
            body: JSON.stringify({filename})
        });
    }

    /**
     * List all saved characters
     */
    async listCharacters() {
        return await this.request('/character/list');
    }

    // Combat Methods

    /**
     * Get current combat status
     */
    async getCombatStatus() {
        return await this.request('/combat/status');
    }

    /**
     * Attack in combat
     */
    async combatAttack(targetIndex = 0) {
        return await this.request('/combat/attack', {
            method: 'POST',
            body: JSON.stringify({target_index: targetIndex})
        });
    }

    /**
     * Use item in combat
     */
    async combatUseItem(itemName) {
        return await this.request('/combat/item', {
            method: 'POST',
            body: JSON.stringify({item_name: itemName})
        });
    }

    /**
     * Flee from combat
     */
    async combatFlee() {
        return await this.request('/combat/flee', {
            method: 'POST'
        });
    }

    async healPlayer() {
        return await this.request('/player/heal', {
            method: 'POST'
        });
    }

    /**
     * Use a consumable item from inventory
     */
    async useItem(itemName) {
        return await this.request('/player/use_item', {
            method: 'POST',
            body: JSON.stringify({item_name: itemName})
        });
    }

    /**
     * Consume a day ration to heal half HP
     */
    async consumeDayRation() {
        return await this.request('/player/consume_day_ration', {
            method: 'POST'
        });
    }
}
