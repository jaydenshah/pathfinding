import pygame

pygame.init()

# change this stuff
fps = 60
win_size = 1000 # window size
board_size = 20 # size of board in squares
width = 2 # width of grid lines
detail = True # determines whether to show green/red colors, always True if animate is True
animate = True # determines whether to animate pathfinding or find a path instantly
anim_interval = 5 # frames between each pathfinding update if animate is True
move_diagonally = False # determines whether a square can move diagonally

# some of the worst variable names in the world
square_size = win_size / board_size
hold = False
hold_count = 0
old_hold_count = 0
start_end_count = 0
button = 1
mode = "create"
is_pathfinding = False
if animate:
    detail = True

win = pygame.display.set_mode((win_size, win_size))
pygame.display.set_caption("Pathfinding")
clock = pygame.time.Clock()

class Board:
    def __init__(self):
        self.board = []
        self.path_board = []
        for y in range(board_size):
            self.board.append([])
            self.path_board.append([])
            for x in range(board_size):
                self.board[y].append(0)
                self.path_board[y].append(0)

    def get_mouse_pos(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        square_x = int(max(min(mouse_x // square_size, board_size - 1), 0))
        square_y = int(max(min(mouse_y // square_size, board_size - 1), 0))
        return square_x, square_y

    def on_click(self, click_type=1):
        global old_hold_count
        global start_end_count
        global mode
        
        x, y = self.get_mouse_pos()
        if hold_count != old_hold_count:
            old_hold_count = hold_count
            if (self.board[y][x] == 1 and click_type == 1) or (self.board[y][x] == 2 and click_type == 3):
                mode = "remove"
            else:
                mode = "create"

        if mode == "remove":
            if self.board[y][x] == 2:
                start_end_count -= 1
            self.board[y][x] = 0
        else:
            if click_type == 1:
                if self.board[y][x] == 2:
                    start_end_count -= 1
                self.board[y][x] = 1
            elif click_type == 3 and start_end_count < 2:
                if self.board[y][x] != 2:
                    start_end_count += 1
                self.board[y][x] = 2

    def pathfind(self):
        self.distances = []
        current_square = []
        neighbours = [[0, -1], [-1, 0], [1, 0], [0, 1]]
        if move_diagonally:
            neighbours = [[-1, -1], [0, -1], [1, -1], [-1, 0], [0, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
        destination_square = []
        start_square = []
        
        for y in range(board_size):
            self.distances.append([])
            for x in range(board_size):
                # [dist, shortest dist?, prev square to get to shortest dist]
                if self.board[y][x] == 1:
                    self.distances[y].append([float("inf"), True, [None, None]])
                elif self.board[y][x] == 2 and current_square == []:
                    current_square = [x, y]
                    start_square = [x, y]
                    self.distances[y].append([0, True, [x, y]])
                else:
                    if self.board[y][x] == 2 and current_square != []:
                        destination_square = [x, y]
                    self.distances[y].append([float("inf"), False, [None, None]])

        if start_square == [] or destination_square == []:
            print("You need at least 2 start/end points to make a path")
            return None
        
        while True:
            for neighbour in neighbours:
                try:
                    x = current_square[0] + neighbour[0]
                    y = current_square[1] + neighbour[1]
                    if x not in range(board_size) or y not in range(board_size):
                        raise Exception
                    if self.distances[y][x][1] == False:
                        dist = self.distances[current_square[1]][current_square[0]][0] + 1
                        if neighbour in [[-1, -1], [1, -1], [-1, 1], [1, 1]] and move_diagonally:
                            dist += 0.41
                        if dist < self.distances[y][x][0]:
                            self.distances[y][x][0] = dist
                            self.distances[y][x][2] = current_square
                            if detail:
                                self.path_board[y][x] = 2
                except:
                    pass

            minimum = float("inf")
            old_current_square = current_square
            for i in range(board_size):
                for j in range(board_size):
                    if self.distances[i][j][1] == False and self.distances[i][j][0] < minimum:
                        minimum = self.distances[i][j][0]
                        current_square = [j, i]
                        
            self.distances[current_square[1]][current_square[0]][1] = True
            if detail:
                self.path_board[current_square[1]][current_square[0]] = 3

            if animate:
                self.display()
                pygame.time.wait(anim_interval)

            if current_square == destination_square:
                print("Path found!")
                prev_square = self.distances[current_square[1]][current_square[0]][2]
                while prev_square != start_square:
                    self.path_board[prev_square[1]][prev_square[0]] = 1
                    current_square = prev_square
                    prev_square = self.distances[current_square[1]][current_square[0]][2]
                    if animate:
                        self.display()
                        pygame.time.wait(anim_interval)
                break
            elif current_square == old_current_square:
                print("No path exists")
                break
        
    def display(self):
        win.fill((0, 0, 0))
        for y in range(board_size):
            for x in range(board_size):
                if self.path_board[y][x] == 1:
                    pygame.draw.rect(win, (0, 0, 255), (x * square_size, y * square_size, square_size, square_size))
                elif self.path_board[y][x] == 2:
                    pygame.draw.rect(win, (255, 0, 0), (x * square_size, y * square_size, square_size, square_size))
                elif self.path_board[y][x] == 3:
                    pygame.draw.rect(win, (0, 255, 0), (x * square_size, y * square_size, square_size, square_size))
                    
                if self.board[y][x] == 1:
                    pygame.draw.rect(win, (255, 255, 255), (x * square_size, y * square_size, square_size, square_size))
                elif self.board[y][x] == 2:
                    pygame.draw.rect(win, (255, 255, 0), (x * square_size, y * square_size, square_size, square_size))

        for i in range(1, board_size):
            pygame.draw.line(win, (255, 255, 255), (i * square_size, 0), (i * square_size, win_size), width)
            pygame.draw.line(win, (255, 255, 255), (0, i * square_size), (win_size, i * square_size), width)

        pygame.display.update()
                
board = Board()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            hold = True
            hold_count += 1
            button = event.button
        if event.type == pygame.MOUSEBUTTONUP:
            hold = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                is_pathfinding = True
                board.pathfind()
            
    if hold and not is_pathfinding:
        board.on_click(button)
                
    
    board.display()

    clock.tick(fps)

pygame.quit()
