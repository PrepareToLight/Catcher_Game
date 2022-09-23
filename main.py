from objects import *

class App:
    def __init__(self, width: int = 900, height: int = 600) -> None:
        pg.init()
        App.width = width
        App.height = height
        App.running = True
        flags = pg.RESIZABLE
        App.screen = pg.display.set_mode((width, height), flags)
        App.clock = pg.time.Clock()
        App.screen.get_width()
        App.screen.get_height()

        #initialize in game objects
        App.Hero = Hero(App.screen)
        App.Net = Net(App.screen)
        App.Squares = []
        for i in range(10):
            App.Squares.append(Squares(App.screen))


    def run(self):
        while App.running:
            App.clock.tick(FPS)
            for event in pg.event.get():
                #print(event)
                if event.type == pg.QUIT:
                    App.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        App.running = False
                if event.type == pg.MOUSEMOTION:
                    App.Hero.move(event.pos)
                    App.Net.move(event.pos)
                    
            keys_pressed = pg.key.get_pressed()

            App.screen.fill((0,0,0))
            App.Net.catch_directory(keys_pressed)
    
            for i, obj in enumerate(App.Squares):
                obj.move(i)
                obj.show()
                App.Net.net_catch(i,obj,App.Squares)

            App.Hero.show()
            App.Net.show()
            pg.display.flip()

        pg.quit()

if __name__ == "__main__":
    App(width, height).run()