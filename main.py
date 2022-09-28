def run_game():
	import pygame
	from screen import Screen
	from player import Player, PlayerNoAcceleration
	from game import Game
	from map import Object, TileMap
	from spritesheet import Spritesheet
	from camera import Camera
	from color import Color
	import time 

	pygame.init()

	screen = Screen()

	current_map = TileMap(Spritesheet("./assets/PixelFantasy_Caves_1.0/mainlev_build.png", 64, 64, scale = 2),
		"./assets/Test_map_1/delete_this_behind_player.csv",
		"./assets/Test_map_1/delete_this_before_player.csv",
		"./assets/Test_map_1/delete_this_hitbox.csv",
		1016, 1341)
	current_map.add_BG_images(["./assets/PixelFantasy_Caves_1.0/background1.png",
		"./assets/PixelFantasy_Caves_1.0/background2.png",
		"./assets/PixelFantasy_Caves_1.0/background3.png",
		"./assets/PixelFantasy_Caves_1.0/background4a.png"
		],
		[12, 10, 8, 6],
		screen)

	player = Player(current_map.player_x_starting_position, current_map.player_y_starting_position)

	game = Game()

	camera = Camera(player = player)
	camera.define_borders(0, current_map.height, 0, current_map.width)

	while not game.game_over:

		game.update_key_states()

		player.get_inputs(game)
		player.update_state(current_map.BG_objects)

		player.update_speed(current_map.BG_objects)
		player.move(current_map)
		player.jump()
		player.recharge_jumps()
		player.update_speed_after_colision()

		player.determinate_current_animation()
		player.change_size(current_map.BG_objects)
		
		camera.scroll(screen, player)
		screen.update_screen(current_map, player, camera)
		pygame.display.update()
		print(player.x, player.y)

	pygame.quit()

if __name__ == "__main__":
	run_game()