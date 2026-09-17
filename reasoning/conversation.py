class ConversationManager:
    def __init__(self):
        self.memory = []
        self.slots = {
            "soil_ph": None,
            "organic_carbon_pct": None,
            "rainfall_mm": None,
            "land_use": None,
            "species_richness": None,
            "pollution_level": None,
            "moisture": None,
            "habitat_diversity": None,
            "region": None,
        }

    def update_slots(self, data: dict):
        for key, value in data.items():
            if key in self.slots and value is not None:
                self.slots[key] = value

    def get_missing_slots(self):
        required = ["soil_ph", "organic_carbon_pct", "rainfall_mm", "land_use", "species_richness", "pollution_level", "region"]
        return [k for k in required if self.slots.get(k) is None]

    def add_message(self, role, content):
        self.memory.append({"role": role, "content": content})

    def get_context(self):
        return {"slots": self.slots, "memory": self.memory[-5:]}