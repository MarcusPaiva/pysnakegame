from light_game_engine.inputs.game_input import Joystick
from light_game_engine.scene.SplashScreen import SplashScreen
from light_game_engine.scene.game_management import GameManagement, SceneManagement
from light_game_engine.screen import SurfaceScreen

from game_src.screens.game_stage import Stage
from game_src.screens.main_menu import MainMenu

screen = SurfaceScreen(1100, 720, "PySnake Game")
joystick = Joystick(0)

# Splash screen
splash = SplashScreen(
    screen,
    r'game_src/assets/images/logo/my_logo.png',
    r'./game_src/assets/sounds/effects/intro.mp3',
)
splash.setup()
splash.loop()

# Scenes
SceneManagement().add_scene("main_menu", MainMenu(screen, joystick))
SceneManagement().add_scene("game_stage", Stage(screen, joystick))

# Game Management
game_management = GameManagement(screen)
game_management.setup()
game_management.loop()
