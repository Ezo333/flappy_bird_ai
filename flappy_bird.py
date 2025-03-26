import pygame
import neat
import time
import os 
import random 
pygame.font.init()
# mask ene odoo bidriin pipe bas brid hoorondoo hursniig hiihed amarhan yagaad gevel 4lchn dotord boorhi baigaa tern mordoldvl tgd hoorondoo hursn geel oilogchih hha martahguil baydaa ))

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))
STAT_FONT = pygame.font.SysFont("comicsans",50)

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0 
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5 # ene yagaad negitive baigaa bee geheer 
                         # manai py game windows maan deed zuun bulangaas 0;0 goos 
                         # eheldeg tiim bolhoor mana bird deesee yuvhiin tuld - doosoo bol +
        self.tick_count = 0 
        self.height = self.y # checks 

    def move(self):
        self.tick_count += 1 # track how many jump did we did

        d = self.vel*self.tick_count+1.5*self.tick_count**2
        # how much we moving up and how much we moving down
        # - 10.5 + 1.5 = 9 tick count maan 0 baigaa gehdee jump hiih bolgond nemegdn tgd 7 6 5 geel real2
        #example
#Current Frame: 1
#Current Velocity -9.0
#Current Frame: 2
#Current Velocity -15.0
#Current Frame: 3
#Current Velocity -18.0
#Current Frame: 4
#Current Velocity -18.0
#Current Frame: 5
#Current Velocity -15.0
#Current Frame: 6
#Current Velocity -9.0
#Current Frame: 7
#Current Velocity 0.0
#Current Frame: 8
#Current Velocity 12.0
#Current Frame: 9
#Current Velocity 27.0

        if d >= 16:
            d = 16

        if d <= 0:
            d -= 2 # how much higher jump

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50: # ene yornhiidoo bol mana bird deeshleheer dooshoogiin maanl shalgaj baigaa gej oilgoj bln
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION # deeshee bolgoj baigaa
            else:
                if self.tilt > -90: # dooshoo unac baigaag haruulch baigaa
                    self.tilt -= self.ROT_VEL

        
    def draw(self,win):
        self.img_count += 1 # how many time we showed 1 img

        # ene if elif maan bidrii zurgiin yag animation time aar solch baigaa
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4+1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[0]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt) # ene manai bird iig aimar sonig hargduulaad bsn
        
        # testing this code rotating fall its funny
        #if self.vel < 0:  # If bird is going up, keep its upward tilt
         #self.tilt = self.MAX_ROTATION
        #elif self.vel >= 0:  # If bird is falling, adjust tilt based on velocity
         #self.tilt -= self.ROT_VEL

        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center) # stackoverflow deer olsn code ene code maan mana bird iig arail gaiguu haruulsn real2
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VEL = 5 

    def __init__(self,x):
        self.x = x
        self.height = 0 

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG,False,True) # maybe u forget pipeiin zurag door davhad yag bolsn baigaa teriig zgr fli deer deer baihad yamarhuu baihnuug shalgaal bolchj baigaa
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height() # checking the pipe iin maan dont know yu gej helhiin yamartaich pipe iin deedldeer hurh yumiigl hiich bn 
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self,win):
        win.blit(self.PIPE_TOP, (self.x , self.top))
        win.blit(self.PIPE_BOTTOM, (self.x , self.bottom))
    
    def collide(self,bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM) # pixel eer overcollide hiich bn uu shalgn


        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset) # collide hiihgui bol none ogn
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        
        return False
    
class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH # bid base image ee 2 bolgood teriigee odoo 1 base odoo haragdach baihad nogoo 2 doh base maan hodlood screend haragdahku bolhd bider teriigee buchaagaad gargach irch baigaa yagl toirgoor 
    
    def draw(self,win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def draw_window(win, birds, pipes, base, score): # background img and bird on top
    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)
    
    text = STAT_FONT.render("Score: " + str(score), 1,(255,255,255))
    win.blit(text,(WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()


def main(genomes, config):
    nets = []
    ge = []
    birds = []
    #manai neat algorithm 
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness = 0
        ge.append(g)
        


    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].PIPE_TOP.get_width(): # pipeduu oorchlc baigaa birduud maan yahaas shaltgaaln
                pipe_ind = 1
        else:
            run = False
            break
        
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()


        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                   ge[x].fitness -= 1 # bird ai maan hervee piped hurvel bider neg onoo hasch baigaa yagaad gevl buruu yum hiihees boluulahiin tuld
                   birds.pop(x)
                   nets.pop(x)
                   ge.pop(x)

                if not pipe.passed and pipe.x < bird.x: #hervee manai bird pipe aar zonguut bider dahaid pipe nemne
                   pipe.passed=True
                   add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width()<0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600)) # hoorondiin zai pipeiin

        for r in rem:
            pipes.remove(r)
        
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()
        draw_window(win, birds, pipes, base, score)




def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"c:/Users/Dell/Desktop/python/biedaalt/neat")
    run(config_path)






