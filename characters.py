class NPC:
    def __init__(self, data):
        self.npc_id = data["npc_id"]
        self.race = data["race"]
        self.role = data["role"]
        self.location = data["location"]
        self.personality = data["personality"]
        self.long_term_memory = data.get("long_term_memory", [])
        self.short_term_memory = data.get("short_term_memory", [])

    def summary(self):
        return f"You are {self.npc_id}, a {self.race} {self.role} in {self.location}."

    def personality_desc(self):
        return f"Your personality is {self.personality}."

    def memory_summary(self):
        long_mem = ", ".join([m["text"] for m in self.long_term_memory])
        short_mem = ", ".join([m["text"] for m in self.short_term_memory])
        return (
            f"You clearly remember: {long_mem or 'nothing important'}.",
            f"You briefly remember: {short_mem or 'nothing right now'}."
        )
