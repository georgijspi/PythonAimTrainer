import math
import random
import pygame
import time
pygame.init()

WIDTH, HEIGHT = 800, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT

TARGET_PADDING = 30

BG_COLOR = (0, 25, 40)
LIVES = 10
TOP_BAR_HEIGHT = 50

LABEL_FONT = pygame.font.SysFont("comicsans", 24)

class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = 'red'
    SECONDARY_COLOR = 'white'

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.growing = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.growing = False

        if self.growing:
            self.size += self.GROWTH_RATE

        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECONDARY_COLOR, (self.x, self.y), self.size*0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size*0.6)
        pygame.draw.circle(win, self.SECONDARY_COLOR, (self.x, self.y), self.size*0.4)

    def collide(self, x, y):
        distance = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return distance <= self.size

def draw(win, targets):
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)
    
# currently unused, potentially useful replacement for round(elapsed_time, 2) in draw_top_bar
def format_time(seconds):
    return time.strftime("%M:%S", time.gmtime(seconds))
    
def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    # time_label = LABEL_FONT.render(f"Time: {round(elapsed_time, 2)}", 1, "black") # round(elapsed_time to 2 decimal places may be incrorrect, check_later
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")
    win.blit(time_label, (5, 5))

def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)
    
    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                targets.append(Target(random.randint(TARGET_PADDING, WIDTH-TARGET_PADDING), random.randint(TARGET_PADDING, HEIGHT-TARGET_PADDING)))

                # another method of doing the above append in a more readable format:
                # x = random.randint(TARGET_PADDING, WIDTH-TARGET_PADDING)
                # y = random.randint(TARGET_PADDING, HEIGHT-TARGET_PADDING)
                # target = Target(x, y)
                # targets.append(target) 

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1
            
        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1
        
            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1
            
        if misses >= LIVES:
            pass # end game
        
        draw(WIN, targets) # draw targets after top bar to prevent overlap
        draw_top_bar(WIN, time.time() - start_time, targets_pressed, misses)
        pygame.display.update()
                                
    pygame.quit()

if __name__ == "__main__":
    main()