import cv2
import mediapipe as mp
import pygame
import numpy as np
import random
import time
import math
from threading import Thread
import queue

class CameraGameLevels:
    def __init__(self):
        # Initialize MediaPipe
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Game variables
        self.screen_width = 640
        self.screen_height = 480
        self.game_running = True
        self.collision_detected = False
        self.start_time = time.time()
        self.fullscreen = False
        
        # Level system
        self.current_level = 1
        self.max_level = 5
        
        # Level configurations
        self.level_configs = {
            1: {"speed": 2.0, "star_size": 25, "color": (255, 255, 0)},    # Yellow
            2: {"speed": 3.0, "star_size": 22, "color": (255, 165, 0)},   # Orange
            3: {"speed": 4.0, "star_size": 20, "color": (255, 0, 0)},     # Red
            4: {"speed": 5.0, "star_size": 18, "color": (128, 0, 128)},   # Purple
            5: {"speed": 6.0, "star_size": 15, "color": (0, 255, 255)}    # Cyan
        }
        
        # Star size options
        self.star_size_options = {
            "Small": 15,
            "Medium": 20,
            "Large": 25,
            "Extra Large": 30
        }
        
        # Get current level config
        config = self.level_configs[self.current_level]
        self.object_speed = config["speed"]
        self.object_radius = config["star_size"]
        self.object_color = config["color"]
        
        # Moving object properties
        self.object_x = random.randint(50, self.screen_width - 50)
        self.object_y = random.randint(50, self.screen_height - 50)
        self.object_dx = random.choice([-1, 1]) * self.object_speed
        self.object_dy = random.choice([-1, 1]) * self.object_speed
        
        # Player tracking
        self.player_positions = []
        self.max_player_positions = 10
        
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Camera Touch Game - Level Selection")
        self.clock = pygame.time.Clock()
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.ORANGE = (255, 165, 0)
        self.PURPLE = (128, 0, 128)
        self.CYAN = (0, 255, 255)
        self.GRAY = (128, 128, 128)
        
        # Font
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        
        # Camera frame queue for threading
        self.frame_queue = queue.Queue(maxsize=1)
        self.camera_surface = None
        
        # Menu state
        self.show_menu = True
        self.selected_level = 1
        self.selected_star_size = "Medium"
        
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.screen_width, self.screen_height = self.screen.get_size()
        else:
            self.screen = pygame.display.set_mode((640, 480))
            self.screen_width, self.screen_height = 640, 480
        
        # Update window title
        if self.show_menu:
            pygame.display.set_caption("Camera Touch Game - Level Selection")
        else:
            pygame.display.set_caption(f"Camera Touch Game - Level {self.current_level} ({self.selected_star_size} Star)")
    
    def show_level_selection_menu(self):
        """Show level and star size selection menu"""
        self.screen.fill(self.BLACK)
        
        # Title
        title_text = self.large_font.render("Camera Touch Game", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.font.render("Select Your Settings", True, self.YELLOW)
        subtitle_rect = subtitle_text.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Level selection
        level_title = self.font.render("Select Level:", True, self.WHITE)
        self.screen.blit(level_title, (50, 150))
        
        y_pos = 200
        for level in range(1, self.max_level + 1):
            config = self.level_configs[level]
            color = config["color"]
            speed = config["speed"]
            size = config["star_size"]
            
            # Level button
            if level == self.selected_level:
                pygame.draw.rect(self.screen, self.GREEN, (50, y_pos - 5, 500, 40))
            
            level_text = self.small_font.render(f"Level {level}: Speed {speed}, Size {size}px", True, self.WHITE)
            self.screen.blit(level_text, (60, y_pos))
            
            # Draw star preview
            star_x = 450
            star_y = y_pos + 10
            self.draw_star(star_x, star_y, size, color)
            
            y_pos += 50
        
        # Star size selection
        size_title = self.font.render("Custom Star Size:", True, self.WHITE)
        self.screen.blit(size_title, (50, 450))
        
        size_y = 480
        size_x = 50
        for size_name, size_value in self.star_size_options.items():
            if size_name == self.selected_star_size:
                pygame.draw.rect(self.screen, self.BLUE, (size_x - 5, size_y - 5, 120, 30))
            
            size_text = self.small_font.render(size_name, True, self.WHITE)
            self.screen.blit(size_text, (size_x, size_y))
            
            # Draw star preview
            self.draw_star(size_x + 100, size_y + 10, size_value, self.YELLOW)
            
            size_x += 130
        
        # Instructions
        instruction_text = self.small_font.render("Use UP/DOWN arrows to select level, LEFT/RIGHT for star size", True, self.WHITE)
        self.screen.blit(instruction_text, (50, 520))
        
        start_text = self.font.render("Press ENTER to start game", True, self.GREEN)
        self.screen.blit(start_text, (50, 550))
        
        # Fullscreen instruction
        fullscreen_text = self.small_font.render("Press F11 to toggle fullscreen", True, self.WHITE)
        self.screen.blit(fullscreen_text, (50, 580))
        
        pygame.display.flip()
        
        # Handle menu input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_level = max(1, self.selected_level - 1)
                        self.show_level_selection_menu()
                    elif event.key == pygame.K_DOWN:
                        self.selected_level = min(self.max_level, self.selected_level + 1)
                        self.show_level_selection_menu()
                    elif event.key == pygame.K_LEFT:
                        size_names = list(self.star_size_options.keys())
                        current_index = size_names.index(self.selected_star_size)
                        self.selected_star_size = size_names[max(0, current_index - 1)]
                        self.show_level_selection_menu()
                    elif event.key == pygame.K_RIGHT:
                        size_names = list(self.star_size_options.keys())
                        current_index = size_names.index(self.selected_star_size)
                        self.selected_star_size = size_names[min(len(size_names) - 1, current_index + 1)]
                        self.show_level_selection_menu()
                    elif event.key == pygame.K_RETURN:
                        return True
                    elif event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                        self.show_level_selection_menu()
                    elif event.key == pygame.K_ESCAPE:
                        return False
            
            # Cap frame rate for menu
            self.clock.tick(60)
        
        return False
    
    def apply_user_selections(self):
        """Apply user's level and star size selections"""
        self.current_level = self.selected_level
        config = self.level_configs[self.current_level]
        self.object_speed = config["speed"]
        self.object_color = config["color"]
        
        # Use custom star size if selected
        self.object_radius = self.star_size_options[self.selected_star_size]
        
        # Reset object position
        self.object_x = random.randint(50, self.screen_width - 50)
        self.object_y = random.randint(50, self.screen_height - 50)
        self.object_dx = random.choice([-1, 1]) * self.object_speed
        self.object_dy = random.choice([-1, 1]) * self.object_speed
        
        # Update window title
        pygame.display.set_caption(f"Camera Touch Game - Level {self.current_level} ({self.selected_star_size} Star)")
    
    def update_level(self):
        """Update to next level"""
        if self.current_level < self.max_level:
            self.current_level += 1
            config = self.level_configs[self.current_level]
            self.object_speed = config["speed"]
            self.object_color = config["color"]
            
            # Keep the user's selected star size
            self.object_radius = self.star_size_options[self.selected_star_size]
            
            # Reset object position
            self.object_x = random.randint(50, self.screen_width - 50)
            self.object_y = random.randint(50, self.screen_height - 50)
            self.object_dx = random.choice([-1, 1]) * self.object_speed
            self.object_dy = random.choice([-1, 1]) * self.object_speed
            
            # Update window title
            pygame.display.set_caption(f"Camera Touch Game - Level {self.current_level} ({self.selected_star_size} Star)")
            return True
        return False
    
    def update_moving_object(self):
        """Update the position of the moving object"""
        self.object_x += self.object_dx
        self.object_y += self.object_dy
        
        # Bounce off walls
        if self.object_x <= self.object_radius or self.object_x >= self.screen_width - self.object_radius:
            self.object_dx *= -1
            self.object_x = max(self.object_radius, min(self.screen_width - self.object_radius, self.object_x))
            
        if self.object_y <= self.object_radius or self.object_y >= self.screen_height - self.object_radius:
            self.object_dy *= -1
            self.object_y = max(self.object_radius, min(self.screen_height - self.object_radius, self.object_y))
    
    def detect_player_position(self, frame):
        """Detect player position using MediaPipe pose estimation"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        
        if results.pose_landmarks:
            nose = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.NOSE]
            screen_x = int(nose.x * self.screen_width)
            screen_y = int(nose.y * self.screen_height)
            
            self.player_positions.append((screen_x, screen_y))
            
            if len(self.player_positions) > self.max_player_positions:
                self.player_positions.pop(0)
            
            return True, (screen_x, screen_y)
        
        return False, None
    
    def check_collision(self):
        """Check if player collides with the moving object"""
        if not self.player_positions:
            return False
        
        player_x, player_y = self.player_positions[-1]
        distance = math.sqrt((player_x - self.object_x)**2 + (player_y - self.object_y)**2)
        player_radius = 30
        return distance < (self.object_radius + player_radius)
    
    def camera_thread(self):
        """Thread for processing camera frames"""
        while self.game_running:
            ret, frame = self.cap.read()
            if ret:
                player_detected, player_pos = self.detect_player_position(frame)
                
                if player_detected and self.check_collision():
                    self.collision_detected = True
                
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_surface = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))
                
                try:
                    self.frame_queue.put_nowait(frame_surface)
                except queue.Full:
                    try:
                        self.frame_queue.get_nowait()
                        self.frame_queue.put_nowait(frame_surface)
                    except queue.Empty:
                        pass
    
    def draw_game(self):
        """Draw the game interface"""
        if self.camera_surface:
            self.screen.blit(self.camera_surface, (0, 0))
        else:
            self.screen.fill(self.BLACK)
        
        # Draw moving object (star)
        self.draw_star(self.object_x, self.object_y, self.object_radius, self.object_color)
        
        # Draw player positions
        if self.player_positions:
            for i, (x, y) in enumerate(self.player_positions):
                alpha = int(255 * (i + 1) / len(self.player_positions))
                color = (0, alpha, 255 - alpha)
                pygame.draw.circle(self.screen, color, (x, y), 5)
            
            current_x, current_y = self.player_positions[-1]
            pygame.draw.circle(self.screen, self.GREEN, (current_x, current_y), 10, 2)
            pygame.draw.circle(self.screen, self.GREEN, (current_x, current_y), 30, 1)
        
        # Draw UI
        self.draw_ui()
    
    def draw_star(self, x, y, radius, color):
        """Draw a star shape"""
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            if i % 2 == 0:
                r = radius
            else:
                r = radius * 0.5
            points.append((x + r * math.cos(angle), y + r * math.sin(angle)))
        
        pygame.draw.polygon(self.screen, color, points)
    
    def draw_ui(self):
        """Draw user interface elements"""
        # Level display
        level_text = self.small_font.render(f"Level: {self.current_level}/{self.max_level}", True, self.WHITE)
        self.screen.blit(level_text, (10, 10))
        
        # Timer
        elapsed_time = time.time() - self.start_time
        timer_text = self.small_font.render(f"Time: {elapsed_time:.1f}s", True, self.WHITE)
        self.screen.blit(timer_text, (10, 35))
        
        # Speed indicator
        speed_text = self.small_font.render(f"Speed: {self.object_speed:.1f}", True, self.WHITE)
        self.screen.blit(speed_text, (10, 60))
        
        # Star size indicator
        size_text = self.small_font.render(f"Star Size: {self.object_radius} ({self.selected_star_size})", True, self.WHITE)
        self.screen.blit(size_text, (10, 85))
        
        # Instructions
        instruction_text = self.small_font.render("Touch the star with your body!", True, self.WHITE)
        self.screen.blit(instruction_text, (10, self.screen_height - 30))
        
        # Fullscreen instruction
        fullscreen_text = self.small_font.render("F11: Toggle Fullscreen", True, self.WHITE)
        self.screen.blit(fullscreen_text, (10, self.screen_height - 55))
    
    def show_level_complete_screen(self):
        """Show level complete screen"""
        self.screen.fill(self.BLACK)
        
        elapsed_time = time.time() - self.start_time
        
        if self.current_level < self.max_level:
            complete_text = self.large_font.render(f"LEVEL {self.current_level} COMPLETE!", True, self.GREEN)
            complete_rect = complete_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 80))
            self.screen.blit(complete_text, complete_rect)
            
            time_text = self.font.render(f"Time: {elapsed_time:.1f} seconds", True, self.WHITE)
            time_rect = time_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 30))
            self.screen.blit(time_text, time_rect)
            
            next_level_text = self.small_font.render(f"Next Level: {self.current_level + 1} (Harder!)", True, self.YELLOW)
            next_level_rect = next_level_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 10))
            self.screen.blit(next_level_text, next_level_rect)
            
            continue_text = self.small_font.render("Press SPACE to continue or ESC to quit", True, self.WHITE)
            continue_rect = continue_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
            self.screen.blit(continue_text, continue_rect)
        else:
            complete_text = self.large_font.render("GAME COMPLETE!", True, self.GREEN)
            complete_rect = complete_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 80))
            self.screen.blit(complete_text, complete_rect)
            
            time_text = self.font.render(f"Total Time: {elapsed_time:.1f} seconds", True, self.WHITE)
            time_rect = time_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 30))
            self.screen.blit(time_text, time_rect)
            
            congrats_text = self.small_font.render("Congratulations! You beat all levels!", True, self.YELLOW)
            congrats_rect = congrats_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 10))
            self.screen.blit(congrats_text, congrats_rect)
            
            restart_text = self.small_font.render("Press SPACE to restart or ESC to quit", True, self.WHITE)
            restart_rect = restart_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True
                    elif event.key == pygame.K_ESCAPE:
                        return False
            
            # Cap frame rate for menu
            self.clock.tick(60)
        
        return False
    
    def reset_game(self):
        """Reset the game state"""
        self.collision_detected = False
        self.start_time = time.time()
        self.player_positions = []
        self.current_level = 1
        
        config = self.level_configs[self.current_level]
        self.object_speed = config["speed"]
        self.object_color = config["color"]
        self.object_radius = self.star_size_options[self.selected_star_size]
        
        self.object_x = random.randint(50, self.screen_width - 50)
        self.object_y = random.randint(50, self.screen_height - 50)
        self.object_dx = random.choice([-1, 1]) * self.object_speed
        self.object_dy = random.choice([-1, 1]) * self.object_speed
        
        pygame.display.set_caption(f"Camera Touch Game - Level {self.current_level} ({self.selected_star_size} Star)")
    
    def run(self):
        """Main game loop"""
        # Show level selection menu first
        if not self.show_level_selection_menu():
            return
        
        # Apply user selections
        self.apply_user_selections()
        
        # Start camera thread
        camera_thread = Thread(target=self.camera_thread, daemon=True)
        camera_thread.start()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_F11:
                        self.toggle_fullscreen()
            
            try:
                self.camera_surface = self.frame_queue.get_nowait()
            except queue.Empty:
                pass
            
            if self.collision_detected:
                if self.show_level_complete_screen():
                    if self.current_level < self.max_level:
                        self.update_level()
                        self.collision_detected = False
                        self.start_time = time.time()
                    else:
                        self.reset_game()
                else:
                    running = False
            else:
                self.update_moving_object()
                self.draw_game()
                pygame.display.flip()
                self.clock.tick(60)
        
        self.game_running = False
        self.cap.release()
        pygame.quit()

if __name__ == "__main__":
    print("Starting Camera Touch Game - Level System...")
    print("Instructions:")
    print("- Select your preferred level and star size before starting")
    print("- Use UP/DOWN arrows to select level")
    print("- Use LEFT/RIGHT arrows to select star size")
    print("- Press ENTER to start the game")
    print("- Press F11 to toggle fullscreen mode")
    print("- Complete 5 levels with increasing difficulty")
    print("- Move your body to touch the star")
    print("- Press ESC to quit")
    
    game = CameraGameLevels()
    try:
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    finally:
        print("Game ended") 