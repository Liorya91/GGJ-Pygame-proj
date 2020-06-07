__author__ = "Mika Wainer && Lior"
 
import pygame
from pygame import *
from os.path import dirname,join
import random
# from player import Player

pygame.init()
font.init()
"""
pygame.font.init()
score_font = pygame.font.SysFont('Comic Sans MS', 30)
score_text_surface = score_font.render('abc',False, (0,0,0))
screen.blit(score_text_surface,(0,0))
"""

def touch(rectA, rectB):
	return rectA.colliderect(rectB)

class Player():
	def __init__(self, screen, name, imageName, init_x, init_y):
		path = dirname(__file__)
		self.screen = screen;
		self.playerObject = image.load(join(path, imageName))
		self.name = name
		self.width = self.playerObject.get_rect().width
		self.height = self.playerObject.get_rect().height
		self.X = init_x
		self.Y = init_y

	def getPos(self):
		return (self.X, self.Y)

	def getPlayerRect(self):
		return Rect(self.X, self.Y, self.width, self.height)
		
	def draw(self, screen):
		screen.blit(self.playerObject, self.getPos())

	def movePlayer(self, direction):
		if direction == pygame.K_LEFT:
			self.X -= 30
			if self.X < 0:
				self.X = 0
				return True
		elif direction == pygame.K_RIGHT:
			self.X += 30
			if self.X > self.screen.get_rect().width - self.width:
				self.X = self.screen.get_rect().width - self.width
				return True
		elif direction == pygame.K_UP:
			self.Y -= 30
			if self.Y < 0:
				self.Y = 0
				return True
		elif direction == pygame.K_DOWN:
			self.Y += 30
			if self.Y > self.screen.get_rect().height - self.height:
				self.Y = self.screen.get_rect().height - self.height
				return True
		return False

	def teleport(self):
		self.X = random.randint(0, 430)
		self.Y = random.randint(0, 260)

class WorldMap():
	def __init__(self, screen):
		path = dirname(__file__)
		self.screen = screen
		self.width = self.screen.get_rect().width
		self.height = self.screen.get_rect().height
		self.bg_image = image.load(join(path,"map2.jpg"))
		self.PlayerA = self.create_player("name", self.width / 4 , self.height /4)
		self.PlayerB = self.create_player("terminator", 3 * self.width / 4, 3 * self.height / 4)
		self.font = font.SysFont('Arial', 30)
		self.score = [0, 0]
		self.DisplayResultText = ""
		self.displayMessage = []
	
	def create_player(self, name, x, y):
		return Player(self.screen, name, 'playerD.png', x, y)

	def draw_background(self):
		self.screen.fill((0,0,0))
		self.screen.blit(self.bg_image,self.bg_image.get_rect(center=self.screen.get_rect().center))
	
	def draw_text(self, text, pos):
		text = str(text)
		label = self.font.render(text, False, (255,0,0))
		self.screen.blit(label, pos)

	def transPlayerMove(self, direction):
		if direction == pygame.K_DOWN:
			return "down"
		elif direction == pygame.K_UP:
			return "up"
		elif direction == pygame.K_RIGHT:
			return "right"
		elif direction == pygame.K_LEFT:
			return "left"

	def round(self, event):
		self.PlayerA.movePlayer(event.key)
		self.calculateScore("playerA")
		direction = random.choice(
				[pygame.K_DOWN, pygame.K_UP, 
				pygame.K_RIGHT, pygame.K_LEFT])
		directionName = self.transPlayerMove(direction)
		if self.PlayerB.movePlayer(direction):
			self.displayMessage.extend(["playerB at <" + directionName + "> boundry" ] * 10)
		else:
			self.displayMessage.extend(["playerB moved " + directionName] * 10)
		self.calculateScore("playerB")
		
	def resetBoard(self):
		self.PlayerA.teleport()
		self.PlayerB.teleport()

	def calculateScore(self, player):
		if touch(self.PlayerA.getPlayerRect(),
			self.PlayerB.getPlayerRect()):
			self.DisplayResultText = 'touchDown - ' + player
			self.resetBoard()
			if player == "playerA":
				self.score = [self.score[0] + 1, self.score[1]]
			else:
				self.score = [self.score[0], self.score[1] + 1]

	def hint(self):
		changeX = random.randint(30, 200)
		changeY = random.randint(30, 200)
		X = self.PlayerB.X - changeX
		Y = self.PlayerB.Y - changeY
		width = self.PlayerB.width + changeX + random.randint(30, 150)
		height = self.PlayerB.height + changeY + random.randint(30, 150)
		return pygame.Rect(X, Y, width, height)
	
	def draw_hint(self, location):
		transperantRed = pygame.Color(255, 0, 0, 64)
		pygame.draw.rect(self.screen, transperantRed, location)

	def run(self):
		displayPlayerB = True
		countSteps = 1
		hint = self.hint()
		mixer.music.play(1000, 15)
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return None
				elif event.type == pygame.KEYDOWN:
					self.DisplayResultText = ""
					displayPlayerB = False
					countSteps += 1
					hint = self.hint()
					self.round(event)
			
			# Redraw the background
			self.draw_background()
			self.draw_text(self.score[0], (10,0))
			if self.DisplayResultText:
				displayPlayerB = True
				countSteps = 1
				self.draw_text(self.DisplayResultText, (200, 0))
			self.draw_text(self.score[1], (620,0))
			if countSteps % 25 == 0:
				self.draw_hint(hint)
			if self.displayMessage:
				self.draw_text(self.displayMessage.pop(0), (0,450))
			self.PlayerA.draw(self.screen)
			if displayPlayerB:
				self.PlayerB.draw(self.screen)
			pygame.display.flip()

if __name__ == "__main__":
	# Creating the screen - 640, 480
	screen = pygame.display.set_mode((640, 480), 0, 32);
	pygame.display.set_caption('cant touch dis')
	pygame.mixer.music.load('cantTouch.ogg')
	worldMapInstance = WorldMap(screen)
	obj = worldMapInstance.run()
	del worldMapInstance
	pygame.quit()