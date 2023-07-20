import math
import random
import pygame
import time
pygame.init()

WIDTH, HEIGHT = 800, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # WIN is the window
pygame.display.set_caption("Aim Trainer")

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT

TARGET_PADDING = 30
TARGET_DELAY = 1000
MAX_TARGETS = 5
last_target_time = 0

BG_COLOR = (0, 25, 40)
LIVES = 10
TOP_BAR_HEIGHT = 50

LABEL_FONT = pygame.font.SysFont("dejavuserif", 24)

# Color Palette
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)


class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = RED
    SECONDARY_COLOR = WHITE

    def __init__(self, x, y): # x and y are the center of the target
        self.x = x
        self.y = y
        self.size = 0
        self.growing = True # if the target is growing or shrinking

    def update(self): # update the size of the target
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE: # if the target is at max size, start shrinking
            self.growing = False

        if self.growing:
            self.size += self.GROWTH_RATE

        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win): # draw the target
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECONDARY_COLOR, (self.x, self.y), self.size*0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size*0.6)
        pygame.draw.circle(win, self.SECONDARY_COLOR, (self.x, self.y), self.size*0.4)

    def collides(self, x, y): # check if the mouse is within the target
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
    time_label = LABEL_FONT.render(f"Time: {round(elapsed_time, 2)}", 1, BLACK)
    speed = round(targets_pressed / elapsed_time, 1) if elapsed_time > 0 else 0
    speed_label = LABEL_FONT.render(f"Speed: {speed} clicks/sec", 1, BLACK)
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, BLACK)
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, BLACK)

    win.blit(time_label, (5, 5))
    win.blit(hits_label, (200, 5))
    win.blit(lives_label, (450, 5))
    win.blit(speed_label, (650, 5))

def end_game(win, elapsed_time, targets_pressed, clicks): # end the game and display the results
    win.fill(BG_COLOR)

    time_label = LABEL_FONT.render(f"Time: {round(elapsed_time, 2)}", 1, WHITE)
    speed = round(targets_pressed / elapsed_time, 1) if elapsed_time > 0 else 0
    speed_label = LABEL_FONT.render(f"Speed: {speed} clicks/sec", 1, WHITE)
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, WHITE)
    accuracy = round(targets_pressed / clicks, 2) if clicks > 0 else 0
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, WHITE)

    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(hits_label, (get_middle(hits_label), 200))
    win.blit(accuracy_label, (get_middle(accuracy_label), 300))
    win.blit(speed_label, (get_middle(speed_label), 400))

    pygame.display.update()

    run = True
    while run: # wait for the user to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                run = False
                break

def get_middle(surface): # for use in end_game to find the middle of the screen to render the endgame labels
    return WIDTH / 2 - surface.get_width() / 2

def create_target():
    x = random.randint(TARGET_PADDING, WIDTH-TARGET_PADDING)
    y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT-TARGET_PADDING)
    return Target(x, y)

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

        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                # targets.append(Target(random.randint(TARGET_PADDING, WIDTH-TARGET_PADDING), random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT-TARGET_PADDING))) # one-line less readable version of the below append

                # readable format:
                if current_time - last_target_time >= TARGET_DELAY and len(targets) < MAX_TARGETS: # if the time since the last target is greater than the delay and there are less than 10 targets on the screen, add a new target
                    targets.append(create_target())
                    last_target_time - current_time

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1
            
        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1
            
        targets = [target for target in targets if target.size > 0]
            
        if misses >= LIVES:
            end_game(WIN, time.time() - start_time, targets_pressed, clicks)
            run = False
        
        for target in targets:
            if click and target.collides(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1
                break

        draw(WIN, targets) # draw targets
        draw_top_bar(WIN, time.time() - start_time, targets_pressed, misses) # draw top bar
        pygame.display.update()
                                
    pygame.quit()

if __name__ == "__main__":
    main()