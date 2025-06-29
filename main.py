import pygame
from scenes.intro import IntroScene

class SceneManager:
    def __init__(self):
        self.current_scene = None
    
    def set_scene(self, scene):
        self.current_scene = scene
    
    def update(self, dt):
        if self.current_scene:
            self.current_scene.update(dt)
    
    def draw(self, screen):
        if self.current_scene:
            self.current_scene.draw(screen)
    
    def handle_event(self, event):
        if self.current_scene:
            self.current_scene.handle_event(event)

class Scene:
    def update(self, dt):
        pass
    
    def draw(self, screen):
        pass
    
    def handle_event(self, event):
        pass

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("ZELTARUNE")
clock = pygame.time.Clock()

scene_manager = SceneManager()
scene_manager.set_scene(IntroScene(scene_manager))

running = True
while running:
    dt = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        scene_manager.handle_event(event)
    
    scene_manager.update(dt)
    
    screen.fill((0, 0, 0))
    scene_manager.draw(screen)
    pygame.display.flip()

pygame.quit()