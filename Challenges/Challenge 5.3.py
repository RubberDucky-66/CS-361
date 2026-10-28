class Stats:
    def __init__(self, str = 9, dex = 12, con = 8, int = 18, wis = 10, cha = 0):
        self.str = str  # stats
        self.dex = dex
        self.con = con
        self.int = int
        self.wis = wis
        self.cha = cha


class Armor:
    def __init__(self, name, ac):
        self.name = name
        self.ac = ac


class Weapon:
    def __init__(self, name, dice_roll):
        self.name = name
        self.dice_roll = dice_roll


class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 10
        self.stats = Stats()
        self.armor = [Armor("iron helmet", 8), Armor("chain mail", 16)]
        self.weapon = Weapon("short sword", "1d6")

    def damage(self, amount):
        self.hp -= amount

    def compute_damage(self, base):
        # Pretend this is some complex thing with AC, armor, hp
        pass

    # And more functions here to handle stats, weapons, and armor

p = Player("Alfredo")