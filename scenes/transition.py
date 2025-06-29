import pygame

class TransitionScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        original_logo = pygame.image.load("resources/utils/logotext.png")
        
        # Make image bigger (2x scale)
        new_size = (original_logo.get_width() * 2, original_logo.get_height() * 2)
        self.logo_img = pygame.transform.scale(original_logo, new_size)
        
        self.screen_width = 640
        self.screen_height = 480
        
        # Play intro noise
        self.intro_sound = pygame.mixer.Sound("resources/snd/snd_INTRONOISE.mp3")
        self.intro_sound.play()
        
        # Center the logo
        self.logo_rect = self.logo_img.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        
        # Transition states - 12 seconds total
        self.state = "fade_in"  # fade_in -> pixelate -> fade_out -> black
        self.alpha = 0
        self.timer = 0
        self.fade_in_time = 3.0  # 3 seconds fade in
        self.pixelate_time = 6.0  # 6 seconds gradual pixelation
        self.fade_out_time = 3.0  # 3 seconds fade out
        
        # Pixelation parameters
        self.max_pixel_size = min(self.logo_img.get_width(), self.logo_img.get_height()) // 2
        self.min_pixel_size = 1
        
    def update(self, dt):
        self.timer += dt
        
        if self.state == "fade_in":
            self.alpha = min(255, (self.timer / self.fade_in_time) * 255)
            if self.timer >= self.fade_in_time:
                self.alpha = 255
                self.state = "pixelate"
                self.timer = 0
                
        elif self.state == "pixelate":
            if self.timer >= self.pixelate_time:
                self.state = "fade_out"
                self.timer = 0
                
        elif self.state == "fade_out":
            self.alpha = max(0, 255 - (self.timer / self.fade_out_time) * 255)
            if self.timer >= self.fade_out_time:
                self.alpha = 0
                self.state = "black"
                # Switch to ch1Select scene
                from .ch1Select import Ch1SelectScene
                self.scene_manager.set_scene(Ch1SelectScene(self.scene_manager))
    
    def get_pixelated_image(self, progress):
        # Calculate current pixel size based on progress (0 to 1)
        # Start with original, gradually reduce to minimum
        current_divisor = int(self.max_pixel_size - (progress * (self.max_pixel_size - self.min_pixel_size)))
        current_divisor = max(self.min_pixel_size, current_divisor)
        
        # Create pixelated version
        small_width = max(1, self.logo_img.get_width() // current_divisor)
        small_height = max(1, self.logo_img.get_height() // current_divisor)
        
        small_img = pygame.transform.scale(self.logo_img, (small_width, small_height))
        return pygame.transform.scale(small_img, self.logo_img.get_size())
    
    def draw(self, screen):
        if self.state == "black":
            return
            
        if self.state == "fade_in":
            # Normal fade in
            logo_copy = self.logo_img.copy()
            logo_copy.set_alpha(int(self.alpha))
            screen.blit(logo_copy, self.logo_rect)
        elif self.state == "pixelate":
            # Gradual pixelation
            progress = self.timer / self.pixelate_time
            pixelated_img = self.get_pixelated_image(progress)
            pixelated_img.set_alpha(255)
            screen.blit(pixelated_img, self.logo_rect)
        else:  # fade_out
            # Keep maximum pixelation during fade out
            pixelated_img = self.get_pixelated_image(1.0)
            pixelated_img.set_alpha(int(self.alpha))
            screen.blit(pixelated_img, self.logo_rect)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_RETURN or event.key == pygame.K_z) and self.state != "fade_out":
                # Stop sound and skip to fade out
                self.intro_sound.stop()
                self.state = "fade_out"
                self.timer = 0