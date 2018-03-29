import pygame as sc


class Controls:
    def __init__(self,w=525,h=750,fps=60):
        self.done=False
        self.w=w
        self.h=h
        self.fps=fps
        self.window=sc.display.set_mode((w,h))
        self.clock=sc.time.Clock()

    def setup(self,states,start):
        self.states=states
        self.start_state=start
        self.current_state=self.states[self.start_state]

    def state_change(self):
        self.current_state.done=False
        previous, self.start_state=self.start_state,self.current_state.next 
        self.current_state.cleanup()
        self.current_state=self.states[self.start_state]
        self.current_state.startup()
        self.current_state.previous=previous

    def update(self,temp): 
        if self.current_state.quit:
            self.done=True
        elif self.current_state.done:
            print("updating state\n")
            self.state_change()
        self.current_state.update(self.window,temp)
    def event_loop(self):
        for event in sc.event.get():
            if event.type== sc.QUIT:
                self.done=True
            self.current_state.get_event(event)

    def main_loop(self):
        while not self.done:
            timer=self.clock.tick(self.fps)/100.0
            self.event_loop()
            self.update(timer)
            sc.display.update()
    






