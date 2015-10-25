
class Animation:

    def __init__(self):
        self.frames = []
        self.length = 0
        self.duration = 0
        self.cycle = True

    def append(self, img, duration):
        self.frames.append((img, duration))
        self.duration += duration
        self.length += 1
#endclass

class Slot:

    def __init__(self, animation):
        self.animation = animation
        self.rewind()

    def rewind(self, ticks = 0):
        self.frame = 0
        self.ticks = ticks % self.animation.duration
        self.ended = False

    def behave(self):
        self.ticks += 1

    def getSurface(self):
        while not self.ended and self.ticks > self.animation.frames[self.frame][1]:
            self.ticks -= self.animation.frames[self.frame][1]
            if self.frame+1 >= self.animation.length and not self.animation.cycle:
                self.ended = True
                break
            self.frame += 1
            if self.frame >= self.animation.length:
                self.frame = 0
        return self.animation.frames[self.frame][0]

    def draw(self, screen, x, y):
        screen.blit(self.getSurface(), (x, y))

    def get_rect(self):
        return self.getSurface().get_rect()
#endclass

