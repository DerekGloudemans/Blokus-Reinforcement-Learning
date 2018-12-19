from graphics import *
from random import seed, randint
from time import clock

top_left_x = 100
top_left_y = 100
width = 60
height = 60
# num_rows = int(input('Number of rows: '))  # commented out for now
num_columns = int(input('Number of columns: '))

window = GraphWin('Lab 4B', 800, 800)
top_left_point = Point(top_left_x, top_left_y)
bottom_right_point = Point(top_left_x + width, top_left_y + height)
enclosing_rectangle = Rectangle(top_left_point, bottom_right_point)
enclosing_rectangle.setFill(random_color())
enclosing_rectangle.draw(window)

window.getMouse()
window.close()