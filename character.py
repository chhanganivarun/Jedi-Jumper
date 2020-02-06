import colorama
class Character:
    def __init__(self,name,lives = None):
        self.name = name
        if lives == None or type(lives) is not int:
            self._lives = 3
        else:
            self._lives = lives
        self._lives_left = self._lives
        self._vel = 0
        self._xpos = 0 # from bottom left OF THE GROUND
        self._ypos = 0 # from bottom left OF THE GROUND

    def greet(self):
        print(colorama.Fore.RED)
        print('Who called the {lives} lives holder {name}'.format(name=self.name,lives=self._lives))
        print(colorama.Style.RESET_ALL)
    def get_lives(self):
        return self._lives_left
