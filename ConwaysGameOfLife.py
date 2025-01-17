"""
 _________________________________
/  __  __                         \
| |  \/  | ___   ___              |
| | |\/| |/ _ \ / _ \             |
| | |  | | (_) | (_) |            |
| |_|  |_|\___/ \___/             |
|                                 |
\ This code was written by CalSch /
 ---------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
"""
import pixelstrip
import board 
from colors import *
import math
import random

# screen=[
#     0,1,0,0,0,0,0,0,
#     0,0,1,0,0,0,0,0,
#     1,1,1,0,0,0,0,0,
#     0,0,0,0,0,0,0,0,
#     0,0,0,0,0,0,0,0,
#     0,0,0,0,0,0,0,0,
#     0,0,0,0,0,0,0,0,
#     0,0,0,0,0,0,0,0,
# ]
screen=[]
new_screen=[]
for i in range(64):
    screen.append(random.randint(0,1)==0)
new_screen=screen.copy()
neighbor_indices=[
    -9,-8,-7, -1, 1, 7, 8, 9
]
scalar=float
def hsv_to_rgb( h:scalar, s:scalar, v:scalar, a:scalar ) -> tuple:
    if s:
        if h == 1.0: h = 0.0
        i = int(h*6.0); f = h*6.0 - i
        
        w = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        
        if i==0: return (v, t, w, a)
        if i==1: return (q, v, w, a)
        if i==2: return (w, v, t, a)
        if i==3: return (w, q, v, a)
        if i==4: return (t, w, v, a)
        if i==5: return (v, w, q, a)
    else: return (v, v, v, a)


class Coder(pixelstrip.Animation):
    def line(self, y, length):
        for i in range(length):
                if y-i >= 0 and y-i <= strip.n:
                    if i == 0:
                        strip[y-i] = (0, 0, 0, 0)                   
                    if i < length/2 and not i == 0:
                        strip[y-i] = (0, int(abs(0.5*5*math.cos(math.pi*i/(length*0.1)))), 0, 0)
                    if i == length/2:
                        strip[y-i] = (0, 15, 0, 0)
                    if i > length/2:
                        strip[y-i] = (int(abs(0.5*math.cos(math.pi*i/(length*0.1)))), 15, int(abs(0.5*5*math.cos(math.pi*i/(length*0.1)))), 0)
    def __init__(self):
        self.timeout = 0.0
        self.t=0
        print("init\n")
    def reset(self, strip):
        self.timeout = 0.0

    def draw(self, strip, delta_time):
        global screen,new_screen,neighbor_indices
        if self.is_timed_out():
            self.timeout = 0.1
            for i in range(64):
                n=0
                for j in neighbor_indices:
                    n+=screen[(i+j)%64]
                if screen[i]:
                    if n<=1 or n>=4:
                        new_screen[i]=False
                    else:
                        new_screen[i]=True
                else:
                    if n==3:
                        new_screen[i]=True
                # if screen[i]:
                #     new_screen[i]=False
                #     new_screen[min(i+1,63)]=True
                #     pass
            if random.randint(0,20)==0:
                for i in range(15):
                    new_screen[random.randint(0,63)]=random.randint(0,1)
            screen=new_screen.copy()
            # strip[self.t%64]=(self.t,0,self.t/100,0)
            for i in range(64):
                y=int(i/8)
                x=i%8
                if y%2==0:
                    x=7-x
                strip[x,y]=hsv_to_rgb((self.t/100)%1,0.75,10,0) if screen[i] else BLACK
            self.t+=1
            strip.show()


if __name__ == "__main__":
    strip = pixelstrip.PixelStrip(board.D12, width=8, height=8, bpp=4, pixel_order=pixelstrip.GRB)
    strip.timeout = 0.7

    strip.animation = Coder()

    while True:
        strip.draw()
