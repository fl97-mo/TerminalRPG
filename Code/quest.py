class Quest:
    def __init__(self, quest_data):
        self.id = quest_data["id"]
        self.name = quest_data["name"]
        self.description = quest_data["description"]
        self.objectives = [Objective(o) for o in quest_data["objectives"]]
        self.rewards = quest_data["rewards"]
        self.assigned_npc = quest_data["assigned_npc"]
        self.trigger = quest_data["trigger"]
        self.is_completed = False
        self.is_accepted = False

    def check_completion(self):
        if all(obj.completed for obj in self.objectives):
            self.is_completed = True
            return True
        return False

    def update_progress(self, trigger_type, **kwargs):
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
        elif trigger_type == "kill":
            if kwargs.get("enemy_type") != self.trigger.get("enemy"):
                return False
            count = kwargs.get("count", 1)
            for obj in self.objectives:
                obj.current += count
                if obj.current >= obj.required:
                    obj.completed = True
            return self.check_completion()
        return False

class Objective:
    def __init__(self, obj_data):
        self.id = obj_data["id"]
        self.description = obj_data["description"]
        self.current = obj_data["current"]
        self.required = obj_data["required"]
        self.completed = obj_data.get("completed", False)