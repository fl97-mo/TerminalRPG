class Quest:
    def __init__(self, quest_data):
        self.id = quest_data["id"]
        self.name = quest_data["name"]
        self.description = quest_data["description"]
        self.objectives = [Objective(o) for o in quest_data["objectives"]]
        self.rewards = quest_data["rewards"]
        self.assigned_npc = quest_data["assigned_npc"]
        self.trigger = quest_data["trigger"]
        self.status = quest_data.get("status", "locked")

    def check_completion(self):
        if all(obj.completed for obj in self.objectives):
            self.status = "completed"
            return True
        return False

    def update_progress(self, trigger_type, **kwargs):
        if self.status != "active":
            return False
        if self.trigger.get("type") != trigger_type:
            return False
        if trigger_type == "collect":
            if kwargs.get("container_id") != self.trigger.get("container_id"):
                return False
            count = kwargs.get("count", 1)
            for obj in self.objectives:
                obj.current += count
                if obj.current >= obj.required:
                    obj.completed = True
            return self.check_completion()
        # will add other triggers soon.
        return False

class Objective:
    def __init__(self, obj_data):
        self.id = obj_data["id"]
        self.description = obj_data["description"]
        self.current = obj_data["current"]
        self.required = obj_data["required"]
        self.completed = obj_data.get("completed", False)