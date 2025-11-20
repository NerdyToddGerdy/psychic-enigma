/**
 * Shop Manager
 * Handles vendor interactions, shop UI, and buy/sell transactions
 */

class ShopManager {
    constructor(gameClient) {
        this.gameClient = gameClient;
        this.currentVendorType = null;
        this.currentInventory = null;

        // Modal elements
        this.shopModal = document.getElementById('shopModal');
        this.shopTitle = document.getElementById('shopTitle');
        this.shopPlayerCurrency = document.getElementById('shopPlayerCurrency');

        // Tab elements
        this.shopTabs = document.querySelectorAll('.shop-tab');
        this.buyTab = document.getElementById('buyTab');
        this.sellTab = document.getElementById('sellTab');

        // Content elements
        this.shopInventory = document.getElementById('shopInventory');
        this.shopPlayerInventory = document.getElementById('shopPlayerInventory');

        this.initializeEventListeners();
    }

    /**
     * Initialize event listeners for shop modal
     */
    initializeEventListeners() {
        // Close buttons
        const closeButtons = this.shopModal.querySelectorAll('.close, .modal-close-btn');
        closeButtons.forEach(btn => {
            btn.addEventListener('click', () => this.closeShop());
        });

        // Tab switching
        this.shopTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const tabName = tab.getAttribute('data-tab');
                this.switchTab(tabName);
            });
        });

        // Close on background click
        this.shopModal.addEventListener('click', (e) => {
            if (e.target === this.shopModal) {
                this.closeShop();
            }
        });
    }

    /**
     * Switch between Buy and Sell tabs
     */
    switchTab(tabName) {
        // Update tab buttons
        this.shopTabs.forEach(tab => {
            if (tab.getAttribute('data-tab') === tabName) {
                tab.classList.add('active');
            } else {
                tab.classList.remove('active');
            }
        });

        // Update tab panes
        if (tabName === 'buy') {
            this.buyTab.classList.add('active');
            this.sellTab.classList.remove('active');
        } else {
            this.sellTab.classList.add('active');
            this.buyTab.classList.remove('active');
            this.displayPlayerInventory();
        }
    }

    /**
     * Open shop for a specific vendor type
     */
    async openShop(vendorType) {
        this.currentVendorType = vendorType;
        this.shopTitle.textContent = `${vendorType}'s Shop`;

        // Show modal
        this.shopModal.style.display = 'block';

        // Reset to buy tab
        this.switchTab('buy');

        // Load vendor inventory
        await this.loadVendorInventory(vendorType);

        // Update player currency display
        this.updateCurrencyDisplay();
    }

    /**
     * Close the shop modal
     */
    closeShop() {
        this.shopModal.style.display = 'none';
        this.currentVendorType = null;
        this.currentInventory = null;

        // Refresh game state to update UI
        if (window.refreshGameState) {
            window.refreshGameState();
        }
    }

    /**
     * Load vendor inventory from API
     */
    async loadVendorInventory(vendorType) {
        try {
            this.shopInventory.innerHTML = '<p class="loading">Loading inventory...</p>';

            const response = await fetch(`/api/vendor/list?vendor_type=${vendorType}`);
            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || 'Failed to load inventory');
            }

            this.currentInventory = data.inventory;
            this.displayVendorInventory(data.inventory);

        } catch (error) {
            console.error('Error loading vendor inventory:', error);
            this.shopInventory.innerHTML = `<p class="error">${error.message}</p>`;
        }
    }

    /**
     * Display vendor inventory in the buy tab
     */
    displayVendorInventory(inventory) {
        this.shopInventory.innerHTML = '';

        // Handle Armorer (has weapons and armor categories)
        if (this.currentVendorType === 'Armorer' && inventory.weapons && inventory.armor) {
            // Weapons section
            const weaponsHeader = document.createElement('h4');
            weaponsHeader.textContent = 'Weapons';
            this.shopInventory.appendChild(weaponsHeader);

            inventory.weapons.forEach(item => {
                this.shopInventory.appendChild(this.createShopItem(item));
            });

            // Armor section
            const armorHeader = document.createElement('h4');
            armorHeader.textContent = 'Armor & Protection';
            armorHeader.style.marginTop = '20px';
            this.shopInventory.appendChild(armorHeader);

            inventory.armor.forEach(item => {
                this.shopInventory.appendChild(this.createShopItem(item));
            });
        } else {
            // Merchant or Herbalist (flat list)
            inventory.forEach(item => {
                this.shopInventory.appendChild(this.createShopItem(item));
            });
        }

        if (this.shopInventory.children.length === 0) {
            this.shopInventory.innerHTML = '<p class="no-items">No items available</p>';
        }
    }

    /**
     * Create a shop item element with buy button
     */
    createShopItem(item) {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'shop-item';

        const itemInfo = document.createElement('div');
        itemInfo.className = 'shop-item-info';

        const itemName = document.createElement('div');
        itemName.className = 'shop-item-name';
        itemName.textContent = item.name;
        itemInfo.appendChild(itemName);

        const itemDesc = document.createElement('div');
        itemDesc.className = 'shop-item-description';
        itemDesc.textContent = item.description;
        itemInfo.appendChild(itemDesc);

        itemDiv.appendChild(itemInfo);

        const itemActions = document.createElement('div');
        itemActions.className = 'shop-item-actions';

        const itemPrice = document.createElement('span');
        itemPrice.className = 'shop-item-price';
        const gold = Math.floor(item.cost_silver / 10);
        const silver = item.cost_silver % 10;
        itemPrice.textContent = gold > 0 ? `${gold}gp ${silver}sp` : `${silver}sp`;
        itemActions.appendChild(itemPrice);

        const buyButton = document.createElement('button');
        buyButton.className = 'btn btn-primary btn-sm';
        buyButton.textContent = 'Buy';
        buyButton.addEventListener('click', () => this.buyItem(item.name));
        itemActions.appendChild(buyButton);

        itemDiv.appendChild(itemActions);

        return itemDiv;
    }

    /**
     * Display party inventory in the sell tab
     */
    async displayPlayerInventory() {
        try {
            // Get current game state to access party inventory
            const response = await fetch('/api/game/state');
            const data = await response.json();

            if (!data.party_inventory) {
                this.shopPlayerInventory.innerHTML = '<p class="no-items">No items in inventory</p>';
                return;
            }

            this.shopPlayerInventory.innerHTML = '';

            const inventory = data.party_inventory;
            const sellableItems = inventory.filter(item => !item.includes('(slot 2)'));

            if (sellableItems.length === 0) {
                this.shopPlayerInventory.innerHTML = '<p class="no-items">No items to sell</p>';
                return;
            }

            sellableItems.forEach(itemName => {
                const itemDiv = this.createSellItem(itemName);
                this.shopPlayerInventory.appendChild(itemDiv);
            });

        } catch (error) {
            console.error('Error loading party inventory:', error);
            this.shopPlayerInventory.innerHTML = '<p class="error">Failed to load inventory</p>';
        }
    }

    /**
     * Create a sell item element with sell button
     */
    createSellItem(itemName) {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'shop-item';

        const itemInfo = document.createElement('div');
        itemInfo.className = 'shop-item-info';

        const itemNameDiv = document.createElement('div');
        itemNameDiv.className = 'shop-item-name';
        itemNameDiv.textContent = itemName;
        itemInfo.appendChild(itemNameDiv);

        itemDiv.appendChild(itemInfo);

        const itemActions = document.createElement('div');
        itemActions.className = 'shop-item-actions';

        const sellButton = document.createElement('button');
        sellButton.className = 'btn btn-accent btn-sm';
        sellButton.textContent = 'Sell';
        sellButton.addEventListener('click', () => this.sellItem(itemName));
        itemActions.appendChild(sellButton);

        itemDiv.appendChild(itemActions);

        return itemDiv;
    }

    /**
     * Buy an item from the vendor
     */
    async buyItem(itemName) {
        try {
            const response = await fetch('/api/vendor/buy', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    vendor_type: this.currentVendorType,
                    item_name: itemName
                })
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || 'Purchase failed');
            }

            // Show success message
            this.showNotification(`Purchased ${itemName}!`, 'success');

            // Update currency display
            this.updateCurrencyDisplay();

            // Reload inventory to show updated player inventory for sell tab
            if (this.sellTab.classList.contains('active')) {
                await this.displayPlayerInventory();
            }

        } catch (error) {
            console.error('Error buying item:', error);
            this.showNotification(error.message, 'error');
        }
    }

    /**
     * Sell an item from player inventory
     */
    async sellItem(itemName) {
        try {
            const response = await fetch('/api/vendor/sell', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    item_name: itemName
                })
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || 'Sale failed');
            }

            // Show success message
            const gold = data.gold_received;
            const silver = data.silver_received;
            const priceText = gold > 0 ? `${gold}gp ${silver}sp` : `${silver}sp`;
            this.showNotification(`Sold ${itemName} for ${priceText}!`, 'success');

            // Update currency display
            this.updateCurrencyDisplay();

            // Reload player inventory
            await this.displayPlayerInventory();

        } catch (error) {
            console.error('Error selling item:', error);
            this.showNotification(error.message, 'error');
        }
    }

    /**
     * Update party currency display in shop
     */
    async updateCurrencyDisplay() {
        try {
            const response = await fetch('/api/game/state');
            const data = await response.json();

            const gold = data.party_gold || 0;
            const silver = data.party_silver || 0;
            this.shopPlayerCurrency.textContent = `${gold}gp ${silver}sp`;
        } catch (error) {
            console.error('Error updating currency display:', error);
        }
    }

    /**
     * Show a notification message
     */
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;

        // Add to body
        document.body.appendChild(notification);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}
