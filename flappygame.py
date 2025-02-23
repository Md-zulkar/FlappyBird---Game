import pygame
import random
import os

#initialize a pygame module
pygame.init() 

# set up a game window
# Initialize pygame
pygame.init()

# Load and play background music

FPS=32
WIDTH, HEIGHT= 600,  800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Birds")

#SET UP A COLOR
white = (255,255,255)
blue = (135,206,250)
black=(0,0,0)
green=(0,255,0)
script_dir=os.path.dirname(os.path.abspath(__file__))
#set up a load assets

pipe_img = pygame.image.load(os.path.join(script_dir,"pipe.png")).convert_alpha()
background_img = pygame.image.load(os.path.join(script_dir,"background.png")).convert_alpha()
background_img = pygame.transform.scale(background_img,(WIDTH,HEIGHT))

bird_imgs = pygame.image.load(os.path.join(script_dir, "bird.png")).convert_alpha()
bird_imgs= pygame.transform.scale(bird_imgs,(40,60))
front_bird = pygame.image.load(os.path.join(script_dir, "front_image.png")).convert_alpha()
front_bird = pygame.transform.scale(front_bird,(WIDTH,HEIGHT))

pygame.mixer.init()
pygame.mixer.music.load(os.path.join(script_dir, "background.mp3"))  # Replace with actual file name
pygame.mixer.music.play(-1)  # -1 makes it loop infinitely
pygame.mixer.music.set_volume(0.5)  # Adjust volume (optional)


#now we set the bird properties 
bird_x =50  #horizantal position
bird_y = HEIGHT//2   #initial vertical position
bird_velocity = 0     #initial velocity
bird_gravity = 0.6            
jump = -6  #jumping value upward that how much jump upward
bird_animation_index = 0
bird_animation_timer = 0

#set up a pipe properties
pipe_width = 40 #pipe width
pipe_gap = 400   #gap between two pipes 
pipe_speed = 3    #pipe speed to continue
pipes = []        #list of pipes to store pipes efficiently
font = pygame.font.Font(None,36)

def start_screen():
    """Displays a message on the screen."""
    screen.blit(front_bird,(0,0))
    text = font.render("press SPACE to start", True, black)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT -100))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def game_over_screen(score):
    """Displays the game over screen with the final score."""
    screen.fill(black)
    text = font.render(f"Game Over! Score: {score}", True, white)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)


 
#create a new function to generate a pipes
def create_pipes():
    height = random.randint(100,300)  #random generate hieght of the pipe
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width,height)
    bottom_pipe = pygame.Rect(WIDTH, height+pipe_gap,pipe_width,HEIGHT -(height+pipe_gap))
    pipes.append((top_pipe,bottom_pipe))

#show the screen
start_screen()
# main game loop to continue game until player loses or exit the game

clock = pygame.time.Clock()
running = True
paused=False
score = 0


while running:
    screen.blit(background_img,(0,0)) #drwa background imageon the screen
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not paused:
                bird_velocity = jump  # Bird jumps when space is pressed
            if event.key == pygame.K_p:  # Press 'P' to pause/resume
                paused = not paused  # Toggle pause state
                if paused:
                    pygame.mixer.music.pause()  # Pause music
                else:
                    pygame.mixer.music.unpause()  # Resume music

    if paused:
        pause_text = font.render("PAUSED - Press 'P' to Resume", True, black)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
        pygame.display.update()
        continue  # Skip the rest of the loop while paused

#apply gravity to bird
    bird_velocity += bird_gravity
    bird_y +=bird_velocity

    bird_rect = pygame.Rect(bird_x, bird_y, 40, 60) #generate bird rectangle
#move the pipe on the left side 
    for top_pipe, bottom_pipe in pipes:
        top_pipe.x -= pipe_speed
        bottom_pipe.x -= pipe_speed
       
        screen.blit(pipe_img, (top_pipe.x, top_pipe.y))  # Draw top pipe
        screen.blit(pipe_img, (bottom_pipe.x, bottom_pipe.y))
#handle the collision

    
        if top_pipe.colliderect(bird_rect) or  bottom_pipe.colliderect(bird_rect):
         running = False
         break
        if top_pipe.x + pipe_width < bird_x and not top_pipe.x + pipe_width < bird_x - pipe_speed:
           score += 1


    
   #remove pipe that move out of screen
    pipes=[pipe for pipe in pipes if pipe[0].x > -pipe_width]
    
    #create new pipe when needed
    if len(pipes)==0 or pipes[-1][0].x < WIDTH - 200:
        create_pipes()

    #animate bird wings
    screen.blit(bird_imgs, (bird_x, bird_y))
  
    if bird_y > HEIGHT - 30:
       Running= False # game over

#display the score on the screen

    score_txt = font.render(f"score: {score}",True,white)
    screen.blit(score_txt ,(10,10))

    pygame.display.update()
    clock.tick(50)

pygame.mixer.music.stop()  # Stop background music



game_over_screen(score)
pygame.quit()
    
