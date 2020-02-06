class Magnet():
    def __init__(self,x,affect = 1000):
        self.__xpos = x
        self.__affect = affect
    def get_pos(self):
        return self.__xpos
    def get_affect(self):
        return self.__affect