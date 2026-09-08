class Punch():
    def __init__(self,x,y,w,h):
        self.punched_left=False
        self.punched_right=False

        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def see_punch(self,angle_left,angle_right,wristl,wristr):
        if 100>angle_left>70 and not self.punched_left:
            x_left,y_left = wristl
            if (self.x <= x_left <= self.x + self.w) and (self.y <= y_left <=self.y+ self.h):
                print('PUNCHEDDD from the lefttt!!!')
                self.punched_left = True
                return True
        
        if 100>angle_right>70 and not self.punched_right:
            x_right,y_right = wristr
            if (self.x <= x_right <= self.x + self.w) and (self.y <= y_right<=self.y+ self.h):
                print('PUNCHEDDD from the righttt!!!')
                self.punched_right = True
                return True
            
    def reset(self,angle_left,angle_right,wristl,wristr):
        if angle_left<40 and self.punched_left:
            x_left,y_left = wristl
            if (self.x <= x_left <= self.x + self.w) and (self.y <= y_left <=self.y+ self.h):
                print('left Punch reset')
                self.punched_left = False

        if angle_right<40 and self.punched_right:
            x_right,y_right = wristr
            if (self.x <= x_right <= self.x + self.w) and (self.y <= y_right <=self.y+ self.h):
                print('right Punch reset')
                self.punched_right = False