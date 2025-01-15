import sys
import pygame as p
from engine import GameState, Move

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 10
BUTTON_COLOR = (119, 153, 82)
BUTTON_TEXT_COLOR = (255, 255, 255)

LIGHT_SQUARE_COLOR = (237, 238, 209)
DARK_SQUARE_COLOR = (119, 153, 82)
MOVE_HIGHLIGHT_COLOR = (84, 115, 161)
POSSIBLE_MOVE_COLOR = (255, 255, 51)

def loadImages():
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK',
              'bp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wp']
    for piece in pieces:
        image_path = "images1/" + piece + ".png"
        original_image = p.image.load(image_path)
        IMAGES[piece] = p.transform.smoothscale(
            original_image, (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()

    screen.fill(p.Color(LIGHT_SQUARE_COLOR))
    moveLogFont = p.font.SysFont("Times New Roman", 12, False, False)
    
    loadImages()
    running = True
    board = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    ]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

        drawPieces(screen, board)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(
                    col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                
def pawnPromotionPopup(screen, gs):
    font = p.font.SysFont("Times New Roman", 30, False, False)
    text = font.render("Choose promotion:", True, p.Color("black"))

    button_width, button_height = 100, 100
    buttons = [
        p.Rect(100, 200, button_width, button_height),
        p.Rect(200, 200, button_width, button_height),
        p.Rect(300, 200, button_width, button_height),
        p.Rect(400, 200, button_width, button_height)
    ]

    if gs.whiteToMove:
        button_images = [
            p.transform.smoothscale(p.image.load(
                "images1/bQ.png"), (100, 100)),
            p.transform.smoothscale(p.image.load(
                "images1/bR.png"), (100, 100)),
            p.transform.smoothscale(p.image.load(
                "images1/bB.png"), (100, 100)),
            p.transform.smoothscale(p.image.load("images1/bN.png"), (100, 100))
        ]
    else:
        button_images = [
            p.transform.smoothscale(p.image.load(
                "images1/wQ.png"), (100, 100)),
            p.transform.smoothscale(p.image.load(
                "images1/wR.png"), (100, 100)),
            p.transform.smoothscale(p.image.load(
                "images1/wB.png"), (100, 100)),
            p.transform.smoothscale(p.image.load("images1/wN.png"), (100, 100))
        ]

    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            elif e.type == p.MOUSEBUTTONDOWN:
                mouse_pos = e.pos
                for i, button in enumerate(buttons):
                    if button.collidepoint(mouse_pos):
                        if i == 0:
                            return "Q"  # Queen
                        elif i == 1:
                            return "R" # Rook
                        elif i == 2:
                            return "B" # Bishop
                        else:
                            return "N" # Knight

        screen.fill(p.Color(LIGHT_SQUARE_COLOR))
        screen.blit(text, (110, 150))

        for i, button in enumerate(buttons):
            p.draw.rect(screen, p.Color("white"), button)
            screen.blit(button_images[i], button.topleft)

        p.display.flip()

def main():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
        
    gs = GameState()
    if gs.playerWantsToPlayAsBlack:
        gs.board = gs.board1

    screen.fill(p.Color(LIGHT_SQUARE_COLOR))
    moveLogFont = p.font.SysFont("Times New Roman", 12, False, False)
    gs = GameState()
    if (gs.playerWantsToPlayAsBlack):
        gs.board = gs.board1
    validMoves = gs.getValidMoves()
    moveMade = False 
    animate = False  
    loadImages()
    running = True
    squareSelected = ()  
    playerClicks = []
    gameOver = False 
    AIThinking = False  
    moveFinderProcess = None
    moveUndone = False
    pieceCaptured = False
    positionHistory = ""
    previousPos = ""
    countMovesForDraw = 0
    COUNT_DRAW = 0
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE 
                    row = location[1]//SQ_SIZE
                    
                    undo_button, restart_button = drawButtons(screen)
                    
                    if undo_button.collidepoint(location):
                        gs.undoMove()
                        moveMade = True
                        animate = False
                        gameOver = False
                        if AIThinking:
                            moveFinderProcess.terminate()
                            AIThinking = False
                        moveUndone = True

                    elif restart_button.collidepoint(location):
                        screen.fill(p.Color(LIGHT_SQUARE_COLOR))
                            
                        gs = GameState()
                        if gs.playerWantsToPlayAsBlack:
                            gs.board = gs.board1
                                
                        validMoves = gs.getValidMoves()
                        squareSelected = ()
                        playerClicks = []
                        moveMade = False
                        animate = False
                        gameOver = False
                        if AIThinking:
                            moveFinderProcess.terminate()
                            AIThinking = False
                        moveUndone = True
                        continue
                    
                    if squareSelected == (row, col) or col >= 8:
                        squareSelected = () 
                        playerClicks = []  
                    else:
                        squareSelected = (row, col)
                        playerClicks.append(squareSelected)
                        if not moveMade:
                            playerClicks = [squareSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()  
                        AIThinking = False
                    moveUndone = True
                if e.key == p.K_r: 
                    gs = GameState()
                    validMoves = gs.getValidMoves()
                    squareSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()  
                        AIThinking = False
                    moveUndone = True

        if moveMade:
            if countMovesForDraw == 0 or countMovesForDraw == 1 or countMovesForDraw == 2 or countMovesForDraw == 3:
                countMovesForDraw += 1
            if countMovesForDraw == 4:
                positionHistory += gs.getBoardString()
                if previousPos == positionHistory:
                    COUNT_DRAW += 1
                    positionHistory = ""
                    countMovesForDraw = 0
                else:
                    previousPos = positionHistory
                    positionHistory = ""
                    countMovesForDraw = 0
                    COUNT_DRAW = 0
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
            moveUndone = False

        undo_button, restart_button = drawGameState(screen, gs, validMoves, squareSelected, moveLogFont)

        if COUNT_DRAW == 1:
            gameOver = True
            text = 'Draw due to repetition'
            drawEndGameText(screen, text)
        if gs.stalemate:
            gameOver = True
            text = 'Stalemate'
            drawEndGameText(screen, text)
        elif gs.checkmate:
            gameOver = True
            text = 'Black wins by checkmate' if gs.whiteToMove else 'White wins by checkmate'
            drawEndGameText(screen, text)

        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs, validMoves, squareSelected, moveLogFont):
    drawSquare(screen) 
    highlightSquares(screen, gs, validMoves, squareSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)
    return drawButtons(screen)  

def drawSquare(screen):
    global colors
    colors = [p.Color(LIGHT_SQUARE_COLOR), p.Color(DARK_SQUARE_COLOR)]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row + col) % 2)]
            p.draw.rect(screen, color, p.Rect(
                col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def highlightSquares(screen, gs, validMoves, squareSelected):
    if squareSelected != (): 
        row, col = squareSelected
        if gs.board[row][col][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color(MOVE_HIGHLIGHT_COLOR))
            screen.blit(s, (col*SQ_SIZE, row*SQ_SIZE))
            s.fill(p.Color(POSSIBLE_MOVE_COLOR))
            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(
                    col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(
        BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color(LIGHT_SQUARE_COLOR), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []

    for i in range(0, len(moveLog), 2):
        moveString = " " + str(i//2 + 1) + ". " + str(moveLog[i]) + " "
        if i+1 < len(moveLog):
            moveString += str(moveLog[i+1])
        moveTexts.append(moveString)

    movesPerRow = 3
    padding = 10
    lineSpacing = 5
    textY = padding

    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i+j]

        textObject = font.render(text, True, p.Color('black'))

        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)

        textY += textObject.get_height() + lineSpacing

def animateMove(move, screen, board, clock):
    global colors
    deltaRow = move.endRow - move.startRow
    deltaCol = move.endCol - move.startCol
    framesPerSquare = 5
    frameCount = (abs(deltaRow) + abs(deltaCol)) * framesPerSquare
    for frame in range(frameCount + 1):
        row, col = ((move.startRow + deltaRow*frame/frameCount, move.startCol +
                    deltaCol*frame/frameCount)) 
        drawSquare(screen)
        drawPieces(screen, board)

        color = colors[(move.endRow + move.endCol) %
                       2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow *
                           SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)

        if move.pieceCaptured != '--':
            if move.isEnpassantMove:
                enPassantRow = move.endRow + \
                    1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSquare = p.Rect(move.endCol*SQ_SIZE, enPassantRow *
                                   SQ_SIZE, SQ_SIZE, SQ_SIZE) 
            screen.blit(IMAGES[move.pieceCaptured], endSquare)

        screen.blit(IMAGES[move.pieceMoved], p.Rect(
            col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

        p.display.flip()
        clock.tick(240)

def drawEndGameText(screen, text):
    font = p.font.SysFont("Times New Roman", 30, False, False)
    textObject = font.render(text, True, p.Color('black'))

    text_width = textObject.get_width()
    text_height = textObject.get_height()

    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(
        BOARD_WIDTH/2 - text_width/2, BOARD_HEIGHT/2 - text_height/2)

    screen.blit(textObject, textLocation)

    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(1, 1))

def drawButtons(screen):
    normal_color = BUTTON_COLOR
    hover_color = (82, 110, 57)  
    
    mouse_pos = p.mouse.get_pos()
    
    undo_button = p.Rect(
        BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH - (BUTTON_WIDTH * 2 + BUTTON_MARGIN), 
        BOARD_HEIGHT - (BUTTON_HEIGHT + BUTTON_MARGIN),
        BUTTON_WIDTH, 
        BUTTON_HEIGHT
    )
    
    restart_button = p.Rect(
        BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH - (BUTTON_WIDTH + BUTTON_MARGIN),
        BOARD_HEIGHT - (BUTTON_HEIGHT + BUTTON_MARGIN),
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    )
    
    undo_color = hover_color if undo_button.collidepoint(mouse_pos) else normal_color
    restart_color = hover_color if restart_button.collidepoint(mouse_pos) else normal_color
    
    p.draw.rect(screen, undo_color, undo_button, border_radius=10)
    p.draw.rect(screen, restart_color, restart_button, border_radius=10)
    
    font = p.font.SysFont("Times New Roman", 20, False, False)
    undo_text = font.render("Undo", True, BUTTON_TEXT_COLOR)
    restart_text = font.render("Restart", True, BUTTON_TEXT_COLOR)
    
    if undo_button.collidepoint(mouse_pos):
        undo_button.y -= 2
    if restart_button.collidepoint(mouse_pos):
        restart_button.y -= 2
    
    screen.blit(undo_text, (
        undo_button.centerx - undo_text.get_width()//2,
        undo_button.centery - undo_text.get_height()//2
    ))
    screen.blit(restart_text, (
        restart_button.centerx - restart_text.get_width()//2,
        restart_button.centery - restart_text.get_height()//2
    ))
    
    return undo_button, restart_button

if __name__ == "__main__":
    main()
