import core
import data

class Menu:
    opts = []
    active = 0
    height = 0
    skipSpace = 20
    spanSpace = 5

    def __init__(self):
        pass
    #enddef

    def draw(self):
        y = (core.height - (self.height + (len(self.opts)-1)*self.spanSpace))/2
        for i, e in enumerate(self.opts):
            if e[0] == None:
                y += self.skipSpace
                continue
            sf = e[0]
            if (i == self.active):
                sf = e[1]
            r = sf.get_rect()
            core.screen.blit(sf, ((core.width-r.width)/2, y))
            y += r.height + self.spanSpace
        #endfor
    #enddef

    def behave(self):
        dir = 0
        if core.controls.down:
            dir = +1
            core.controls.down = False
        if core.controls.up:
            dir = -1
            core.controls.up = False
        self.active += dir
        while self.active>0 and self.active < len(self.opts) and self.opts[self.active][0]==None:
            self.active += dir
        if self.active<0:
            self.active = len(self.opts) - 1
        if self.active >= len(self.opts):
            self.active = 0
        if core.controls.fire:
            core.controls.fire = False
            if self.opts[self.active][2]:
                self.opts[self.active][2]()
        #endif
    # enddef

    def set(self, no, text, callback = None):
        if len(self.opts) <= no:
            addLen = 1+no-len(self.opts)
            self.opts += [(None, )]*(addLen)
            self.height += (addLen - 1) * self.skipSpace
        self.opts[no] = \
            ( data.mnuFont1.render(text, True, (200,50,50)).convert_alpha(), \
              data.mnuFont2.render(text, True, (200,50,50)).convert_alpha(), \
              callback )
        self.height += self.opts[no][0].get_rect().height
    #enddef
#endclass
