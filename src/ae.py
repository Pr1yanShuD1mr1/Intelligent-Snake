from tkinter import Tk, Label
from random import randint, choice
from time import sleep



class Game:

    def __init__(self, size=(20,20), agent=None):
        row, col = size
        self.row = row if row <= 30 else 30 # for preventing recursion error in track_food
        self.col = col if col <= 30 else 30
        self.agent = agent
        self.win = None

    def _create_window(self):
        if self.win is not None and self.win.winfo_exists():
            self.win.destroy()

        self.win = Tk()
        self.win.title("Intelligent Snake")
        self.win.geometry(f"{self.col*18}x{self.row*18}")





    def setup_board(self):

        # □ 0   vacant
        # ■ 1   wall
        # ▣ 2   snake
        # ● 3   food/player

        self.board    = []
        self.labels   = []
        self.rewards  = []
        self.gameover = False
        self.score    = 0


        # defining the board with walls
        for r in range(self.row):
            rowB = []
            rowL = []
            for c in range(self.col):
                wall = r in (0, self.row-1) or c in (0, self.col-1)
                char, inT = ("■", 1) if wall else (" ", 0)

                label = Label(self.win, text=char)
                label.place(x=c*18, y=r*18)
                rowL.append(label)
                rowB.append(inT)

            self.board.append(rowB)
            self.labels.append(rowL)





    def suggest_vacancy(self):
        vacancy = self.entity[0]
        while vacancy in self.entity:
            vacancy = [randint(1, self.row-2), randint(1, self.col-2)]
        return vacancy





    def initialize(self):
        # creating a movable body for snake and allocating a random place in board
        self.entity = []
        self.entity.append([randint(1, self.row-2), randint(1, self.col-2)])

        x, y = self.entity[0]
        self.labels[x][y].config(text="▣")
        self.board[x][y] = 2

        # allocating food in a place where snake is not present
        self.food = self.suggest_vacancy()

        x, y = self.food
        self.labels[x][y].config(text="●")
        self.board[x][y] = 3





    def on_key_press(self, event):
        key   = event.keysym.lower()
        if key not in ('w', 's', 'a', 'd'): return

        fx, fy = self.food
        if key == 'w': xn, yn = (fx - 1 if 1 < fx < self.row - 1 else self.row - 2), fy
        if key == 's': xn, yn = (fx + 1 if 0 < fx < self.row - 2 else 1), fy
        if key == 'a': xn, yn = fx, (fy - 1 if 1 < fy < self.col - 1 else self.col - 2)
        if key == 'd': xn, yn = fx, (fy + 1 if 0 < fy < self.col - 2 else 1)

        if self.board[xn][yn] != 0: return

        self.board[fx][fy] = 0
        self.labels[fx][fy].config(text=" ")

        self.food = [xn, yn]
        self.board[xn][yn] = 3
        self.labels[xn][yn].config(text="●")

        self.win.update()





    def track_food(self, path, blocked=None):
        if blocked is None: blocked = list()

        current    = path[-1]
        directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        
        # Optimization: Sort directions by distance to food to prevent wild spirals
        if hasattr(self, 'food'):
            fx, fy = self.food
            directions.sort(key = lambda d: abs(current[0] + d[0] - fx) + abs(current[1] + d[1] - fy))

        possible_moves = []
        for dx, dy in directions:
            nx, ny = current[0]+dx, current[1]+dy
            # Skip if visited or in the current path
            if [nx, ny] in blocked or [nx, ny] in path: continue

            # Check boundaries to avoid index errors
            if 0 < nx < self.row and 0 < ny < self.col:
                match self.board[nx][ny]:
                    case 0: possible_moves.append([nx, ny]) # vacant
                    case 3: return path+[[nx, ny]]          # food

        # Recursively test possible moves
        for move in possible_moves:
            blocked.append(move)
            Route = self.track_food(path+[move], blocked)
            if Route: return Route

        return None  # No path found





    def state(self):
        """Return the current game state for agent decision-making."""

        def collision(cell):
            x, y = cell
            if x < 0 or x >= self.row : return True
            if y < 0 or y >= self.col : return True
            if self.board[x][y] == 1  : return True
            if self.board[x][y] == 2  : return [x, y] != self.entity[-1]
            return False

        hx, hy = self.entity[0]
        fx, fy = self.food

        nextCell = {
            'w': (hx-1, hy),
            's': (hx+1, hy),
            'a': (hx, hy-1),
            'd': (hx, hy+1),
        }

        leftSide  = {'w':'a', 's':'d', 'a':'s', 'd':'w'}
        rightSide = {'w':'d', 's':'a', 'a':'w', 'd':'s'}

        return [
            self.direction == 'a',     # snake is moving to left
            self.direction == 'd',     # snake is moving to right
            self.direction == 'w',     # snake is moving to up
            self.direction == 's',     # snake is moving to down

            fy < hy,                   # food is in left direction
            fy > hy,                   # food is in right direction
            fx < hx,                   # food is in up direction
            fx > hx,                   # food is in down direction

            collision(nextCell[self.direction]),            # going straight is collision
            collision(nextCell[rightSide[self.direction]]), # moving right will lead to collision
            collision(nextCell[leftSide[self.direction]]),  # moving left will lead to collision
        ]





    def render_snake(self):
        self.snake = []

        symbols = {
            # segments symbol 
            "endpoint"  : { (-1, 0) : "▲", (1, 0)  : "▼", (0, -1) : "◀", (0, 1)  : "▶", },
            "straight"  : { (-1, 0) : "⇓", (1, 0)  : "⇑", (0, -1) : "⇒", (0, 1)  : "⇐", },
            "corner" : {
                ((-1, 0), (0,  1)) : "⇙",
                ((-1, 0), (0, -1)) : "⇘",
                (( 1, 0), (0,  1)) : "⇖",
                (( 1, 0), (0, -1)) : "⇗", 
            }
        }

        n = len(self.entity)
        for i, curr in enumerate(self.entity):
            if n == 1:
                symbol = "▣"
            elif i == 0:
                next_seg = self.entity[1]
                head_delta = (curr[0] - next_seg[0], curr[1] - next_seg[1])
                symbol = symbols["endpoint"].get(head_delta, "▣") 
            elif i == n - 1:
                prev_seg = self.entity[i - 1]
                tail_delta = (curr[0] - prev_seg[0], curr[1] - prev_seg[1])
                symbol = symbols["endpoint"].get(tail_delta, "▣") 
            else:
                prev_seg = self.entity[i - 1]
                next_seg = self.entity[i + 1]
                dir_from_prev = (curr[0] - prev_seg[0], curr[1] - prev_seg[1])
                dir_to_next = (next_seg[0] - curr[0], next_seg[1] - curr[1])

                if dir_from_prev == dir_to_next:
                    symbol = symbols["straight"].get(dir_from_prev, "▣")
                else:
                    symbol = symbols["corner"].get((dir_from_prev, dir_to_next), "●")

            self.snake.append(symbol)
            x, y = curr
            self.labels[x][y].config(text=symbol)

        return self.snake





    def Run(self, debugOutput=False):
        self.gameover = False
        self._create_window()
        self.setup_board()
        self.initialize()

        self.direction = choice(['w', 'a', 's', 'd'])

        leftSide  = {'w':'a', 's':'d', 'a':'s', 'd':'w'}
        rightSide = {'w':'d', 's':'a', 'a':'w', 'd':'s'}

        def move_snake():
            if self.gameover: return

            old_state = self.state()
            action = self.agent.next_move(old_state)

            match action.index(1):
                case 0: self.direction = leftSide[self.direction]
                case 1: pass # Go straight
                case 2: self.direction = rightSide[self.direction]

            xp, yp = self.entity[0]
            if self.direction == 'w': xn, yn = (xp - 1 if 1 < xp < self.row - 1 else self.row - 2), yp
            if self.direction == 's': xn, yn = (xp + 1 if 0 < xp < self.row - 2 else 1), yp
            if self.direction == 'a': xn, yn = xp, (yp - 1 if 1 < yp < self.col - 1 else self.col - 2)
            if self.direction == 'd': xn, yn = xp, (yp + 1 if 0 < yp < self.col - 2 else 1)

            reward = 0
            food_caught = self.board[xn][yn] == 3

            # Check for collision
            if self.board[xn][yn] == 2:
                tail = self.entity[-1]
                if tail == [xn, yn] and not food_caught:
                    collision = False
                    self.entity.insert(0, [xn, yn])
                else:
                    collision = True
                    self.gameover = True
                    reward = -10
            else:
                collision = False
                self.entity.insert(0, [xn, yn])

            # Manage snake body length
            if not food_caught and not collision:
                x, y = self.entity.pop()
                self.board[x][y] = 0
                self.labels[x][y].config(text=" ")
                reward = -0.1 

            for x, y in self.entity:
                self.board[x][y] = 2
                self.labels[x][y].config(text="▣")

            self.render_snake()

            # Check for food collection
            if food_caught:
                self.food = self.suggest_vacancy()
                x, y = self.food
                self.labels[x][y].config(text="●")
                self.board[x][y] = 3
                self.score += 1
                reward = 10

            new_state = self.state()
            self.agent.fit(old_state, action, reward, new_state, self.gameover)

            # Debugging output
            if debugOutput:
                print(f"you:{str(self.food):8} dir:{str(self.direction):2} head:{str(self.entity[0]):8} len:{len(self.entity):2}")

            if self.gameover:
                self.win.quit()
                return

            self.win.after(100, move_snake)

        self.win.bind("<KeyPress>", self.on_key_press)
        self.win.after(100, move_snake)
        self.win.mainloop()




# if __name__ == "__main__":
#     Game().Run()