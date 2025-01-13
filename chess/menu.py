import pygame as p

DEPTH = 0

class ChessMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.bg_color = (237, 238, 209)
        self.text_color = (0, 0, 0)
        self.hover_color = (119, 153, 82)  # Dark green for hover
        self.button_color = (237, 238, 209)
        
    def drawText(self, screen, text, x, y, font_size=30, is_hover=False):
        font = p.font.SysFont("Times New Roman", font_size, False, False)
        # Calculate text width to center
        text_surface = font.render(text, True, self.text_color)
        text_width = text_surface.get_width()
        
        # Create button background
        button_rect = p.Rect(x, y, text_width + 40, font_size + 20)
        button_color = self.hover_color if is_hover else self.button_color
        p.draw.rect(screen, button_color, button_rect, border_radius=10)
        
        # Center text in button
        text_x = x + (button_rect.width - text_width) // 2
        text_y = y + (button_rect.height - font_size) // 2
        
        screen.blit(text_surface, (text_x, text_y))
        return button_rect

    def show_main_menu(self, screen):
        screen.fill(self.bg_color)
        
        # Center title
        title = self.drawText(screen, "Chess Game", 
                            self.width//2 - 150, 100, 70)
        
        # Store button states
        pvp_hover = False
        pvai_hover = False
        
        # Initial button draw
        pvp_button = self.drawText(screen, "Player vs Player", 
                                 self.width//2 - 120, 250, 30, pvp_hover)
        pvai_button = self.drawText(screen, "Player vs AI", 
                                  self.width//2 - 120, 320, 30, pvai_hover)
        
        while True:
            mouse_pos = p.mouse.get_pos()
            
            # Check hover states
            pvp_hover = pvp_button.collidepoint(mouse_pos)
            pvai_hover = pvai_button.collidepoint(mouse_pos)
            
            # Redraw buttons with hover effects
            pvp_button = self.drawText(screen, "Player vs Player", 
                                     self.width//2 - 120, 250, 30, pvp_hover)
            pvai_button = self.drawText(screen, "Player vs AI", 
                                      self.width//2 - 120, 320, 30, pvai_hover)
            
            p.display.flip()
            
            for e in p.event.get():
                if e.type == p.QUIT:
                    return None, None
                if e.type == p.MOUSEBUTTONDOWN:
                    if pvp_button.collidepoint(mouse_pos):
                        return "PVP", None
                    elif pvai_button.collidepoint(mouse_pos):
                        return "PVAI", self.show_difficulty_menu(screen)

    def show_difficulty_menu(self, screen):
        screen.fill(self.bg_color)
        
        # Draw title
        title = self.drawText(screen, "Select Difficulty", self.width//2 - 120, 100, 50)
        
        # Draw difficulty buttons 
        easy_button = self.drawText(screen, "Easy", self.width//2 - 50, 200)
        medium_button = self.drawText(screen, "Medium", self.width//2 - 50, 250)
        hard_button = self.drawText(screen, "Hard", self.width//2 - 50, 300)
        impossible_button = self.drawText(screen, "Impossible", self.width//2 - 50, 350)
        
        p.display.flip()
        
        while True:
            for e in p.event.get():
                if e.type == p.QUIT:
                    return None
                if e.type == p.MOUSEBUTTONDOWN:
                    mouse_pos = p.mouse.get_pos()
                    if easy_button.collidepoint(mouse_pos):
                        return 1  # 10% depth
                    elif medium_button.collidepoint(mouse_pos):
                        return 2  # 40% depth  
                    elif hard_button.collidepoint(mouse_pos):
                        return 3  # 80% depth
                    elif impossible_button.collidepoint(mouse_pos):
                        return 4  # 99% depth