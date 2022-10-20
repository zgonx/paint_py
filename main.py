from utils import *
from utils.InputBox import InputBox

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drawing Program")


def init_grid(rows, cols, color):
    grid = []

    for i in range(rows):
        grid.append([])
        for _ in range(cols):
            grid[i].append(color)

    return grid


def draw_grid(win, grid):
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (j * PIXEL_SIZE, i *
                                          PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    if DRAW_GRID_LINES:
        for i in range(ROWS + 1):
            pygame.draw.line(win, BLACK, (0, i * PIXEL_SIZE),
                             (WIDTH, i * PIXEL_SIZE))

        for i in range(COLS + 1):
            pygame.draw.line(win, BLACK, (i * PIXEL_SIZE, 0),
                             (i * PIXEL_SIZE, HEIGHT - TOOLBAR_HEIGHT))


def draw(win, grid, buttons):
    win.fill(BG_COLOR)
    draw_grid(win, grid)

    for button in buttons:
        button.draw(win)

    pygame.display.update()

def draw_line(x_y_list,color):
    x1 = x_y_list[0][0]
    x2 = x_y_list[1][0]
    y1 = x_y_list[0][1]
    y2 = x_y_list[1][1]
    print (x1,x2,y1,y2)
    drawing_color = color
    if x1==x2 and y1==y2:
        grid[x1][y1] = drawing_color
    else:
        if abs(x2-x1)>abs(y2-y1):
            a = (y2-y1)/(x2-x1)
            if x1>x2:
                x1,x2 = x2,x1
                y1,y2 = y2,y1
            for x in range(x1,x2):
                y = round(y1+a*(x-x1))
                grid[x][y] = drawing_color
        else:
            a=(x2-x1)/(y2-y1)
            if y1>y2:
                x1,x2 = x2,x1
                y1,y2 = y2,y1
            for y in range(y1,y2):
                x = round(x1+a*(y-y1))
                grid[x][y] = drawing_color


def get_row_col_from_pos(pos):
    x, y = pos
    row = y // PIXEL_SIZE
    col = x // PIXEL_SIZE

    if row >= ROWS:
        raise IndexError

    return row, col


run = True
clock = pygame.time.Clock()
grid = init_grid(ROWS, COLS, BG_COLOR)
drawing_color = BLACK
last_2_pos = []
done = False
save_txt = ''

button_y = HEIGHT - TOOLBAR_HEIGHT/2 - 75
buttons = [
    Button(10, button_y, 50, 50, BLACK),
    Button(70, button_y, 50, 50, RED),
    Button(130, button_y, 50, 50, GREEN),
    Button(190, button_y, 50, 50, BLUE),
    Button(250, button_y, 50, 50, WHITE, "Erase", BLACK),
    Button(310, button_y, 50, 50, WHITE, "Clear", BLACK),
    Button(370, button_y, 50, 50, WHITE, "Line", BLACK),
    Button(430, button_y, 50, 50, WHITE, "Save", BLACK),
]

boxes = [
    InputBox(10,button_y+100,140,32),
    # InputBox(250,button_y+100,140,32)
]

while run:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            
            try:
                row, col = get_row_col_from_pos(pos)
                if len(last_2_pos)>1:
                    last_2_pos = last_2_pos[:0]
                last_2_pos.append(get_row_col_from_pos(pos))
                print(last_2_pos) 
                grid[row][col] = drawing_color
            except IndexError:
                for button in buttons:
                    if not button.clicked(pos):
                        continue

                    
                    if button.text == "Clear":
                        grid = init_grid(ROWS, COLS, BG_COLOR)
                        drawing_color = BLACK
                    if button.text == "Line":
                        if len(last_2_pos)==2:
                            draw_line(last_2_pos,drawing_color)
                        else:
                            continue
                    drawing_color = button.color
                    if button.text == "Save":
                        boxes[0].draw(WIN)
                        while not done:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    done = True
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_s:
                                        if pygame.key.get_mods() & pygame.KMOD_CTRL:
                                            done = True
                                for box in boxes:
                                    box.handle_event(event)

                            for box in boxes:
                                box.update()

                            # WIN.fill((30, 30, 30))
                            for box in boxes:
                                save_txt = box.text
                                box.draw(WIN)
                                
                            pygame.display.flip()
                        done = False
                        print(save_txt+".jpeg")
                        pygame.image.save(WIN, save_txt+".jpeg")

    draw(WIN, grid, buttons)

pygame.quit()