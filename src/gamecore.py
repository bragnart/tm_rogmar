

class Raid:
    def __init__(self, id, world_name, description, difficulty, duration):
        
        self.id = id
        self.world_name = world_name
        self.description = description
        self.difficulty = difficulty
        self.duration = duration
        self.completed = False

    def __str__(self):

        return f"Мир: {self.world_name}, Описание: {self.description}, Сложность: {self.difficulty}, Длительность: {self.duration} минут"

