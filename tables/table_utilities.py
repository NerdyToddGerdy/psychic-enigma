from datetime import datetime


def update_status_effects(self):
    """Update status effects, decrementing durations and removing expired ones"""
    effects_to_remove = []
    for effect in self.status_effects:
        if effect["duration"] > 0:
            effect["duration"] -= 1
            if effect["duration"] == 0:
                effects_to_remove.append(effect)

    for effect in effects_to_remove:
        self.status_effects.remove(effect)

    if effects_to_remove:
        self.last_modified = datetime.now().isoformat()
