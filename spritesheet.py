import pygame

class Spritesheet:
	def __init__(self, file, rows, columns, scale = 1, colorkey = (0,0,0)):
		self.spritesheet = pygame.image.load(file).convert_alpha()
		self.spritesheet = pygame.transform.scale(self.spritesheet, (self.spritesheet.get_rect()[2] * scale, self.spritesheet.get_rect()[3] * scale))
		self.scale = scale
		self.rows = rows
		self.columns = columns
		self.cells = rows * columns
		self.rect = self.spritesheet.get_rect()
		self.cell_width = self.rect.width / self.columns
		self.cell_height = self.rect.height / self.rows
		self.colorkey = colorkey

		self.images = []
		for row in range(self.rows):
			for column in range(self.columns):
				image = pygame.Surface((self.cell_width, self.cell_height)).convert_alpha()
				image.blit(self.spritesheet, (0,0), (column * self.cell_width, row * self.cell_height, self.cell_width, self.cell_height))
				image.set_colorkey(self.colorkey)
				self.images.append(image)

	def get_frames(self, first_image_idx, last_image_idx):
		idx = first_image_idx
		frames = []
		for i in range(1 + (last_image_idx - first_image_idx)):
			frames.append(self.images[idx])
			idx += 1
		return frames

	def get_flipped_frames(self, first_image_idx, last_image_idx, horizontal_flip = True, vertical_flip = False):
		idx = first_image_idx
		frames = []
		for i in range(1 + (last_image_idx - first_image_idx)):
			image = self.images[idx]
			image = pygame.transform.flip(image, horizontal_flip, vertical_flip)
			frames.append(image)
			image.set_colorkey(self.colorkey)
			idx += 1
		return frames


class Animation:
	def __init__(self, type, interruptible = True, cycle = False,
		spritesheet = "none", first_image_idx = 0, last_image_idx = 0,    # Necessary for a spritesheet
		filename = "none", number_of_frames = 0, scale = 1, starting_idx = 1, filetype = ".png"):    # Necessary for a folder

		self.type = type
		self.interruptible = interruptible
		self.cycle = cycle
		self.scale = scale
		self.number_of_frames = number_of_frames

		if self.type == "spritesheet":
			self.frames = spritesheet.get_frames(first_image_idx, last_image_idx)
			self.flipped_frames = spritesheet.get_flipped_frames(first_image_idx, last_image_idx)
			self.number_of_frames = len(self.frames)

		if self.type == "folder":
			self.frames = []
			self.flipped_frames = []
			for i in range(number_of_frames):
				image = pygame.image.load(filename + str(i + starting_idx) + filetype).convert_alpha()
				image = pygame.transform.scale(image, (image.get_rect()[2] * self.scale, image.get_rect()[3] * self.scale))
				flipped_image = pygame.transform.flip(image, True, False)
				image.set_colorkey((0,0,0))
				self.frames.append(image)
				self.flipped_frames.append(flipped_image)

		self.x_size = self.frames[0].get_rect()[2]
		self.y_size = self.frames[0].get_rect()[3]







def run_test():
	import time
	pygame.init()
	screen = pygame.display.set_mode((500,500))
	clock = pygame.time.Clock()

	warrior = Spritesheet("./assets/Warrior/SpriteSheet/Warrior_Sheet_Effect.png", 17, 6, scale = 4)
	run = Animation("folder", True, True, filename = "./assets/Warrior/IndividualSprites/Run/Warrior_Run_", number_of_frames = 8, scale = 4, starting_idx = 1, filetype = ".png")
	run_right = run.frames
	run_left = run.flipped_frames
	idle = Animation("folder", True, True, filename = "./assets/Warrior/IndividualSprites/idle/Warrior_Idle_", number_of_frames = 6, scale = 4, starting_idx = 1, filetype = ".png")
	idle_right = idle.frames
	idle_left = idle.flipped_frames
	death = Animation("folder", True, True, filename = "./assets/Warrior/IndividualSprites/Death-Effect/Warrior_Death_", number_of_frames = 11, scale = 4, starting_idx = 1, filetype = ".png")
	death_right = death.frames
	death_left = death.flipped_frames
	a = 0
	b = 0
	x = 0
	y = 0
	r = False
	l = False
	u = False
	d = False
	s = 0
	vs = 0

	direction = "right"

	run_game = True
	while run_game == True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run_game = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					r = True
				elif event.key == pygame.K_LEFT:
					l = True
				elif event.key == pygame.K_UP:
					u = True
				elif event.key == pygame.K_DOWN:
					d = True
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT:
					r = False
				elif event.key == pygame.K_LEFT:
					l = False
				elif event.key == pygame.K_UP:
					u = False
				elif event.key == pygame.K_DOWN:
					d = False

		moving = True
		if r == True:
			x += s
			direction = "right"
		elif l == True:
			x  -= s
			direction = "left"
		else:
			moving = False
		if u == True:
			y -= vs
		if d == True:
			y += vs

		screen.fill((200,200,200))

		a += 1
		if a % 6 == 0:
			b += 1

		if direction == "right":
			if moving == True:
				screen.blit(run_right[b % len(run_right)], (x,y))
			else:
				screen.blit(idle_right[b % len(idle_right)], (x,y))
		if direction == "left":
			if moving == True:
				screen.blit(run_left[b % len(run_left)], (x,y))
			else:
				screen.blit(idle_left[b % len(idle_left)], (x,y))

		pygame.display.update()
		clock.tick(60)

	if direction == "right":
		for frame in death_right:
			screen.fill((200,200,200))
			screen.blit(frame, (x,y))
			pygame.display.update()
			time.sleep(0.1)
	else:
		for frame in death_left:
			screen.fill((200,200,200))
			screen.blit(frame, (x,y))
			pygame.display.update()
			time.sleep(0.1)
	pygame.quit()

if __name__ == "__main__":
	run_test()