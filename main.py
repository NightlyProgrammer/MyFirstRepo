import pygame
import json

def load_settings(path):
    with open(path,'r') as file:
        return json.load(file)
        

def main():
    #Load all the constants from a json file
    SETTINGS = load_settings("settings.json")
    screen = pygame.display.set_mode(SETTINGS["SCREEN_SIZE"])
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
        screen.fill((0,0,0))

        pygame.display.flip()
        pygame.display.set_caption(str(round(clock.get_fps())))
        clock.tick(SETTINGS["FPS"])

if __name__ == '__main__':
    pygame.init()
    main()