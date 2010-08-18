
class Animation:

    def __init__(self):
        self.frames = []
        self.length = 0
        self.duration = 0
        self.cycle = True
    #enddef

    def append(self, img, duration):
        self.frames.append((img, duration))
        self.duration += duration
        self.length += 1
    #enddef
#endclass

class Slot:

    def __init__(self, animation):
        self.animation = animation
        self.rewind()
    #enddef

    def rewind(self, ticks = 0):
        self.frame = 0
        self.ticks = ticks % self.animation.duration
        self.ended = False
    #enddef

    def behave(self):
        self.ticks += 1
    #enddef

    def getSurface(self):
        while not self.ended and self.ticks > self.animation.frames[self.frame][1]:
            self.ticks -= self.animation.frames[self.frame][1]
            if self.frame+1 >= self.animation.length and not self.animation.cycle:
                self.ended = True
                break
            #endif
            self.frame += 1
            if self.frame >= self.animation.length:
                self.frame = 0
        #endwhile
        return self.animation.frames[self.frame][0]
    #enddef

    def draw(self, screen, x, y):
        screen.blit(self.getSurface(), (x, y))
    #enddef
#endclass

