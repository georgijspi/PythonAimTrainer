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

BG_COLOR = (0, 25, 40)
LIVES = 10
TOP_BAR_HEIGHT = 50

LABEL_FONT = pygame.font.SysFont("dejavuserif", 24)

class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = 'red'
    SECONDARY_COLOR = 'white'

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

    def collide(self, x, y): # check if the mouse is within the target
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
    time_label = LABEL_FONT.render(f"Time: {round(elapsed_time, 2)}", 1, "black")
    # time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")

    speed = round(targets_pressed / elapsed_time, 1) if elapsed_time > 0 else 0
    speed_label = LABEL_FONT.render(f"Speed: {speed} clicks/sec", 1, "black")

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")

    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")

    win.blit(time_label, (5, 5))
    win.blit(hits_label, (200, 5))
    win.blit(lives_label, (450, 5))
    win.blit(speed_label, (650, 5))

def end_game(win, elapsed_time, targets_pressed, clicks): # end the game and display the results
    win.fill(BG_COLOR)

    time_label = LABEL_FONT.render(f"Time: {round(elapsed_time, 2)}", 1, "white")

    speed = round(targets_pressed / elapsed_time, 1) if elapsed_time > 0 else 0
    speed_label = LABEL_FONT.render(f"Speed: {speed} clicks/sec", 1, "white")

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")

    accuracy = round(targets_pressed / clicks, 2) if clicks > 0 else 0
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")

    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(hits_label, (get_middle(hits_label), 200))
    win.blit(accuracy_label, (get_middle(accuracy_label), 300))
    win.blit(speed_label, (get_middle(speed_label), 400))

    pygame.display.update()

    run = True
    while run: # wait for the user to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()

def get_middle(surface): # for use in end_game to find the middle of the screen to render the endgame labels
    return WIDTH / 2 - surface.get_width() / 2

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
                # targets.append(Target(random.randint(TARGET_PADDING, WIDTH-TARGET_PADDING), random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT-TARGET_PADDING))) # one-line less readable version of the below append

                # readable format:
                x = random.randint(TARGET_PADDING, WIDTH-TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT-TARGET_PADDING)
                targets.append(Target(x, y)) 

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
            end_game(WIN, time.time() - start_time, targets_pressed, clicks)
        
        draw(WIN, targets) # draw targets
        draw_top_bar(WIN, time.time() - start_time, targets_pressed, misses) # draw top bar
        pygame.display.update()
                                
    pygame.quit()

if __name__ == "__main__":
    main()