import pygame
import os
import configparser

class Ch1SelectScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.font = pygame.font.Font("resources/fonts/DTC P.otf", 24)
        self.soul_img = pygame.image.load("resources/souls/determination.png")
        
        # Play background music
        pygame.mixer.music.load("resources/snd/mus_ch1s.mp3")
        pygame.mixer.music.play(-1)
        
        # Check if save file exists
        self.save_exists = os.path.exists("data/Zeltarune.ini")
        
        if not self.save_exists:
            self.state = "name_input"
            self.setup_name_input()
        else:
            self.state = "skip"
    
    def setup_name_input(self):
        self.keyboard = [
            ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
            ['H', 'I', 'J', 'K', 'L', 'M', 'N'],
            ['O', 'P', 'Q', 'R', 'S', 'T', 'U'],
            ['V', 'W', 'X', 'Y', 'Z', 'BACK', 'END']
        ]
        self.selected_row = 0
        self.selected_col = 0
        self.player_name = ""
        self.top_text = "NAME THE HUMAN."
        self.confirmation_state = "input"  # input, confirm, animating
        self.name_pos_y = 100
        self.name_scale = 1.0
        self.animation_timer = 0
        self.confirm_selected = 0  # 0 = YES, 1 = NO
        
        # Soul animation
        self.soul_x = 0
        self.soul_y = 0
        self.target_soul_x = 0
        self.target_soul_y = 0
    
    def update(self, dt):
        if self.state == "name_input":
            # Smooth soul movement
            self.soul_x += (self.target_soul_x - self.soul_x) * 8 * dt
            self.soul_y += (self.target_soul_y - self.soul_y) * 8 * dt
            
            if self.confirmation_state == "animating":
                self.animation_timer += dt
                progress = min(1.0, self.animation_timer / 1.0)  # 1 second animation
                
                # Move to center and scale up
                target_y = 240
                target_scale = 2.0
                self.name_pos_y = 100 + (target_y - 100) * progress
                self.name_scale = 1.0 + (target_scale - 1.0) * progress
                
                if progress >= 1.0:
                    self.confirmation_state = "confirm"
    
    def draw(self, screen):
        if self.state == "skip":
            return
            
        if not self.save_exists:
            screen_width, screen_height = screen.get_size()
            
            # Top text
            top_surface = self.font.render(self.top_text, True, (255, 255, 255))
            top_rect = top_surface.get_rect(center=(screen_width // 2, 50))
            screen.blit(top_surface, top_rect)
            
            # Player name input
            name_font = pygame.font.Font("resources/fonts/DTC P.otf", int(24 * self.name_scale))
            name_surface = name_font.render(self.player_name or "_", True, (255, 255, 255))
            name_rect = name_surface.get_rect(center=(screen_width // 2, self.name_pos_y))
            screen.blit(name_surface, name_rect)
            
            if self.confirmation_state == "input":
                # Draw keyboard
                start_y = 200
                for row_idx, row in enumerate(self.keyboard):
                    for col_idx, key in enumerate(row):
                        x = 50 + col_idx * 80
                        y = start_y + row_idx * 50
                        
                        color = (255, 255, 0) if (row_idx == self.selected_row and col_idx == self.selected_col) else (255, 255, 255)
                        key_surface = self.font.render(key, True, color)
                        
                        # Update target soul position for selected key
                        if row_idx == self.selected_row and col_idx == self.selected_col:
                            key_rect = key_surface.get_rect()
                            key_rect.topleft = (x, y)
                            self.target_soul_x = key_rect.centerx - self.soul_img.get_width() // 2
                            self.target_soul_y = key_rect.centery - self.soul_img.get_height() // 2
                        
                        screen.blit(key_surface, (x, y))
                
                # Draw soul at current position
                soul_copy = self.soul_img.copy()
                soul_copy.set_alpha(128)
                screen.blit(soul_copy, (int(self.soul_x), int(self.soul_y)))
            
            elif self.confirmation_state == "confirm":
                # Draw YES/NO options
                yes_color = (255, 255, 0) if self.confirm_selected == 0 else (255, 255, 255)
                no_color = (255, 255, 0) if self.confirm_selected == 1 else (255, 255, 255)
                
                yes_surface = self.font.render("YES", True, yes_color)
                no_surface = self.font.render("NO", True, no_color)
                
                yes_rect = yes_surface.get_rect(center=(screen_width // 2 - 100, screen_height - 100))
                no_rect = no_surface.get_rect(center=(screen_width // 2 + 100, screen_height - 100))
                
                # Update target soul position for selected option
                if self.confirm_selected == 0:
                    self.target_soul_x = yes_rect.centerx - self.soul_img.get_width() // 2
                    self.target_soul_y = yes_rect.centery - self.soul_img.get_height() // 2
                else:
                    self.target_soul_x = no_rect.centerx - self.soul_img.get_width() // 2
                    self.target_soul_y = no_rect.centery - self.soul_img.get_height() // 2
                
                # Draw soul at current position
                soul_copy = self.soul_img.copy()
                soul_copy.set_alpha(128)
                screen.blit(soul_copy, (int(self.soul_x), int(self.soul_y)))
                
                screen.blit(yes_surface, yes_rect)
                screen.blit(no_surface, no_rect)
    
    def handle_event(self, event):
        if not self.save_exists and event.type == pygame.KEYDOWN:
            if self.confirmation_state == "input":
                old_row, old_col = self.selected_row, self.selected_col
                if event.key in [pygame.K_w, pygame.K_UP]:
                    self.selected_row = (self.selected_row - 1) % len(self.keyboard)
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    self.selected_row = (self.selected_row + 1) % len(self.keyboard)
                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    self.selected_col = (self.selected_col - 1) % len(self.keyboard[self.selected_row])
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    self.selected_col = (self.selected_col + 1) % len(self.keyboard[self.selected_row])
                elif event.key in [pygame.K_RETURN, pygame.K_z]:
                    selected_key = self.keyboard[self.selected_row][self.selected_col]
                    if selected_key == "BACK":
                        if self.player_name:
                            self.player_name = self.player_name[:-1]
                    elif selected_key == "END":
                        if self.player_name:
                            self.top_text = "IS THIS CORRECT?"
                            self.confirmation_state = "animating"
                            self.animation_timer = 0
                    else:
                        if len(self.player_name) < 8:
                            self.player_name += selected_key
            
            elif self.confirmation_state == "confirm":
                if event.key in [pygame.K_a, pygame.K_d, pygame.K_LEFT, pygame.K_RIGHT]:
                    self.confirm_selected = 1 - self.confirm_selected
                elif event.key in [pygame.K_RETURN, pygame.K_z]:
                    if self.confirm_selected == 0:  # YES
                        self.create_save_file()
                    else:  # NO
                        self.confirmation_state = "input"
                        self.top_text = "NAME THE HUMAN."
                        self.name_pos_y = 100
                        self.name_scale = 1.0
    
    def create_save_file(self):
        os.makedirs("data", exist_ok=True)
        config = configparser.ConfigParser()
        config['player'] = {
            'name': self.player_name,
            'playerHp': '20',
            'maxPlayerHp': '20',
            'playerLv': '1'
        }
        with open("data/Zeltarune.ini", 'w') as configfile:
            config.write(configfile)