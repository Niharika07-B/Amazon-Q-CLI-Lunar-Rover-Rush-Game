import pygame
import random
import math
import os
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lunar Rover Race")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Game variables
clock = pygame.time.Clock()
FPS = 60

# Lunar physics
MOON_GRAVITY = 0.16  # Moon's gravity is about 1/6 of Earth's

# Create directories for assets if they don't exist
if not os.path.exists("assets"):
    os.makedirs("assets")
if not os.path.exists("assets/sounds"):
    os.makedirs("assets/sounds")
if not os.path.exists("assets/images"):
    os.makedirs("assets/images")

# Create simple rover sprite
def create_rover_sprite():
    # Create a simple rover sprite
    rover = pygame.Surface((50, 30), pygame.SRCALPHA)
    
    # Main body (silver/gray)
    pygame.draw.rect(rover, (180, 180, 180), (5, 10, 40, 15), 0, 3)
    
    # Wheels (black)
    pygame.draw.circle(rover, (50, 50, 50), (10, 25), 5)
    pygame.draw.circle(rover, (50, 50, 50), (40, 25), 5)
    
    # Antenna (white)
    pygame.draw.line(rover, WHITE, (30, 10), (35, 0), 2)
    pygame.draw.circle(rover, RED, (35, 0), 2)
    
    # Solar panel (blue)
    pygame.draw.rect(rover, BLUE, (15, 5, 20, 5))
    
    return rover

# Create stars for background
def create_starry_background():
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Create a gradient background (dark blue to black)
    for y in range(SCREEN_HEIGHT):
        # Calculate color based on y position
        blue_value = max(0, 50 - int(y * 50 / SCREEN_HEIGHT))
        color = (0, 0, blue_value)
        pygame.draw.line(background, color, (0, y), (SCREEN_WIDTH, y))
    
    # Add stars
    for _ in range(150):  # More stars for a denser sky
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT // 2)  # Stars in upper half
        size = random.randint(1, 3)
        brightness = random.randint(150, 255)
        color = (brightness, brightness, brightness)
        pygame.draw.circle(background, color, (x, y), size)
        
        # Add twinkle effect to some stars
        if random.random() < 0.2:
            glow_size = size + random.randint(1, 2)
            glow_color = (brightness // 2, brightness // 2, brightness // 2)
            pygame.draw.circle(background, glow_color, (x, y), glow_size)
    
    # Add Earth in the background
    earth_pos = (SCREEN_WIDTH - 80, 80)
    earth_radius = 60
    # Blue Earth
    pygame.draw.circle(background, (0, 100, 200), earth_pos, earth_radius)
    # Cloud patterns (white)
    for _ in range(15):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, earth_radius * 0.8)
        cloud_x = int(earth_pos[0] + math.cos(angle) * distance)
        cloud_y = int(earth_pos[1] + math.sin(angle) * distance)
        cloud_size = random.randint(5, 15)
        pygame.draw.circle(background, (240, 240, 240), (cloud_x, cloud_y), cloud_size)
    
    # Add distant mountains on the horizon
    for i in range(5):
        mountain_width = random.randint(100, 200)
        mountain_height = random.randint(50, 100)
        mountain_x = random.randint(0, SCREEN_WIDTH)
        mountain_y = int(SCREEN_HEIGHT * 0.5)  # Horizon line
        
        # Draw mountain (dark gray)
        points = [
            (mountain_x, mountain_y),
            (mountain_x + mountain_width // 2, mountain_y - mountain_height),
            (mountain_x + mountain_width, mountain_y)
        ]
        pygame.draw.polygon(background, (50, 50, 60), points)
    
    return background

# Create sound effects
def load_sound_effects():
    sounds = {}
    
    # Create simple beep sounds with different frequencies
    try:
        # Create simple beep sounds with different parameters
        buffer_jump = bytearray()
        buffer_boost = bytearray()
        buffer_crash = bytearray()
        buffer_powerup = bytearray()
        buffer_engine = bytearray()
        buffer_music = bytearray()
        buffer_game_over = bytearray()
        buffer_journey = bytearray()
        
        sample_rate = 22050  # Lower sample rate for better compatibility
        max_sample = 16000  # Lower amplitude to avoid distortion
        
        # Jump sound (higher pitch, short)
        for i in range(int(0.2 * sample_rate)):
            freq = 440 + i * 10  # Rising pitch
            value = int(max_sample * 0.5 * math.sin(2 * math.pi * freq * i / sample_rate))
            # Convert to 16-bit little-endian format
            buffer_jump.extend([value & 0xFF, (value >> 8) & 0xFF])
        
        # Boost sound (medium pitch, medium length)
        for i in range(int(0.3 * sample_rate)):
            freq = 330
            value = int(max_sample * 0.6 * math.sin(2 * math.pi * freq * i / sample_rate))
            # Add some variation
            if i % 1000 < 500:
                value = int(value * 1.2)
            buffer_boost.extend([value & 0xFF, (value >> 8) & 0xFF])
        
        # Crash sound (low pitch, longer)
        for i in range(int(0.5 * sample_rate)):
            # Random noise for crash
            value = int(max_sample * 0.7 * random.uniform(-1, 1))
            buffer_crash.extend([value & 0xFF, (value >> 8) & 0xFF])
        
        # Powerup sound (high pitch, short)
        for i in range(int(0.2 * sample_rate)):
            freq = 660 - i * 5  # Falling pitch
            value = int(max_sample * 0.5 * math.sin(2 * math.pi * freq * i / sample_rate))
            buffer_powerup.extend([value & 0xFF, (value >> 8) & 0xFF])
        
        # Engine sound (low pitch, looping)
        for i in range(int(0.5 * sample_rate)):
            freq = 110
            value = int(max_sample * 0.3 * math.sin(2 * math.pi * freq * i / sample_rate))
            # Add some variation
            value += int(max_sample * 0.1 * math.sin(2 * math.pi * (freq*2) * i / sample_rate))
            buffer_engine.extend([value & 0xFF, (value >> 8) & 0xFF])
        
        # Game over sound (descending tone)
        for i in range(int(1.0 * sample_rate)):
            freq = 440 - i * 0.4  # Descending pitch
            value = int(max_sample * 0.6 * math.sin(2 * math.pi * freq * i / sample_rate))
            # Add tremolo effect
            value = int(value * (0.5 + 0.5 * math.sin(2 * math.pi * 5 * i / sample_rate)))
            buffer_game_over.extend([value & 0xFF, (value >> 8) & 0xFF])
            
        # Journey sound (pleasant chime)
        for i in range(int(0.5 * sample_rate)):
            # Combine two pleasant frequencies
            freq1 = 523.25  # C5
            freq2 = 659.25  # E5
            value = int(max_sample * 0.3 * math.sin(2 * math.pi * freq1 * i / sample_rate))
            value += int(max_sample * 0.3 * math.sin(2 * math.pi * freq2 * i / sample_rate))
            # Add fade in/out
            envelope = 1.0
            if i < 0.1 * sample_rate:
                envelope = i / (0.1 * sample_rate)
            elif i > 0.4 * sample_rate:
                envelope = 1.0 - (i - 0.4 * sample_rate) / (0.1 * sample_rate)
            value = int(value * envelope)
            buffer_journey.extend([value & 0xFF, (value >> 8) & 0xFF])
        
        # Space-themed background music
        notes = [262, 330, 392, 523]  # C4, E4, G4, C5 (C major chord)
        note_duration = int(0.3 * sample_rate)
        for _ in range(3):  # Repeat the pattern
            for note in notes:
                for i in range(note_duration):
                    # Add some harmonics for a richer sound
                    value = int(max_sample * 0.3 * math.sin(2 * math.pi * note * i / sample_rate))
                    value += int(max_sample * 0.15 * math.sin(2 * math.pi * note * 2 * i / sample_rate))
                    # Add some ambient noise
                    value += int(max_sample * 0.05 * random.uniform(-1, 1))
                    # Add fade in/out for each note
                    envelope = 1.0
                    if i < 0.05 * sample_rate:
                        envelope = i / (0.05 * sample_rate)
                    elif i > note_duration - 0.05 * sample_rate:
                        envelope = (note_duration - i) / (0.05 * sample_rate)
                    value = int(value * envelope)
                    buffer_music.extend([value & 0xFF, (value >> 8) & 0xFF])
        
        # Create sound objects
        sounds["jump"] = pygame.mixer.Sound(buffer=buffer_jump)
        sounds["boost"] = pygame.mixer.Sound(buffer=buffer_boost)
        sounds["crash"] = pygame.mixer.Sound(buffer=buffer_crash)
        sounds["powerup"] = pygame.mixer.Sound(buffer=buffer_powerup)
        sounds["engine_idle"] = pygame.mixer.Sound(buffer=buffer_engine)
        sounds["engine_low"] = pygame.mixer.Sound(buffer=buffer_engine)
        sounds["engine_medium"] = pygame.mixer.Sound(buffer=buffer_engine)
        sounds["engine_high"] = pygame.mixer.Sound(buffer=buffer_engine)
        sounds["background_music"] = pygame.mixer.Sound(buffer=buffer_music)
        sounds["game_over"] = pygame.mixer.Sound(buffer=buffer_game_over)
        sounds["journey"] = pygame.mixer.Sound(buffer=buffer_journey)
        
    except Exception as e:
        print(f"Error creating sounds: {e}")
        # Create dummy sound class if sound creation fails
        class DummySound:
            def play(self, loops=0):
                pass
            def stop(self):
                pass
        
        # Fill with dummy sounds
        sounds["jump"] = DummySound()
        sounds["boost"] = DummySound()
        sounds["crash"] = DummySound()
        sounds["powerup"] = DummySound()
        sounds["engine_idle"] = DummySound()
        sounds["engine_low"] = DummySound()
        sounds["engine_medium"] = DummySound()
        sounds["engine_high"] = DummySound()
        sounds["background_music"] = DummySound()
        sounds["game_over"] = DummySound()
        sounds["journey"] = DummySound()
    
    return sounds

# Create assets
rover_img = create_rover_sprite()
background_img = create_starry_background()
sounds = load_sound_effects()

# Terrain generation
class TerrainGenerator:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ground_height = screen_height * 0.7
        self.segments = []
        self.segment_width = 20
        self.generate_initial_terrain()
    
    def generate_initial_terrain(self):
        # Generate terrain segments that extend beyond the screen
        for x in range(0, self.screen_width + 500, self.segment_width):
            # Create some variation in height
            height = self.ground_height + random.randint(-30, 30)
            # Occasionally add craters or hills
            if random.random() < 0.1:
                # Crater
                height += random.randint(20, 40)
            elif random.random() < 0.1:
                # Hill
                height -= random.randint(20, 40)
            
            self.segments.append((x, height))
    
    def update(self, scroll_speed):
        # Remove segments that have scrolled off screen
        while self.segments and self.segments[0][0] < -self.segment_width:
            self.segments.pop(0)
        
        # Add new segments at the right edge
        last_x = self.segments[-1][0]
        last_height = self.segments[-1][1]
        
        if last_x < self.screen_width + 500:
            new_x = last_x + self.segment_width
            # Smooth transition from last height
            new_height = last_height + random.randint(-10, 10)
            
            # Occasionally add craters or hills
            if random.random() < 0.1:
                # Crater
                new_height += random.randint(20, 40)
            elif random.random() < 0.1:
                # Hill
                new_height -= random.randint(20, 40)
            
            # Keep height within reasonable bounds
            new_height = max(min(new_height, self.ground_height + 50), self.ground_height - 50)
            
            self.segments.append((new_x, new_height))
        
        # Scroll all segments
        for i in range(len(self.segments)):
            self.segments[i] = (self.segments[i][0] - scroll_speed, self.segments[i][1])
    
    def draw(self, surface):
        # Draw the terrain
        for i in range(len(self.segments) - 1):
            x1, y1 = self.segments[i]
            x2, y2 = self.segments[i + 1]
            
            # Draw the segment
            pygame.draw.polygon(surface, GRAY, [
                (x1, y1), 
                (x2, y2), 
                (x2, self.screen_height), 
                (x1, self.screen_height)
            ])
    
    def get_height_at(self, x):
        # Find the height of the terrain at position x
        for i in range(len(self.segments) - 1):
            x1, y1 = self.segments[i]
            x2, y2 = self.segments[i + 1]
            
            if x1 <= x < x2:
                # Linear interpolation
                ratio = (x - x1) / (x2 - x1)
                return y1 + ratio * (y2 - y1)
        
        # Default if not found
        return self.ground_height

# Player class
class Rover:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 30
        self.vel_y = 0
        self.jumping = False
        self.speed = 5
        self.health = 100
        self.fuel = 100  # Maximum fuel level
        self.fuel_consumption_rate = 0.1  # Fuel consumed per frame
        self.boosting = False
        self.boost_time = 0
        self.shield_active = False
        self.shield_time = 0
        self.skin = "default"  # default or red or green
        self.skins = {"default": "blue", "red": "red", "green": "green"}
        self.engine_sound_playing = False
        self.engine_sound_channel = None
        self.score = 0  # Player's score
        self.jump_height = 0  # Track jump height for scoring
        self.max_jump_height = 0  # Track maximum jump height
    
    def update(self, terrain, keys):
        # Apply gravity
        self.vel_y += MOON_GRAVITY
        
        # Handle jumping with up arrow key
        if keys[pygame.K_UP] and not self.jumping and self.fuel > 5:
            self.vel_y = -5  # Negative velocity means going up
            self.jumping = True
            self.fuel -= 5  # Jumping consumes fuel
            self.jump_height = 0  # Reset jump height
            self.max_jump_height = 0  # Reset max jump height
            sounds["jump"].play()
        
        # Handle downward movement with down arrow key (faster falling)
        if keys[pygame.K_DOWN] and self.jumping:
            self.vel_y += 0.3  # Accelerate downward
        
        # Update position
        self.y += self.vel_y
        
        # Track jump height for scoring
        if self.jumping:
            # Calculate height from ground
            terrain_height = terrain.get_height_at(self.x + self.width / 2)
            current_height = terrain_height - (self.y + self.height)
            self.jump_height = current_height
            
            # Update max jump height
            if current_height > self.max_jump_height:
                self.max_jump_height = current_height
        
        # Check for collision with terrain
        terrain_height = terrain.get_height_at(self.x + self.width / 2)
        if self.y + self.height > terrain_height:
            self.y = terrain_height - self.height
            self.vel_y = 0
            
            # Award points for jump height when landing
            if self.jumping:
                jump_points = int(self.max_jump_height * 0.5)  # 0.5 points per pixel of height
                if jump_points > 0:
                    self.score += jump_points
                    # Show jump points text
                    self.show_jump_points = True
                    self.jump_points_value = jump_points
                    self.jump_points_timer = 60  # Show for 1 second
                    self.jump_points_x = self.x
                    self.jump_points_y = self.y - 20
            
            self.jumping = False
            self.jump_height = 0
        
        # Handle boosting
        if self.boosting:
            self.boost_time -= 1
            self.fuel -= 0.3  # Boosting consumes more fuel
            if self.boost_time <= 0 or self.fuel <= 0:
                self.boosting = False
                self.speed = 5
        
        # Handle shield
        if self.shield_active:
            self.shield_time -= 1
            if self.shield_time <= 0:
                self.shield_active = False
        
        # Update engine sound based on speed
        self.update_engine_sound()
        
        # Consume fuel when moving
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_a] or keys[pygame.K_d]:
            self.fuel -= self.fuel_consumption_rate
        
        # Limit fuel to valid range
        self.fuel = max(0, min(self.fuel, 100))
        
        # If out of fuel, reduce speed
        if self.fuel <= 0:
            self.speed = max(1, self.speed - 0.1)  # Gradually slow down
        
        # Update jump points display
        if hasattr(self, 'show_jump_points') and self.show_jump_points:
            self.jump_points_timer -= 1
            self.jump_points_y -= 1  # Float upward
            if self.jump_points_timer <= 0:
                self.show_jump_points = False
    
    def update_engine_sound(self):
        # Determine which engine sound to play based on speed
        if self.boosting:
            engine_sound = sounds["engine_high"]
        elif self.speed > 7:
            engine_sound = sounds["engine_medium"]
        elif self.speed > 3:
            engine_sound = sounds["engine_low"]
        else:
            engine_sound = sounds["engine_idle"]
        
        # Play the appropriate engine sound if not already playing
        if not self.engine_sound_playing:
            self.engine_sound_channel = engine_sound.play(-1)  # Loop indefinitely
            self.engine_sound_playing = True
        else:
            # Stop current sound and play new one if speed changed
            if self.engine_sound_channel is not None:
                self.engine_sound_channel.stop()
            self.engine_sound_channel = engine_sound.play(-1)
    
    def draw(self, surface):
        # Draw the rover with different colors based on skin
        rover_copy = rover_img.copy()
        
        if self.skin == "red":
            # Tint the rover red
            red_tint = pygame.Surface(rover_copy.get_size(), pygame.SRCALPHA)
            red_tint.fill((255, 0, 0, 100))
            rover_copy.blit(red_tint, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        elif self.skin == "green":
            # Tint the rover green
            green_tint = pygame.Surface(rover_copy.get_size(), pygame.SRCALPHA)
            green_tint.fill((0, 255, 0, 100))
            rover_copy.blit(green_tint, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        
        surface.blit(rover_copy, (self.x, self.y))
        
        # Draw shield if active
        if self.shield_active:
            pygame.draw.circle(surface, BLUE, (int(self.x + self.width / 2), int(self.y + self.height / 2)), 
                              int(max(self.width, self.height) * 0.7), 2)
        
        # Draw jump points if active
        if hasattr(self, 'show_jump_points') and self.show_jump_points:
            font = pygame.font.Font(None, 24)
            points_text = font.render(f"+{self.jump_points_value}", True, (255, 255, 0))
            surface.blit(points_text, (self.jump_points_x, self.jump_points_y))
            
        # Draw jump height indicator when jumping
        if self.jumping:
            # Draw a line showing jump height
            pygame.draw.line(surface, (255, 255, 0), 
                            (self.x + self.width + 5, self.y + self.height),
                            (self.x + self.width + 5, self.y + self.height - self.jump_height),
                            2)
    
    def activate_boost(self):
        if self.fuel > 10:  # Only activate boost if enough fuel
            self.boosting = True
            self.boost_time = 180  # 3 seconds at 60 FPS
            self.speed = 10
            sounds["boost"].play()
    
    def activate_shield(self):
        self.shield_active = True
        self.shield_time = 300  # 5 seconds at 60 FPS
        sounds["powerup"].play()
        
    def add_fuel(self, amount):
        self.fuel = min(100, self.fuel + amount)
        
    def add_score(self, points):
        self.score += points

# Hazard class
class Hazard:
    def __init__(self, x, y, hazard_type):
        self.x = x
        self.y = y
        self.type = hazard_type
        self.width = 30
        self.height = 30
        self.active = True
        
        if hazard_type == "meteor":
            self.width = 20
            self.height = 20
        elif hazard_type == "laser":
            self.width = 10
            self.height = 40
        elif hazard_type == "crater":
            self.width = 50
            self.height = 10
    
    def update(self, scroll_speed):
        self.x -= scroll_speed
        
        # Deactivate if off screen
        if self.x + self.width < 0:
            self.active = False
    
    def draw(self, surface):
        if not self.active:
            return
            
        if self.type == "meteor":
            # Draw a meteor (red circle with some details)
            pygame.draw.circle(surface, RED, (int(self.x + self.width / 2), int(self.y + self.height / 2)), 
                              int(self.width / 2))
            # Add some meteor details
            pygame.draw.circle(surface, (150, 50, 50), 
                              (int(self.x + self.width / 3), int(self.y + self.height / 3)), 
                              int(self.width / 6))
        elif self.type == "laser":
            # Draw a laser beam (red rectangle with glow)
            pygame.draw.rect(surface, RED, (self.x, self.y, self.width, self.height))
            # Add glow effect
            glow_surf = pygame.Surface((self.width + 4, self.height + 4), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (255, 100, 100, 128), (0, 0, self.width + 4, self.height + 4))
            surface.blit(glow_surf, (self.x - 2, self.y - 2))
        elif self.type == "crater":
            # Draw a crater (gray ellipse with shadow)
            pygame.draw.ellipse(surface, GRAY, (self.x, self.y, self.width, self.height))
            # Add shadow
            pygame.draw.ellipse(surface, (50, 50, 50), (self.x + 5, self.y + 5, self.width - 10, self.height - 5))
    
    def check_collision(self, rover):
        if not self.active:
            return False
            
        # Simple rectangle collision
        rover_rect = pygame.Rect(rover.x, rover.y, rover.width, rover.height)
        hazard_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        return rover_rect.colliderect(hazard_rect)

# PowerUp class
class PowerUp:
    def __init__(self, x, y, power_type, force_floating=False):
        self.x = x
        self.y = y
        self.type = power_type
        self.width = 20
        self.height = 20
        self.active = True
        
        # Make coins float by default or if forced
        if power_type == "coin" or force_floating:
            self.floating = True
            if not force_floating and random.random() < 0.5:
                # Float higher for some coins
                self.y -= random.randint(50, 150)
        else:
            self.floating = False
    
    def update(self, scroll_speed):
        self.x -= scroll_speed
        
        # Deactivate if off screen
        if self.x + self.width < 0:
            self.active = False
    
    def draw(self, surface):
        if not self.active:
            return
            
        if self.type == "boost":
            # Draw a boost powerup (green arrow)
            pygame.draw.rect(surface, GREEN, (self.x, self.y, self.width, self.height))
            # Draw arrow shape
            points = [
                (self.x + self.width/2, self.y),
                (self.x + self.width, self.y + self.height/2),
                (self.x + 3*self.width/4, self.y + self.height/2),
                (self.x + 3*self.width/4, self.y + self.height),
                (self.x + self.width/4, self.y + self.height),
                (self.x + self.width/4, self.y + self.height/2),
                (self.x, self.y + self.height/2)
            ]
            pygame.draw.polygon(surface, (50, 200, 50), points)
        elif self.type == "shield":
            # Draw a shield powerup (blue circle)
            pygame.draw.circle(surface, BLUE, (int(self.x + self.width / 2), int(self.y + self.height / 2)), 
                              int(self.width / 2))
            # Draw shield symbol
            pygame.draw.arc(surface, (100, 100, 255), 
                           (self.x + 2, self.y + 2, self.width - 4, self.height - 4),
                           0, math.pi, 2)
        elif self.type == "magnet":
            # Draw a magnet powerup (yellow horseshoe)
            pygame.draw.rect(surface, YELLOW, (self.x, self.y, self.width, self.height))
            # Draw magnet symbol
            pygame.draw.arc(surface, (200, 200, 0), 
                           (self.x + 2, self.y + 2, self.width - 4, self.height - 4),
                           0, math.pi, 3)
        elif self.type == "fuel":
            # Draw a fuel powerup (red canister)
            pygame.draw.rect(surface, RED, (self.x, self.y, self.width, self.height))
            # Draw fuel symbol
            pygame.draw.rect(surface, (200, 50, 50), 
                            (self.x + 4, self.y + 2, self.width - 8, self.height - 4))
            pygame.draw.rect(surface, (250, 250, 250), 
                            (self.x + 6, self.y + 4, self.width - 12, self.height - 8))
        elif self.type == "coin":
            # Draw a coin (gold circle)
            pygame.draw.circle(surface, (255, 215, 0), (int(self.x + self.width / 2), int(self.y + self.height / 2)), 
                              int(self.width / 2))
            # Draw coin details
            pygame.draw.circle(surface, (255, 235, 100), 
                              (int(self.x + self.width / 2), int(self.y + self.height / 2)), 
                              int(self.width / 3))
            
            # If floating, draw a small indicator
            if self.floating:
                pygame.draw.line(surface, (255, 255, 255), 
                                (self.x + self.width/2, self.y + self.height),
                                (self.x + self.width/2, self.y + self.height + 10),
                                1)
    
    def check_collision(self, rover):
        if not self.active:
            return False
            
        # Simple rectangle collision
        rover_rect = pygame.Rect(rover.x, rover.y, rover.width, rover.height)
        powerup_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        return rover_rect.colliderect(powerup_rect)

# Game state
class Game:
    def __init__(self, num_players=1):
        self.num_players = num_players
        self.terrain = TerrainGenerator(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.players = [Rover(100, 300)]
        if num_players == 2:
            self.players.append(Rover(150, 300))
            self.players[1].skin = "red"  # Second player uses red rover
        
        self.scroll_speed = 5
        self.hazards = []
        self.powerups = []
        self.score = 0
        self.game_over = False
        self.hazard_timer = 0
        self.powerup_timer = 0
        self.path_coin_timer = 0  # Timer for coins in the pathway
        
        # Ghost data for time trials
        self.recording_ghost = False
        self.ghost_data = []
        self.playing_ghost = False
        self.ghost_position = []
        self.ghost_index = 0
        
        # Load high score
        self.load_high_score()
        
        # Spawn initial fuel powerups
        for _ in range(3):
            x = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH)
            y = random.randint(100, int(self.terrain.ground_height) - 50)
            self.powerups.append(PowerUp(x, y, "fuel"))
    
    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                self.high_score = int(file.read())
        except:
            self.high_score = 0
    
    def save_high_score(self):
        # Only save if player 1's score is higher than current high score
        if len(self.players) > 0 and int(self.players[0].score) > self.high_score:
            self.high_score = int(self.players[0].score)
            try:
                with open("high_score.txt", "w") as file:
                    file.write(str(self.high_score))
            except:
                pass
    
    def update(self):
        if self.game_over:
            return
            
        # Update terrain
        self.terrain.update(self.scroll_speed)
        
        # Update players
        for i, player in enumerate(self.players):
            keys = pygame.key.get_pressed()
            if i == 0:  # First player controls
                if keys[pygame.K_LEFT] and player.fuel > 0:
                    player.x -= player.speed
                if keys[pygame.K_RIGHT] and player.fuel > 0:
                    player.x += player.speed
            elif i == 1:  # Second player controls
                if keys[pygame.K_a] and player.fuel > 0:
                    player.x -= player.speed
                if keys[pygame.K_d] and player.fuel > 0:
                    player.x += player.speed
                if keys[pygame.K_w] and not player.jumping and player.fuel > 5:
                    player.vel_y = -5
                    player.jumping = True
                    player.fuel -= 5  # Jumping consumes fuel
            
            # Keep player on screen
            player.x = max(0, min(player.x, SCREEN_WIDTH - player.width))
            
            player.update(self.terrain, keys)
            
            # Record ghost data if in time trial mode
            if self.recording_ghost and i == 0:
                self.ghost_data.append((player.x, player.y))
            
            # Check if player is out of fuel
            if player.fuel <= 0:
                self.game_over = True
                sounds["game_over"].play()
        
        # Update ghost if playing
        if self.playing_ghost and self.ghost_data:
            if self.ghost_index < len(self.ghost_data):
                self.ghost_position = self.ghost_data[self.ghost_index]
                self.ghost_index += 1
            else:
                self.ghost_index = 0
        
        # Generate hazards
        self.hazard_timer += 1
        if self.hazard_timer >= 120:  # Every 2 seconds
            self.hazard_timer = 0
            if random.random() < 0.7:  # 70% chance to spawn a hazard
                hazard_type = random.choice(["meteor", "laser", "crater"])
                x = SCREEN_WIDTH + 50
                y = random.randint(100, int(self.terrain.ground_height) - 50)
                self.hazards.append(Hazard(x, y, hazard_type))
        
        # Generate pathway coins and fuel every 4 seconds
        self.path_coin_timer += 1
        if self.path_coin_timer >= 240:  # Every 4 seconds (60 FPS * 4)
            self.path_coin_timer = 0
            self.generate_path_coins()
            
            # Add fuel in the middle of the pathway
            if random.random() < 0.7:  # 70% chance to spawn fuel
                x = SCREEN_WIDTH + 150  # Middle of the pathway
                y = int(self.terrain.ground_height) - 50
                self.powerups.append(PowerUp(x, y, "fuel"))
                
                # Play journey sound occasionally
                sounds["journey"].play()
        
        # Generate powerups
        self.powerup_timer += 1
        if self.powerup_timer >= 300:  # Every 5 seconds
            self.powerup_timer = 0
            if random.random() < 0.7:  # 70% chance to spawn a powerup
                # Choose powerup type with different probabilities
                power_type_choices = ["boost", "shield", "magnet", "fuel", "coin", "coin", "coin"]
                power_type = random.choice(power_type_choices)  # Coins are more common
                x = SCREEN_WIDTH + 50
                
                # Position based on type
                if power_type == "coin" and random.random() < 0.7:
                    # Position coins in patterns that require jumping
                    pattern = random.choice(["arc", "steps", "line"])
                    
                    if pattern == "arc":
                        # Create an arc of coins
                        for i in range(5):
                            angle = math.pi * (0.25 + i * 0.1)  # Arc from 45 to 90 degrees
                            radius = 100
                            coin_x = x + i * 30
                            coin_y = int(self.terrain.ground_height) - 50 - int(math.sin(angle) * radius)
                            self.powerups.append(PowerUp(coin_x, coin_y, "coin", True))  # Force floating
                    
                    elif pattern == "steps":
                        # Create ascending steps of coins
                        for i in range(4):
                            coin_x = x + i * 40
                            coin_y = int(self.terrain.ground_height) - 50 - i * 30
                            self.powerups.append(PowerUp(coin_x, coin_y, "coin", True))  # Force floating
                    
                    else:  # line
                        # Create a horizontal line of coins above ground
                        height = random.randint(50, 150)
                        for i in range(5):
                            coin_x = x + i * 30
                            coin_y = int(self.terrain.ground_height) - 50 - height
                            self.powerups.append(PowerUp(coin_x, coin_y, "coin", True))  # Force floating
                else:
                    # Normal ground-level powerup
                    y = random.randint(100, int(self.terrain.ground_height) - 50)
                    self.powerups.append(PowerUp(x, y, power_type))
        
        # Update hazards and check collisions
        for hazard in self.hazards[:]:
            hazard.update(self.scroll_speed)
            
            if not hazard.active:
                self.hazards.remove(hazard)
                continue
                
            for player in self.players:
                if hazard.check_collision(player) and not player.shield_active:
                    player.health -= 10
                    hazard.active = False
                    sounds["crash"].play()
                    
                    if player.health <= 0:
                        self.game_over = True
                        sounds["game_over"].play()
        
        # Update powerups and check collisions
        for powerup in self.powerups[:]:
            powerup.update(self.scroll_speed)
            
            if not powerup.active:
                self.powerups.remove(powerup)
                continue
                
            for player in self.players:
                if powerup.check_collision(player):
                    # Only collect coins if jumping or if they're not coins
                    if powerup.type != "coin" or player.jumping:
                        if powerup.type == "boost":
                            player.activate_boost()
                        elif powerup.type == "shield":
                            player.activate_shield()
                        elif powerup.type == "magnet":
                            # Implement magnet effect (higher jumps)
                            player.vel_y = -8
                            player.jumping = True
                            sounds["powerup"].play()
                        elif powerup.type == "fuel":
                            # Add fuel
                            player.add_fuel(30)
                            sounds["powerup"].play()
                        elif powerup.type == "coin":
                            # Add score - bonus points if the coin was floating (required jumping)
                            bonus = 100
                            if powerup.floating:
                                bonus = 250  # More points for floating coins
                            player.add_score(bonus)
                            sounds["powerup"].play()
                        
                        powerup.active = False
        
        # Increase score based on distance traveled
        for player in self.players:
            player.score += self.scroll_speed / 10
            
            # Consume fuel continuously
            player.fuel -= 0.05  # Constant fuel consumption
    
    def generate_path_coins(self):
        # Generate a path of coins for the player to follow
        x_start = SCREEN_WIDTH + 50
        
        # Choose a pattern for the path
        pattern_type = random.choice(["straight", "zigzag", "curve", "tunnel"])
        
        if pattern_type == "straight":
            # Simple straight line of coins - all floating to require jumps
            y = int(self.terrain.ground_height) - 80  # Higher off the ground
            for i in range(8):
                coin_x = x_start + i * 40
                self.powerups.append(PowerUp(coin_x, y, "coin", True))  # Force floating
        
        elif pattern_type == "zigzag":
            # Zigzag pattern of coins - all floating
            y = int(self.terrain.ground_height) - 80
            for i in range(8):
                coin_x = x_start + i * 40
                offset = 30 if i % 2 == 0 else -30
                self.powerups.append(PowerUp(coin_x, y + offset, "coin", True))  # Force floating
        
        elif pattern_type == "curve":
            # Curved path of coins - all floating
            for i in range(8):
                coin_x = x_start + i * 40
                # Sine wave pattern
                offset = int(math.sin(i * 0.5) * 50)
                coin_y = int(self.terrain.ground_height) - 80 + offset
                self.powerups.append(PowerUp(coin_x, coin_y, "coin", True))  # Force floating
        
        elif pattern_type == "tunnel":
            # Tunnel of coins with obstacles in between - all floating
            y = int(self.terrain.ground_height) - 80
            for i in range(8):
                coin_x = x_start + i * 60
                
                # Add coins at top and bottom of "tunnel"
                self.powerups.append(PowerUp(coin_x, y - 60, "coin", True))  # Force floating
                self.powerups.append(PowerUp(coin_x, y, "coin", True))  # Force floating
                
                # Add obstacle in middle occasionally
                if i > 0 and i < 7 and i % 2 == 1:
                    self.hazards.append(Hazard(coin_x, y - 30, "laser"))
    
    def draw(self, surface):
        # Draw background
        surface.blit(background_img, (0, 0))
        
        # Draw terrain
        self.terrain.draw(surface)
        
        # Draw hazards
        for hazard in self.hazards:
            hazard.draw(surface)
        
        # Draw powerups
        for powerup in self.powerups:
            powerup.draw(surface)
        
        # Draw players
        for player in self.players:
            player.draw(surface)
        
        # Draw ghost if playing
        if self.playing_ghost and self.ghost_position:
            ghost_x, ghost_y = self.ghost_position
            # Draw a semi-transparent version of the rover for the ghost
            ghost_rover = rover_img.copy()
            ghost_rover.set_alpha(128)  # Semi-transparent
            surface.blit(ghost_rover, (ghost_x, ghost_y))
        
        # Draw UI
        font = pygame.font.Font(None, 36)
        
        # Draw player stats
        for i, player in enumerate(self.players):
            # Draw score
            score_text = font.render(f"P{i+1} Score: {int(player.score)}", True, WHITE)
            surface.blit(score_text, (10, 10 + i * 100))
            
            # Draw health bar
            health_text = font.render(f"Health:", True, WHITE)
            surface.blit(health_text, (10, 50 + i * 100))
            pygame.draw.rect(surface, RED, (100, 55 + i * 100, 100, 15))
            pygame.draw.rect(surface, GREEN, (100, 55 + i * 100, player.health, 15))
            
            # Draw fuel bar
            fuel_text = font.render(f"Fuel:", True, WHITE)
            surface.blit(fuel_text, (10, 80 + i * 100))
            pygame.draw.rect(surface, (100, 100, 100), (100, 85 + i * 100, 100, 15))
            fuel_color = (0, 255, 255) if player.fuel > 30 else (255, 165, 0) if player.fuel > 10 else RED
            pygame.draw.rect(surface, fuel_color, (100, 85 + i * 100, player.fuel, 15))
        
        # Draw high score
        if hasattr(self, 'high_score'):
            high_score_text = font.render(f"High Score: {self.high_score}", True, YELLOW)
            surface.blit(high_score_text, (SCREEN_WIDTH - 250, 10))
        
        if self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            surface.blit(overlay, (0, 0))
            
            # Game over text
            game_over_text = font.render("GAME OVER - OUT OF FUEL", True, RED)
            surface.blit(game_over_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 50))
            
            # Show final score
            if len(self.players) == 1:
                final_score = self.players[0].score
                score_text = font.render(f"Final Score: {int(final_score)}", True, WHITE)
                surface.blit(score_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2))
            
            # Restart instructions
            restart_text = font.render("Press ENTER to restart", True, WHITE)
            surface.blit(restart_text, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 50))
            
            # Quit instructions
            quit_text = font.render("Press Q to quit", True, WHITE)
            surface.blit(quit_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90))

# Main menu
def main_menu():
    menu = True
    selected = 0
    options = ["Single Player", "Two Players", "Time Trial", "Quit"]
    
    # Play background music
    try:
        sounds["background_music"].play(-1)  # Loop indefinitely
    except:
        pass
    
    while menu:
        screen.fill(BLACK)
        
        # Draw background
        screen.blit(background_img, (0, 0))
        
        # Draw title
        font_title = pygame.font.Font(None, 72)
        title_text = font_title.render("LUNAR ROVER RACE", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
        
        # Draw menu options
        font_menu = pygame.font.Font(None, 48)
        for i, option in enumerate(options):
            color = YELLOW if i == selected else WHITE
            text = font_menu.render(option, True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250 + i * 60))
        
        pygame.display.update()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                    sounds["jump"].play()
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                    sounds["jump"].play()
                elif event.key == pygame.K_RETURN:
                    sounds["powerup"].play()
                    if selected == 0:  # Single Player
                        return Game(1)
                    elif selected == 1:  # Two Players
                        return Game(2)
                    elif selected == 2:  # Time Trial
                        game = Game(1)
                        game.recording_ghost = True
                        return game
                    elif selected == 3:  # Quit
                        pygame.quit()
                        return None
        
        clock.tick(FPS)

# Main game loop
def main():
    running = True
    game = main_menu()
    
    if game is None:
        return
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and game.game_over:
                    # Save high score before restarting
                    game.save_high_score()
                    
                    # Restart game
                    if game.recording_ghost:
                        # Start time trial with ghost
                        new_game = Game(1)
                        new_game.playing_ghost = True
                        new_game.ghost_data = game.ghost_data
                        game = new_game
                    else:
                        # Normal restart
                        game = Game(game.num_players)
                        
                elif event.key == pygame.K_q:
                    # Quit game
                    running = False
        
        # Update game state
        game.update()
        
        # Draw everything
        game.draw(screen)
        
        # Update display
        pygame.display.update()
        
        # Cap the frame rate
        clock.tick(FPS)
    
    # Save high score before quitting
    if game.game_over:
        game.save_high_score()
    
    pygame.quit()

if __name__ == "__main__":
    main()
