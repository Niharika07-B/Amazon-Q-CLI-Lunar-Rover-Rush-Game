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
    background.fill(BLACK)
    
    # Add stars
    for _ in range(100):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT // 2)  # Stars in upper half
        size = random.randint(1, 3)
        brightness = random.randint(150, 255)
        color = (brightness, brightness, brightness)
        pygame.draw.circle(background, color, (x, y), size)
    
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
    
    return background

# Create built-in sound effects
def create_sound_effect(frequency, duration, volume=0.5, waveform="sine"):
    buffer = bytearray()
    sample_rate = 44100
    max_sample = 32767
    
    for i in range(int(duration * sample_rate)):
        if waveform == "sine":
            value = int(max_sample * volume * math.sin(2 * math.pi * frequency * i / sample_rate))
        elif waveform == "square":
            value = int(max_sample * volume * (1 if math.sin(2 * math.pi * frequency * i / sample_rate) > 0 else -1))
        elif waveform == "sawtooth":
            value = int(max_sample * volume * ((i % int(sample_rate / frequency)) / (sample_rate / frequency) * 2 - 1))
        elif waveform == "noise":
            value = int(max_sample * volume * random.uniform(-1, 1))
        else:  # Default to sine
            value = int(max_sample * volume * math.sin(2 * math.pi * frequency * i / sample_rate))
            
        # Convert to 16-bit little-endian format
        buffer.extend([value & 0xFF, (value >> 8) & 0xFF])
    
    sound = pygame.mixer.Sound(buffer=buffer)
    return sound

# Create space-themed background music
def create_space_music(duration=30):
    # Create a buffer for a longer piece of music
    buffer = bytearray()
    sample_rate = 44100
    max_sample = 32767
    
    # Space-themed chord progression
    chord_progression = [
        [196.00, 293.66, 392.00],  # G minor
        [174.61, 261.63, 349.23],  # F major
        [233.08, 293.66, 349.23],  # Bb major
        [196.00, 293.66, 392.00]   # G minor again
    ]
    
    # Duration of each chord in seconds
    chord_duration = duration / len(chord_progression)
    
    # Create the music
    for chord in chord_progression:
        for i in range(int(chord_duration * sample_rate)):
            # Mix the frequencies with different amplitudes
            value = 0
            for j, freq in enumerate(chord):
                # Fade in/out for smoother transitions
                fade = min(i, sample_rate * chord_duration - i, sample_rate * 0.5) / (sample_rate * 0.5)
                # Add harmonics with decreasing volume
                value += int(max_sample * 0.2 * fade * math.sin(2 * math.pi * freq * i / sample_rate))
                # Add some subtle modulation
                value += int(max_sample * 0.05 * fade * math.sin(2 * math.pi * (freq * 1.01) * i / sample_rate))
            
            # Add a subtle bass line
            bass_freq = chord[0] / 2
            value += int(max_sample * 0.15 * math.sin(2 * math.pi * bass_freq * i / sample_rate))
            
            # Add some ambient noise
            value += int(max_sample * 0.02 * random.uniform(-1, 1))
            
            # Clip to prevent overflow
            value = max(min(value, max_sample), -max_sample)
            
            # Convert to 16-bit little-endian format
            buffer.extend([value & 0xFF, (value >> 8) & 0xFF])
    
    sound = pygame.mixer.Sound(buffer=buffer)
    return sound

# Create engine sound that changes with speed
def create_engine_sound(base_frequency=80, duration=1.0):
    buffer = bytearray()
    sample_rate = 44100
    max_sample = 32767
    
    # Create a loopable engine sound with some harmonics
    for i in range(int(duration * sample_rate)):
        # Base engine tone
        value = int(max_sample * 0.3 * math.sin(2 * math.pi * base_frequency * i / sample_rate))
        
        # Add harmonics
        value += int(max_sample * 0.15 * math.sin(2 * math.pi * (base_frequency * 2) * i / sample_rate))
        value += int(max_sample * 0.1 * math.sin(2 * math.pi * (base_frequency * 3) * i / sample_rate))
        
        # Add some noise for texture
        value += int(max_sample * 0.05 * random.uniform(-1, 1))
        
        # Add some pulsing/vibration
        value = int(value * (0.9 + 0.1 * math.sin(2 * math.pi * 30 * i / sample_rate)))
        
        # Convert to 16-bit little-endian format
        buffer.extend([value & 0xFF, (value >> 8) & 0xFF])
    
    sound = pygame.mixer.Sound(buffer=buffer)
    return sound

# Create sound effects
def load_sound_effects():
    sounds = {}
    
    # Create built-in sound effects
    sounds["jump"] = create_sound_effect(440, 0.3, waveform="sine")  # A4 note
    sounds["boost"] = create_sound_effect(660, 0.5, waveform="sawtooth")  # E5 note with sawtooth wave
    sounds["crash"] = create_sound_effect(220, 0.7, waveform="noise")  # Noise-based crash
    sounds["powerup"] = create_sound_effect(880, 0.2, waveform="square")  # A5 note with square wave
    
    # Create engine sounds at different speeds
    sounds["engine_idle"] = create_engine_sound(80, 1.0)
    sounds["engine_low"] = create_engine_sound(100, 1.0)
    sounds["engine_medium"] = create_engine_sound(120, 1.0)
    sounds["engine_high"] = create_engine_sound(150, 1.0)
    
    # Create space background music
    sounds["background_music"] = create_space_music(30)
    
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
        self.boosting = False
        self.boost_time = 0
        self.shield_active = False
        self.shield_time = 0
        self.skin = "default"  # default or red or green
        self.skins = {"default": "blue", "red": "red", "green": "green"}
        self.engine_sound_playing = False
        self.engine_sound_channel = None
    
    def update(self, terrain, keys):
        # Apply gravity
        self.vel_y += MOON_GRAVITY
        
        # Handle jumping
        if keys[pygame.K_SPACE] and not self.jumping:
            self.vel_y = -5  # Negative velocity means going up
            self.jumping = True
            sounds["jump"].play()
        
        # Update position
        self.y += self.vel_y
        
        # Check for collision with terrain
        terrain_height = terrain.get_height_at(self.x + self.width / 2)
        if self.y + self.height > terrain_height:
            self.y = terrain_height - self.height
            self.vel_y = 0
            self.jumping = False
        
        # Handle boosting
        if self.boosting:
            self.boost_time -= 1
            if self.boost_time <= 0:
                self.boosting = False
                self.speed = 5
        
        # Handle shield
        if self.shield_active:
            self.shield_time -= 1
            if self.shield_time <= 0:
                self.shield_active = False
        
        # Update engine sound based on speed
        self.update_engine_sound()
    
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
    
    def activate_boost(self):
        self.boosting = True
        self.boost_time = 180  # 3 seconds at 60 FPS
        self.speed = 10
        sounds["boost"].play()
    
    def activate_shield(self):
        self.shield_active = True
        self.shield_time = 300  # 5 seconds at 60 FPS
        sounds["powerup"].play()

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
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.type = power_type
        self.width = 20
        self.height = 20
        self.active = True
    
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
        
        # Ghost data for time trials
        self.recording_ghost = False
        self.ghost_data = []
        self.playing_ghost = False
        self.ghost_position = []
        self.ghost_index = 0
    
    def update(self):
        if self.game_over:
            return
            
        # Update terrain
        self.terrain.update(self.scroll_speed)
        
        # Update players
        for i, player in enumerate(self.players):
            keys = pygame.key.get_pressed()
            if i == 0:  # First player controls
                if keys[pygame.K_LEFT]:
                    player.x -= player.speed
                if keys[pygame.K_RIGHT]:
                    player.x += player.speed
            elif i == 1:  # Second player controls
                if keys[pygame.K_a]:
                    player.x -= player.speed
                if keys[pygame.K_d]:
                    player.x += player.speed
                if keys[pygame.K_w] and not player.jumping:
                    player.vel_y = -5
                    player.jumping = True
            
            # Keep player on screen
            player.x = max(0, min(player.x, SCREEN_WIDTH - player.width))
            
            player.update(self.terrain, keys)
            
            # Record ghost data if in time trial mode
            if self.recording_ghost and i == 0:
                self.ghost_data.append((player.x, player.y))
        
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
        
        # Generate powerups
        self.powerup_timer += 1
        if self.powerup_timer >= 300:  # Every 5 seconds
            self.powerup_timer = 0
            if random.random() < 0.5:  # 50% chance to spawn a powerup
                power_type = random.choice(["boost", "shield", "magnet"])
                x = SCREEN_WIDTH + 50
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
        
        # Update powerups and check collisions
        for powerup in self.powerups[:]:
            powerup.update(self.scroll_speed)
            
            if not powerup.active:
                self.powerups.remove(powerup)
                continue
                
            for player in self.players:
                if powerup.check_collision(player):
                    if powerup.type == "boost":
                        player.activate_boost()
                    elif powerup.type == "shield":
                        player.activate_shield()
                    elif powerup.type == "magnet":
                        # Implement magnet effect (higher jumps)
                        player.vel_y = -8
                        player.jumping = True
                        sounds["powerup"].play()
                    
                    powerup.active = False
        
        # Increase score
        self.score += 1
    
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
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        surface.blit(score_text, (10, 10))
        
        for i, player in enumerate(self.players):
            health_text = font.render(f"P{i+1} Health: {player.health}", True, WHITE)
            surface.blit(health_text, (10, 50 + i * 40))
        
        if self.game_over:
            game_over_text = font.render("GAME OVER", True, RED)
            surface.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
            restart_text = font.render("Press R to restart", True, WHITE)
            surface.blit(restart_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 50))

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
                if event.key == pygame.K_r and game.game_over:
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
        
        # Update game state
        game.update()
        
        # Draw everything
        game.draw(screen)
        
        # Update display
        pygame.display.update()
        
        # Cap the frame rate
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
