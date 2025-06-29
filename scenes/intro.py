import pygame
import sys
import os

class IntroScene:
    def __init__(self, scene_manager=None):
        self.scene_manager = scene_manager
        pygame.mixer.init()
        pygame.mixer.music.load("resources/snd/mus_cSelect.mp3")
        pygame.mixer.music.play(-1)
        
        self.font = pygame.font.Font("resources/fonts/DT Mono.ttf", 36)
        self.soul_img = pygame.image.load("resources/souls/determination.png")
        self.move_sound = pygame.mixer.Sound("resources/snd/snd_moveS.mp3")
        self.select_sound = pygame.mixer.Sound("resources/snd/snd_oSelect.mp3")
        
        self.options = ["chapter1", "quit"]
        self.selected = 0
        
        # Soul animation
        self.soul_x = 5
        self.soul_y = 25
        self.target_soul_x = 5
        self.target_soul_y = 25
    
    def update(self, dt):
        # Smooth soul movement
        self.soul_x += (self.target_soul_x - self.soul_x) * 8 * dt
        self.soul_y += (self.target_soul_y - self.soul_y) * 8 * dt
    
    def draw(self, screen):
        screen_width, screen_height = screen.get_size()
        
        # Chapter 1 and The Beginning on same line
        color1 = (255, 255, 0) if self.selected == 0 else (255, 255, 255)
        chapter_text = self.font.render("Chapter 1", True, color1)
        beginning_text = self.font.render("The Beginning", True, color1)
        
        screen.blit(chapter_text, (40, 20))
        screen.blit(beginning_text, (40 + chapter_text.get_width() + 40, 20))
        
        # HR line below Chapter 1 text
        line_y = 20 + chapter_text.get_height() + 10
        pygame.draw.line(screen, (255, 255, 255), (0, line_y), (screen_width, line_y), 2)
        
        # Quit at bottom center
        color2 = (255, 255, 0) if self.selected == 1 else (255, 255, 255)
        quit_text = self.font.render("Quit", True, color2)
        quit_rect = quit_text.get_rect(center=(screen_width // 2, screen_height - 40))
        screen.blit(quit_text, quit_rect)
        
        # Update target soul position
        if self.selected == 0:
            self.target_soul_x = 5
            self.target_soul_y = 25
        else:
            self.target_soul_x = quit_rect.x - self.soul_img.get_width() - 15
            self.target_soul_y = quit_rect.y + (quit_text.get_height() - self.soul_img.get_height()) // 2
        
        # Draw soul at current position
        screen.blit(self.soul_img, (int(self.soul_x), int(self.soul_y)))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                self.move_sound.play()
                self.selected = (self.selected + 1) % 2
            elif event.key == pygame.K_RETURN:
                self.select_sound.play()
                if self.selected == 0:  # Chapter 1
                    pygame.mixer.music.stop()
                    if self.scene_manager:
                        from .transition import TransitionScene
                        self.scene_manager.set_scene(TransitionScene(self.scene_manager))
                elif self.selected == 1:  # Quit
                    pygame.quit()
                    sys.exit()