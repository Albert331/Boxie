class Health():
    def __init__(self,max_health=100):
        self.health = max_health
        self.health_reduction_points =15
        self.isAlive =True

    def take_damage(self,):
        self.health = max(0,self.health-self.health_reduction_points)
        if self.health <=0:
            self.isAlive = False

    def heal(self,points):
        self.health= min(100,self.health+points)    

