
class Animation:

    def __init__(self, frames = None):
        if frames != None:
            self.frames = frames
        else:
            self.frames = []
        self.length = len(self.frames)
        self.cycle = True
    #enddef

    def append(self, img, duration):
        self.frames.append((img, duration))
        self.length += 1
    #enddef
#endclass

class Slot:

    def __init__(self, animation):
        self.animation = animation
        self.rewind()
    #enddef

    def rewind(self, frame = 0):
        self.frame = frame
        self.ticks = 0
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

