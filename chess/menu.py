import pygame as p

p.mixer.init()
p.mixer.music.load("sounds/dep.mp3")  # Replace with the path to your file
p.mixer.music.play(-1) 
p.mixer.music.set_volume(0.2)
music_muted = False

class ChessMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.button_color = (128, 128, 128)
        self.hover_color = (69, 70, 76)
        self.text_color = (255, 255, 255)
        self.border_color = (255, 215, 0)  # Gold color
        self.bg_color = (40, 40, 40)
        self.font_path = "font/soviet.ttf"  # Add font path
        self.font = p.font.Font(self.font_path, 20)
        self.title_font = p.font.Font(self.font_path, 50)
        self.help_button_width = 200
        self.help_button_height = 40
        self.help_showing = False

    def drawText(self, screen, text, y, font_size=30, is_hover=False):
        # Load custom font
        font = p.font.Font(self.font_path, font_size)
        text_surface = font.render(text.upper(), True, self.text_color)

        # Calculate text width and height to center it
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        x = (self.width - text_width) // 2

        # Define button rect and colors
        button_rect = p.Rect(x - 20, y, text_width + 40, text_height + 20)
        button_color = self.hover_color if is_hover else self.button_color

        # Draw button background with a bold gold border
        p.draw.rect(screen, self.border_color, button_rect.inflate(4, 4))
        p.draw.rect(screen, button_color, button_rect)

        # Center text within the button
        text_x = x
        text_y = y + (button_rect.height - text_height) // 2

        screen.blit(text_surface, (text_x, text_y))
        return button_rect
    
    def draw_Mute_button(self, screen):
        help_text = "Mute music"
        text_surface = self.font.render(help_text, True, self.text_color)
        
        # Position in bottom left
        x = 40
        y = self.height - 60
        
        # Create button rectangle
        button_rect = p.Rect(x, y, self.help_button_width, self.help_button_height)
        
        # Check hover
        mouse_pos = p.mouse.get_pos()
        is_hover = button_rect.collidepoint(mouse_pos)
        button_color = self.hover_color if is_hover else self.button_color
        
        # Draw button
        p.draw.rect(screen, self.border_color, button_rect.inflate(4, 4))
        p.draw.rect(screen, button_color, button_rect)
        
        # Center text
        text_x = button_rect.centerx - text_surface.get_width() // 2
        text_y = button_rect.centery - text_surface.get_height() // 2
        screen.blit(text_surface, (text_x, text_y))
        
        return button_rect
    
    def show_overlay(self, screen):
        # Semi-transparent background
        overlay = p.Surface((self.width, self.height))
        overlay.set_alpha(0)  # Adjust alpha for better visibility
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Help message box
        msg_width, msg_height = 800, 400
        msg_rect = p.Rect(
            (self.width - msg_width) // 2,
            (self.height - msg_height) // 2,
            msg_width, msg_height
        )
        
        # Draw message box
        p.draw.rect(screen, self.button_color, msg_rect)
        p.draw.rect(screen, self.border_color, msg_rect, 2)
        
        # Help content
        help_lines = [
            "Welcome to OstblockChess!",
            "",
            "You are not allowed to mute music in this game.",
            "Nobody deserves to smile",
            "Stay depressed, кomrade.",
            "",
            "",
            "Кlиcк anиwhere to кl0se"
        ]
        
        y = msg_rect.top + 40
        for line in help_lines:
            text = self.font.render(line, True, self.text_color)
            x = msg_rect.centerx - text.get_width() // 2
            screen.blit(text, (x, y))
            y += 40
    
    

    def show_main_menu(self, screen):
        running = True
        while running:
            screen.fill(self.bg_color)

            # Draw title in a large font, centered
            self.drawText(screen, "OSTblock ChEsS", 100, 70)

            # Initialize button states
            buttons = [
                ("Player vs Player", 250),
                ("Player vs AI", 320),
                ("Fisher's vs AI", 390),
                ("Fisher's PvP", 460),
            ]
            button_rects = []
            mute_button = self.draw_Mute_button(screen)

            # Draw all buttons
            for text, y in buttons:
                button_rects.append(self.drawText(screen, text, y, 30))

            for event in p.event.get():
                if event.type == p.QUIT:
                    return None, None
                    
                if event.type == p.MOUSEBUTTONDOWN:
                    mouse_pos = p.mouse.get_pos()
                    if mute_button.collidepoint(mouse_pos):
                        self.help_showing = True
                    elif self.help_showing:
                        self.help_showing = False
                    else:
                        # Handle other button clicks
                        for i, rect in enumerate(button_rects):
                            if rect.collidepoint(mouse_pos):
                                options = ["PVP", "PVAI", "FISCHER", "FISCHER_PVP"]
                                if i == 1:  # "Player vs AI" needs difficulty menu
                                    return options[i], self.show_difficulty_menu(screen)
                                return options[i], None
                            
            mouse_pos = p.mouse.get_pos()

            # Redraw buttons with hover effects
            for i, (text, y) in enumerate(buttons):
                is_hover = button_rects[i].collidepoint(mouse_pos)
                button_rects[i] = self.drawText(screen, text, y, 30, is_hover)

            # Draw help overlay if showing
            if self.help_showing:
                self.show_overlay(screen)

            p.display.flip()

    def show_difficulty_menu(self, screen):
        screen.fill(self.bg_color)

        # Draw title in a large font, centered
        self.drawText(screen, "Choose slozhnostt'", 100, 50)

        # Draw difficulty buttons
        difficulties = [
            ("easи", 200),
            ("mediум", 270),
            ("harд", 340),
            ("impoссiбlе", 410),
        ]
        button_rects = []

        for text, y in difficulties:
            button_rects.append(self.drawText(screen, text, y, 30))

        p.display.flip()

        while True:
            mouse_pos = p.mouse.get_pos()

            # Update hover states
            for i, (text, y) in enumerate(difficulties):
                is_hover = button_rects[i].collidepoint(mouse_pos)
                button_rects[i] = self.drawText(screen, text, y, 30, is_hover)

            p.display.flip()

            for e in p.event.get():
                if e.type == p.QUIT:
                    return None
                if e.type == p.MOUSEBUTTONDOWN:
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(mouse_pos):
                            difficulties_config = ["1", "2", "3", "4"]
                            with open("difficulty-config.txt", "w") as file:
                                file.write(f'"difficulty": {difficulties_config[i]}')
                            return i + 1
