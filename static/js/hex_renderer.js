/**
 * Hex Grid Renderer
 * Handles SVG rendering of hexagonal grid with axial coordinates
 */

class HexRenderer {
    constructor(svgElement) {
        this.svg = svgElement;
        this.hexSize = 50;  // Radius of hexagon
        this.hexes = new Map();  // Map of "q,r" -> hex element
        this.currentPosition = [0, 0];
        this.onHexClick = null;  // Callback for hex clicks

        // Pan and zoom
        this.viewBox = {x: -500, y: -500, width: 1000, height: 1000};
        this.isPanning = false;
        this.startPan = {x: 0, y: 0};

        // Terrain colors (fallback when images don't load)
        this.terrainColors = {
            'Village': '#FFE4B5',     // Moccasin (warm light orange)
            'Grasslands': '#90EE90',  // Light green
            'Woods': '#228B22',       // Forest green
            'Hills': '#D2B48C',       // Tan
            'Mountains': '#A9A9A9',   // Dark gray
            'Swamp': '#6B8E23',       // Olive drab
            'Wasteland': '#8B7355'    // Brown
        };

        // Terrenos hex tile mapping (Portuguese filenames)
        // Note: Some filenames have encoding issues from original files
        this.terrainTiles = {
            'Grasslands': 'assets/Terrenos (Roll20)/Campos verdejantes.png',
            'Plains': 'assets/Terrenos (Roll20)/Plan"cie.png',
            'Field': 'assets/Terrenos (Roll20)/Campo.png',
            'Hills': 'assets/Terrenos (Roll20)/Colinas.png',
            'Green Hills': 'assets/Terrenos (Roll20)/Colinas Verdejantes.png',
            'Woods': 'assets/Terrenos (Roll20)/Floresta.png',
            'Forest': 'assets/Terrenos (Roll20)/Floresta.png',
            'Dense Forest': 'assets/Terrenos (Roll20)/Floresta Densa.png',
            'Forest Hills': 'assets/Terrenos (Roll20)/Floresta-Colinas.png',
            'Desert': 'assets/Terrenos (Roll20)/Deserto.png',
            'Dunes': 'assets/Terrenos (Roll20)/Dunas.png',
            'Cactus': 'assets/Terrenos (Roll20)/Cactos.png',
            'Mountains': 'assets/Terrenos (Roll20)/Montanhas.png',
            'Mountain': 'assets/Terrenos (Roll20)/Montanha.png',
            'Sea': 'assets/Terrenos (Roll20)/Mar.png',
            'Deep Sea': 'assets/Terrenos (Roll20)/Mar profundo.png',
            'Ocean': 'assets/Terrenos (Roll20)/Oceano.png',
            'Swamp': 'assets/Terrenos (Roll20)/Pハtano.png',
            'Wetlands': 'assets/Terrenos (Roll20)/Pantanal.png',
            'Wasteland': 'assets/Terrenos (Roll20)/Deserto - Vazio.png'
        };

        // Track which patterns have been loaded
        this.loadedPatterns = new Set();

        this.setupPanZoom();
    }

    /**
     * Get emoji icon for settlement type
     */
    getSettlementEmoji(settlementType) {
        const emojiMap = {
            'Refugee': '🏕️',
            'Village': '🏘️',
            'Town': '🏛️',
            'Outpost': '🏰',
            'City': '🏙️'
        };
        return emojiMap[settlementType] || '🏘️';  // Default to village icon
    }

    /**
     * Get emoji icon for terrain type
     */
    getTerrainEmoji(terrainType) {
        const emojiMap = {
            'Mountains': '🏔️',
            'Woods': '🌲',
            'Grasslands': '🌾',
            'Hills': '⛰️',
            'Swamp': '🌿',
            'Wasteland': '🏜️',
            'River': '🌊',
            'Lake': '💧'
        };
        return emojiMap[terrainType] || null;  // Return null if no emoji for terrain
    }

    /**
     * Setup pan and zoom functionality
     */
    setupPanZoom() {
        this.svg.addEventListener('mousedown', (e) => {
            if (e.target === this.svg || e.target.tagName === 'svg') {
                this.isPanning = true;
                this.startPan = {x: e.clientX, y: e.clientY};
                this.svg.style.cursor = 'grabbing';
            }
        });

        this.svg.addEventListener('mousemove', (e) => {
            if (this.isPanning) {
                const dx = (e.clientX - this.startPan.x) * (this.viewBox.width / this.svg.clientWidth);
                const dy = (e.clientY - this.startPan.y) * (this.viewBox.height / this.svg.clientHeight);

                this.viewBox.x -= dx;
                this.viewBox.y -= dy;

                this.updateViewBox();
                this.startPan = {x: e.clientX, y: e.clientY};
            }
        });

        this.svg.addEventListener('mouseup', () => {
            this.isPanning = false;
            this.svg.style.cursor = 'grab';
        });

        this.svg.addEventListener('mouseleave', () => {
            this.isPanning = false;
            this.svg.style.cursor = 'grab';
        });

        // Zoom with mouse wheel
        this.svg.addEventListener('wheel', (e) => {
            e.preventDefault();
            const zoom = e.deltaY > 0 ? 1.1 : 0.9;
            const centerX = this.viewBox.x + this.viewBox.width / 2;
            const centerY = this.viewBox.y + this.viewBox.height / 2;

            this.viewBox.width *= zoom;
            this.viewBox.height *= zoom;
            this.viewBox.x = centerX - this.viewBox.width / 2;
            this.viewBox.y = centerY - this.viewBox.height / 2;

            this.updateViewBox();
        });
    }

    /**
     * Update SVG viewBox
     */
    updateViewBox() {
        this.svg.setAttribute('viewBox',
            `${this.viewBox.x} ${this.viewBox.y} ${this.viewBox.width} ${this.viewBox.height}`);
    }

    /**
     * Convert axial coordinates to pixel coordinates
     */
    axialToPixel(q, r) {
        const x = this.hexSize * (3/2 * q);
        const y = this.hexSize * (Math.sqrt(3)/2 * q + Math.sqrt(3) * r);
        return {x, y};
    }

    /**
     * Generate SVG path for hexagon (flat-top orientation)
     */
    hexagonPath(cx, cy, size) {
        const points = [];
        for (let i = 0; i < 6; i++) {
            // Start at 0 degrees for flat-top orientation
            const angle = Math.PI / 180 * (60 * i);
            const x = cx + size * Math.cos(angle);
            const y = cy + size * Math.sin(angle);
            points.push(`${x},${y}`);
        }
        return `M ${points.join(' L ')} Z`;
    }

    /**
     * Create clipPath for a hexagon
     */
    createHexClipPath(clipPathId, cx, cy) {
        // Check if clipPath already exists
        if (document.getElementById(clipPathId)) {
            return;
        }

        // Create defs element if it doesn't exist
        let defs = this.svg.querySelector('defs');
        if (!defs) {
            defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
            this.svg.insertBefore(defs, this.svg.firstChild);
        }

        // Create clipPath
        const clipPath = document.createElementNS('http://www.w3.org/2000/svg', 'clipPath');
        clipPath.setAttribute('id', clipPathId);

        // Create hexagon path for clipping
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', this.hexagonPath(cx, cy, this.hexSize));

        clipPath.appendChild(path);
        defs.appendChild(clipPath);
    }

    /**
     * Get or create SVG pattern for terrain tile
     */
    getTerrainPattern(terrain) {
        const patternId = `pattern-${terrain.replace(/\s+/g, '-')}`;

        // Check if pattern already exists
        if (this.loadedPatterns.has(patternId)) {
            return `url(#${patternId})`;
        }

        // Get tile image path
        const tilePath = this.terrainTiles[terrain];
        if (!tilePath) {
            return null; // No tile for this terrain, use color fallback
        }

        // Create defs element if it doesn't exist
        let defs = this.svg.querySelector('defs');
        if (!defs) {
            defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
            this.svg.insertBefore(defs, this.svg.firstChild);
        }

        // Create pattern with userSpaceOnUse for pixel-perfect tiling
        const pattern = document.createElementNS('http://www.w3.org/2000/svg', 'pattern');
        pattern.setAttribute('id', patternId);
        pattern.setAttribute('patternUnits', 'userSpaceOnUse');
        pattern.setAttribute('patternContentUnits', 'userSpaceOnUse');

        // Pattern size matches hex dimensions for one full tile per hex
        const patternWidth = this.hexSize * 2;
        const patternHeight = this.hexSize * Math.sqrt(3);
        pattern.setAttribute('width', patternWidth);
        pattern.setAttribute('height', patternHeight);

        // Create image element that fills the entire pattern space
        const image = document.createElementNS('http://www.w3.org/2000/svg', 'image');
        image.setAttribute('href', tilePath);
        image.setAttribute('x', '0');
        image.setAttribute('y', '0');
        image.setAttribute('width', patternWidth);
        image.setAttribute('height', patternHeight);
        image.setAttribute('preserveAspectRatio', 'xMidYMid slice');

        pattern.appendChild(image);
        defs.appendChild(pattern);

        this.loadedPatterns.add(patternId);
        return `url(#${patternId})`;
    }

    /**
     * Render a single hex
     */
    renderHex(hexData) {
        const key = `${hexData.q},${hexData.r}`;
        const pos = this.axialToPixel(hexData.q, hexData.r);

        // Remove existing hex if any
        const existing = this.hexes.get(key);
        if (existing) {
            existing.remove();
        }

        // Create hex group
        const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        group.setAttribute('data-q', hexData.q);
        group.setAttribute('data-r', hexData.r);

        // Add tooltip with hex information
        const title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
        let tooltipText = `${hexData.terrain || 'Unknown'} (${hexData.q}, ${hexData.r})`;
        if (hexData.settlement_type) {
            tooltipText = `${hexData.settlement_type} - ${tooltipText}`;
        }
        if (hexData.water) {
            tooltipText += ' [Water]';
        }
        title.textContent = tooltipText;
        group.appendChild(title);

        // Get clipPath ID for this hex
        const clipPathId = `clip-hex-${hexData.q}-${hexData.r}`;

        // Create clipPath for this hex (if explored with terrain image)
        const tilePath = hexData.explored && hexData.terrain ? this.terrainTiles[hexData.terrain] : null;
        if (tilePath) {
            this.createHexClipPath(clipPathId, pos.x, pos.y);

            // Add terrain image clipped to hex shape
            const image = document.createElementNS('http://www.w3.org/2000/svg', 'image');
            image.setAttribute('href', tilePath);

            // Calculate image bounds to cover the hex
            const imgSize = this.hexSize * 2.5; // Slightly larger to ensure coverage
            image.setAttribute('x', pos.x - imgSize / 2);
            image.setAttribute('y', pos.y - imgSize / 2);
            image.setAttribute('width', imgSize);
            image.setAttribute('height', imgSize);
            image.setAttribute('preserveAspectRatio', 'xMidYMid slice');
            image.setAttribute('clip-path', `url(#${clipPathId})`);
            group.appendChild(image);
        }

        // Create hexagon path for border and fallback fill
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', this.hexagonPath(pos.x, pos.y, this.hexSize));

        // Determine fill and stroke
        let fill = 'none'; // No fill if image is shown
        let strokeColor = '#757575';
        let strokeWidth = 2;
        let opacity = 1;

        if (hexData.explored && hexData.terrain) {
            // Image handles fill, path is just border
            if (!tilePath) {
                // Fallback to color if no tile available
                fill = this.terrainColors[hexData.terrain] || '#90EE90';
            }
            strokeColor = '#333';
        } else if (hexData.revealed) {
            // Gray for revealed but not explored
            fill = '#BDBDBD';
            strokeColor = '#757575';
            opacity = 0.7;
        } else {
            // Unrevealed - show gray
            fill = '#BDBDBD';
        }

        // Current position gets special highlighting
        if (hexData.q === this.currentPosition[0] && hexData.r === this.currentPosition[1]) {
            strokeColor = '#FFA000';
            strokeWidth = 4;
        }

        // Apply styling
        path.setAttribute('fill', fill);
        path.setAttribute('stroke', strokeColor);
        path.setAttribute('stroke-width', strokeWidth);
        path.setAttribute('opacity', opacity);

        // Ensure path captures pointer events even when fill is 'none'
        path.style.pointerEvents = 'all';

        // Water indication (dashed border)
        if (hexData.water) {
            path.setAttribute('stroke', '#2196F3');
            path.setAttribute('stroke-dasharray', '4');
        }

        // Settlement glow effect (golden glow for settlements)
        if (hexData.settlement_type) {
            path.setAttribute('stroke', '#FFD700');  // Gold color
            path.setAttribute('stroke-width', 3);
            path.style.filter = 'drop-shadow(0 0 8px rgba(255, 215, 0, 0.6))';
        }

        // Add click handler
        if (hexData.revealed || hexData.explored) {
            path.style.cursor = 'pointer';
            path.addEventListener('click', () => {
                if (this.onHexClick) {
                    this.onHexClick(hexData.q, hexData.r, hexData);
                }
            });
        }

        group.appendChild(path);

        // Only show emojis on explored tiles
        if (hexData.explored) {
            // Add settlement emoji icon (only if settlement exists)
            if (hexData.settlement_type) {
                const settlementEmoji = this.getSettlementEmoji(hexData.settlement_type);
                const icon = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                icon.setAttribute('x', pos.x);
                icon.setAttribute('y', pos.y - 10);
                icon.setAttribute('text-anchor', 'middle');
                icon.setAttribute('dominant-baseline', 'middle');
                icon.setAttribute('class', 'settlement-icon');
                icon.setAttribute('font-size', '24');
                icon.textContent = settlementEmoji;
                group.appendChild(icon);
            }

            // Add dungeon emoji icon (crossed swords ⚔️)
            if (hexData.has_dungeon) {
                const dungeonIcon = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                dungeonIcon.setAttribute('x', pos.x);
                dungeonIcon.setAttribute('y', pos.y + 15);  // Below settlement
                dungeonIcon.setAttribute('text-anchor', 'middle');
                dungeonIcon.setAttribute('dominant-baseline', 'middle');
                dungeonIcon.setAttribute('class', 'dungeon-icon');
                dungeonIcon.setAttribute('font-size', '24');
                dungeonIcon.textContent = '⚔️';
                group.appendChild(dungeonIcon);
            }
        }

        this.svg.appendChild(group);
        this.hexes.set(key, group);
    }

    /**
     * Render all hexes
     */
    renderGrid(hexesData, playerPosition) {
        // Clear existing hexes
        this.clear();

        // Update current position
        if (playerPosition) {
            this.currentPosition = playerPosition;
        }

        // Render each hex
        hexesData.forEach(hexData => {
            this.renderHex(hexData);
        });

        // Center view on player if first render
        if (this.hexes.size > 0) {
            this.centerOnPlayer();
        }
    }

    /**
     * Center view on player position
     */
    centerOnPlayer() {
        const pos = this.axialToPixel(this.currentPosition[0], this.currentPosition[1]);
        const centerX = pos.x;
        const centerY = pos.y;

        this.viewBox.x = centerX - this.viewBox.width / 2;
        this.viewBox.y = centerY - this.viewBox.height / 2;
        this.updateViewBox();
    }

    /**
     * Update a single hex
     */
    updateHex(hexData) {
        this.renderHex(hexData);
    }

    /**
     * Clear all hexes
     */
    clear() {
        this.hexes.forEach(hex => hex.remove());
        this.hexes.clear();

        // Clean up clipPaths to avoid memory leaks
        const defs = this.svg.querySelector('defs');
        if (defs) {
            const clipPaths = defs.querySelectorAll('clipPath[id^="clip-hex-"]');
            clipPaths.forEach(cp => cp.remove());
        }
    }

    /**
     * Highlight a specific hex (for quest destinations)
     */
    highlightHex(q, r, highlight = true) {
        const key = `${q},${r}`;
        const group = this.hexes.get(key);

        if (group) {
            const path = group.querySelector('path');
            if (highlight) {
                path.style.stroke = '#FF9800';
                path.style.strokeWidth = '4';
            } else {
                path.style.stroke = '';
                path.style.strokeWidth = '';
            }
        }
    }
}
