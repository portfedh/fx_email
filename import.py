import base

class new():
    def __init__(self):
        print('new class created')

    def color(self):
        self.color = 'blue'
        print(self.color)

    def odor(self):
        self.odor = base.first()
        self.odor.smell()

if __name__ == '__main__':
    object = new()
    object.color()
    object.odor()

