class Color:
	white = (255,255,255)
	black = (0,0,0)
	red = (255,0,0)
	green = (0,255,0)
	blue = (0,0,255)
	gray = (120,120,120)
	light_blue = (0,100,255)

	dark_gray = (60,60,60)


def run_test():

	import pygame
	screen = pygame.display.set_mode((500, 500))
	testing_color = (120,120,120)
	run_game = True

	while run_game == True:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run_game = False

		screen.fill(testing_color)

		pygame.display.update()
	pygame.quit()

if __name__ == "__main__":
	run_test()