class Stamina:
    def __init__(self, max_stamina=100):
        self.stamina = max_stamina
        self.punch_stamina_reduction = 20
        self.block_stamina_reduction = 0.5
        self.stamina_regen = 0.5
        self.is_blocking = False
        self.block_locked_out = False
        self.min_stamina_to_block = 10

    @staticmethod
    def pose_calc(person):
        if person[9][1] < person[0][1] and person[10][1] < person[0][1]:
            return True
        return False

    def punch(self):
        if self.stamina == 0 or self.stamina < self.punch_stamina_reduction:
            return False
        self.stamina = max(0, self.stamina - self.punch_stamina_reduction)
        return True

    def block(self, person):
        if self.stamina == 0:
            self.block_locked_out = True   

        if self.block_locked_out:
            if self.stamina >= self.min_stamina_to_block:
                self.block_locked_out = False   
                self.is_blocking = False
                return

        self.is_blocking = self.pose_calc(person)
        if self.is_blocking:
            self.stamina = max(0, self.stamina - self.block_stamina_reduction)

    def regen(self):
        if not self.is_blocking:
            self.stamina = min(100, self.stamina + self.stamina_regen)
