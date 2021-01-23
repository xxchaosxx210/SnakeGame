from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint

FRAME_RATE_SPEED = .25
MOVEMENT_SPEED = 60

class SnakePart(Widget):
    pass

class GameScreen(Widget):
    
    step_size = MOVEMENT_SPEED
    snake_parts = []
    movement_x = 0
    movement_y = 0
    frame_counter = 0
    
    def new_game(self):
        for part in self.snake_parts:
            self.remove_widget(part)
        self.ids.food.pos = (randint(40, Window.width-40), randint(0, Window.height-40))
        self.snake_parts = []
        self.movement_x = 0
        self.movement_y = 0
        head = SnakePart()
        head.pos = (0, 0)
        self.snake_parts.append(head)
        self.add_widget(head)
    
    def collides_widget(self, wid1, wid2):
        if wid1.right <= wid2.x:
            return False
        if wid1.x >= wid2.right:
            return False
        if wid1.top <= wid2.y:
            return False
        if wid1.y >= wid2.top:
            return False
        return True    
    
    def on_touch_up(self, touch):
        dx = touch.x - touch.opos[0]
        dy = touch.y - touch.opos[1]
        if abs(dx) > abs(dy):
            # Moving left or Right
            self.movement_y = 0
            if dx > 0:
                # Moving right
                self.movement_x = self.step_size
            else:
                # Moving Left
                self.movement_x = - self.step_size
        else:
            self.movement_x = 0
            # Moving up or down
            if dy > 0:
                # Moving up
                self.movement_y = self.step_size
            else:
                # Moving Down
                self.movement_y = - self.step_size
    
    def next_frame(self, *args):
        # get the snake head widget
        head = self.snake_parts[0]
        # get the food widget
        food = self.ids.food
        # store the last snake parts position
        last_x = self.snake_parts[-1].x
        last_y = self.snake_parts[-1].y
        
        # Move the body
        for i, part in enumerate(self.snake_parts):
            # head widget ignore
            if i == 0:
                continue
            # get the previous snake part position and assign it to the current snake part
            part.new_y = self.snake_parts[i-1].y
            part.new_x = self.snake_parts[i-1].x
        for part in self.snake_parts[1:]:
            part.y = part.new_y
            part.x = part.new_x
        
        # Move the Snake
        head.x += self.movement_x
        head.y += self.movement_y
        
        # Check collisions
        # check if Snake eats food
        if self.collides_widget(head, food):
            # Set New random position for snake on screen
            food.x = randint(0, Window.width - food.width)
            food.y = randint(0, Window.height - food.height)
            # Create new part to snake
            new_part = SnakePart()
            # store new snake part position the same as snake heads position
            new_part.x = last_x
            new_part.y = last_y
            self.snake_parts.append(new_part)
            self.add_widget(new_part)
        # check for snake colliding with snake
        for i, part in enumerate(self.snake_parts):
            if i == 0:
                continue
            if self.collides_widget(part, head):
                print(f"{part.x}, {part.y}")
                print(f"{head.x}, {head.y}")
                self.new_game()
        # check for snake colliding with wall out of bounds
        if not self.collides_widget(self, head):
            self.new_game()
        #if head.x >= self.width:
            #head.x = self.width - head.width
        #if head.x < 0:
            #head.x = 0
        #if head.y < 0:
            #head.y = 0
        #if head.y >= self.height:
            #head.y = self.height - head.height
            
class MainApp(App):
    
    def on_start(self):
        self.root.new_game()
        Clock.schedule_interval(self.root.next_frame, FRAME_RATE_SPEED)

def main():
    MainApp().run()

if __name__ == '__main__':
    main()