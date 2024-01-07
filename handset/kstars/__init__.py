from handset import Handset


class KStars(Handset):
    def __init__(self):
        super().__init__('./handset/kstars', ['up', 'down', 'left', 'right'])