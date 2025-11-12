/**
 * Quest Manager UI
 * Handles quest display and management
 */

class QuestManager {
    constructor(questListElement, activeQuestElement, completedQuestListElement) {
        this.questListElement = questListElement;
        this.activeQuestElement = activeQuestElement;
        this.completedQuestListElement = completedQuestListElement;
        this.onQuestAccept = null;  // Callback for quest acceptance
        this.onDungeonReenter = null;  // Callback for dungeon re-entry
        this.playerPosition = null;  // Current player position [q, r]
    }

    /**
     * Render quest list
     */
    renderQuests(quests) {
        if (!quests || quests.length === 0) {
            this.questListElement.innerHTML = '<p class="no-quests">No quests available. Generate one!</p>';
            return;
        }

        this.questListElement.innerHTML = '';

        quests.forEach((quest, index) => {
            if (!quest.is_active) {
                const questCard = this.createQuestCard(quest);
                this.questListElement.appendChild(questCard);
            }
        });
    }

    /**
     * Render active quest
     */
    renderActiveQuest(quest, playerPosition = null) {
        if (!quest) {
            this.activeQuestElement.innerHTML = '<p class="no-quest">No active quest</p>';
            return;
        }

        this.playerPosition = playerPosition;
        const questCard = this.createQuestCard(quest, true);
        this.activeQuestElement.innerHTML = '';
        this.activeQuestElement.appendChild(questCard);
    }

    /**
     * Create quest card element
     */
    createQuestCard(quest, isActive = false) {
        const card = document.createElement('div');
        card.className = `quest-card${isActive ? ' active' : ''}`;

        // Quest title
        const title = document.createElement('h4');
        title.textContent = `${quest.action} ${quest.target}`;
        card.appendChild(title);

        // Quest description
        const description = document.createElement('p');
        description.className = 'quest-description';
        description.textContent = quest.description;
        card.appendChild(description);

        // Quest details grid
        const details = document.createElement('div');
        details.className = 'quest-details';

        const detailItems = [
            {label: 'Location', value: quest.where},
            {label: 'Opposition', value: quest.opposition},
            {label: 'Source', value: quest.source},
            {label: 'Reward', value: quest.reward}
        ];

        if (quest.direction && quest.distance) {
            detailItems.push({
                label: 'Direction',
                value: `${quest.distance} hex${quest.distance > 1 ? 'es' : ''} ${quest.direction}`
            });
        }

        // Add coordinates for active quests
        if (isActive && quest.coordinates) {
            detailItems.push({
                label: 'Coordinates',
                value: `(${quest.coordinates[0]}, ${quest.coordinates[1]})`
            });
        }

        detailItems.forEach(item => {
            const detailDiv = document.createElement('div');
            detailDiv.className = 'quest-detail';

            const label = document.createElement('span');
            label.className = 'quest-detail-label';
            label.textContent = item.label;

            const value = document.createElement('span');
            value.className = 'quest-detail-value';
            value.textContent = item.value;

            detailDiv.appendChild(label);
            detailDiv.appendChild(value);
            details.appendChild(detailDiv);
        });

        card.appendChild(details);

        // Enter dungeon button (always visible for active quests with quest destinations)
        if (isActive && quest.coordinates && this.onDungeonReenter) {
            const playerAtLocation = this.playerPosition &&
                this.playerPosition[0] === quest.coordinates[0] &&
                this.playerPosition[1] === quest.coordinates[1];

            // Always show button if quest has a destination
            const actions = document.createElement('div');
            actions.className = 'quest-actions';

            const dungeonBtn = document.createElement('button');
            dungeonBtn.className = 'btn btn-warning';

            // Enable button only if player is at the quest location
            if (playerAtLocation) {
                dungeonBtn.textContent = '🏰 Enter Dungeon';
                dungeonBtn.disabled = false;
            } else {
                dungeonBtn.textContent = '🏰 Enter Dungeon (Travel to location first)';
                dungeonBtn.disabled = true;
                dungeonBtn.title = `Go to coordinates (${quest.coordinates[0]}, ${quest.coordinates[1]})`;
            }

            dungeonBtn.style.marginTop = '10px';
            dungeonBtn.addEventListener('click', () => {
                if (playerAtLocation) {
                    this.onDungeonReenter();
                }
            });

            actions.appendChild(dungeonBtn);
            card.appendChild(actions);
        }

        // Quest actions (only for non-active quests)
        if (!isActive && this.onQuestAccept) {
            const actions = document.createElement('div');
            actions.className = 'quest-actions';

            const acceptBtn = document.createElement('button');
            acceptBtn.className = 'btn btn-primary';
            acceptBtn.textContent = 'Accept';
            acceptBtn.addEventListener('click', () => {
                this.onQuestAccept(quest.index);
            });

            actions.appendChild(acceptBtn);
            card.appendChild(actions);
        }

        return card;
    }

    /**
     * Add a new quest to the list
     */
    addQuest(quest) {
        // Remove "no quests" message if present
        const noQuests = this.questListElement.querySelector('.no-quests');
        if (noQuests) {
            noQuests.remove();
        }

        const questCard = this.createQuestCard(quest);
        this.questListElement.appendChild(questCard);
    }

    /**
     * Render completed quests list
     */
    renderCompletedQuests(completedQuests) {
        if (!completedQuests || completedQuests.length === 0) {
            this.completedQuestListElement.innerHTML = '<p class="no-completed-quests">No completed quests yet</p>';
            return;
        }

        this.completedQuestListElement.innerHTML = '';

        completedQuests.forEach((quest) => {
            const questCard = this.createCompletedQuestCard(quest);
            this.completedQuestListElement.appendChild(questCard);
        });
    }

    /**
     * Create completed quest card element (read-only display)
     */
    createCompletedQuestCard(quest) {
        const card = document.createElement('div');
        card.className = 'quest-card completed';

        // Completion order badge
        const badge = document.createElement('div');
        badge.className = 'completion-badge';
        badge.textContent = `#${quest.completion_order}`;
        card.appendChild(badge);

        // Quest title
        const title = document.createElement('h4');
        title.textContent = `${quest.action} ${quest.target}`;
        card.appendChild(title);

        // Quest description
        const description = document.createElement('p');
        description.className = 'quest-description';
        description.textContent = quest.description;
        card.appendChild(description);

        // Completion info
        const completionInfo = document.createElement('div');
        completionInfo.className = 'completion-info';

        if (quest.completion_coordinates) {
            const locationDiv = document.createElement('div');
            locationDiv.className = 'completion-detail';
            locationDiv.innerHTML = `<strong>Completed at:</strong> (${quest.completion_coordinates[0]}, ${quest.completion_coordinates[1]})`;
            completionInfo.appendChild(locationDiv);
        }

        card.appendChild(completionInfo);

        return card;
    }
}
