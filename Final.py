#This program is a simple verson of the game pong

import pygame
import random

# Paddle properties
PADDLE_WIDTH = 25
PADDLE_HEIGHT = 100
PADDLE_COLOR = (0, 0, 0)
PADDLE_SPEED = 6


# Ball properties
BALL_RADIUS = 20
BALL_COLOR = (0, 0, 0)
BALL_INITIAL_VX = -5
BALL_INITIAL_VY = -5


# Base object class
class Object:

# Initializes the object with coordinates, size and color
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vx = 0
        self.vy = 0
        self.color = color


# Updates object by moving it and checking if it's in screen range
    def update(self, screenWidth, screenHeight):
        self.x += self.vx
        self.y += self.vy

        if self.x < 0: self.x = 0
        if self.y < 0: self.y = 0
        if self.x > screenWidth - self.w: self.x = screenWidth - self.w
        if self.y > screenHeight - self.h: self.y = screenHeight - self.h


    def draw(self, surface):
        pass


    # Returns whether object collides with another object (rectangular collision detection)
    def collides(self, obj):
        return self.y < obj.y + obj.h and self.y + self.h > obj.y and self.x < obj.x + obj.w and self.x + self.w > obj.x


    # Called when object collides with anoher object, must be implemented by child classes
    def onCollide(self, obj):
        pass


# Paddle class  
class Paddle(Object):

    # Initializes Paddle object
    def __init__(self, x, y):
        super(Paddle, self).__init__(x, y, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_COLOR)

    # Draws paddle with a rectangle
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.w, self.h))

    # Moves paddle up
    def moveUp(self):
        self.vy -= PADDLE_SPEED

    # Moves paddle down
    def moveDown(self):
        self.vy = PADDLE_SPEED

    # Stops moving the paddle
    def stopMoving(self):
        self.vy = 0


# ComputerPaddle class
class ComputerPaddle(Paddle):

    # Initializes ComputerPaddle object
    def __init__(self, x, y):
        super(ComputerPaddle, self).__init__(x, y)

    # Adjust Y-velocity based on speed and direction of ball
    def update(self, ball, screenWidth, screenHeight):
        super(ComputerPaddle, self).update(screenWidth, screenHeight)

        if ball.vx < 0: 
            self.stopMoving()
            return

        ballX = ball.x
        ballY = ball.y
        ballVX = ball.vx
        ballVY = ball.vy

        while ballX + ball.w < self.x:
            ballX += ballVX
            ballY += ballVY
            if ballY < 0 or ballY > screenHeight - ball.h: ballVY = -ballVY

        if ballY > self.y + self.h: self.moveDown()
        elif ballY + ball.h < self.y: self.moveUp()
        else: self.stopMoving()


# Ball class
class Ball(Object):

    # Initializes the Ball object along with initial velocities
    def __init__(self, x, y):
        super(Ball, self).__init__(x, y, BALL_RADIUS, BALL_RADIUS, BALL_COLOR)
        self.startX = x
        self.startY = y
        self.vx = BALL_INITIAL_VX
        self.vy = BALL_INITIAL_VY


# Updates the ball object, if it hits screen edge then negate velocity
    def update(self, screenWidth, screenHeight):
        super(Ball, self).update(screenWidth, screenHeight)

        if self.x == 0 or self.x == screenWidth - self.w: self.vx = -self.vx
        if self.y == 0 or self.y == screenHeight - self.h: self.vy = -self.vy


# Resets the ball back to its initial coordinates
    def reset(self):
        self.x = self.startX
        self.y = self.startY
        self.vx = BALL_INITIAL_VX
        self.vy = BALL_INITIAL_VY

# Draws a circle onto screen to represent the ball
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.w)


# If ball collides with another object, then negate both velocities by a random amount
    def onCollide(self, obj): 

# If ball is "inside" of paddle, then reposition it so it's just outside the paddle
        if self.x < obj.x + obj.w: self.x = obj.x + obj.w
        elif self.x + self.w > obj.x: self.x = obj.x - self.w
        if self.y < obj.y + obj.h: self.y = obj.y + obj.h
        elif self.y + self.h > obj.y: self.y = obj.y - self.h

        rx = int(random.uniform(-3, 5))
        ry = int(random.uniform(-2, 4))

        self.vx = -self.vx + rx
        self.vy = -self.vy + ry