class BasePage:
    def __init__(self):
        self.ui = None
        self.setup_up()

    def show(self):
        self.ui.show()

    def setup_up(self):
        pass
