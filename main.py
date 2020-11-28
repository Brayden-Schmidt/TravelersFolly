# Open Git Bash
# cd  ~/Documents/VSCODE/MIDPROCESS/TravelersFolly
# git add .
# git commit -m "<your message here>"
# git push origin develop

# Path: C:\Users\blsfu\Documents\VSCODE\MIDPROCESS\TravelersFolly
# Unicode guide: http://www.fileformat.info/info/charset/UTF-8/list.htm
# Start file -> Display start menu -> Select option (play) -> Prompt for seed -> Generate map -> Process player input -> Move/Interact  # noqa:E501
# Dependencies:
# * Inventory
# * Health
# * Buildings
# * Natural structures
# * Stamina
# * Random events
# * Fights (Turn-Based)
# * Items
# * Quests
# * NPC's
# * Bartering
import sys
import json
import msvcrt
import random
from string import Template
from os import system, name
from enum import Enum


def clear():
    if name == 'nt':
        _ = system('cls')


def cycle_list(lst, down=False):
    return_lst = list(lst)
    lst.extend(lst)
    if down:
        for i in range(len(return_lst)):
            return_lst[i] = lst[i + 1]
    else:
        for i in range(len(return_lst)):
            return_lst[i] = lst[-len(return_lst)-1+i]

    return return_lst


def init_db():
    db = {
        "menus": {
            "title_screen": "_____________________________________________________  \n|  #########################            _.._  __     | \n|   Welcome to the Text RPG         .--{    }/  \"~-._| \n|  #########################       /    ^++^/      / | \n|        ${o3} - Play -               {        (0     /  | \n|                                  \\=.___ .//\\___+\"  | \n|                                  \\   .//'     /    | \n|        ${o2} - Help -                )  _//'    _(     | \n|                                  (HHHHH[]HHHH)     | \n|                                  / \\   ..  / \\     | \n|        ${o1} - Quit -              /   }  .. {    \\    | \n|                                 ^+._/\\ .. /\\_.+^   | \n|        copyright 2020                 \\__/         | \n|____________________________________________________| \n",  # noqa: E501
            "help": "############################               \n#       -HELP -          #\n############################               \n                                           \nUse w, a, s d to move\n           \nType e to selct or q to go back\n                \nUse \"`\"\n to enter debug mode                   \nAnd most importantly be careful out there\n\npress \"q\" to go back ---->\n",  # noqa: E501
            "seed_prompt": "If you have a seed, enter it now, otherwise press enter:"  # noqa: E501
        },
        "player": {
            "health": 100,
            "stamina": 100,
            "inventory": []
        },
        "templates": {
            "mountain": "",
            "river": "",
            "town": ""
        }
    }

    jso = JSONOps('db.json')
    jso.write(db)


class SceneStates(Enum):
    title = 0
    help_screen = 1
    game = 2
    seed_prompt = 3


class StructuresEnum(Enum):
    mountain = 0
    river = 1
    town = 2


class World:
    scene_state = SceneStates.title

    def __init__(self, world_size, window_size, window_pos, debug=False):
        init_db()
        self.jso = JSONOps('db.json')
        self.selection_list = [' ', ' ', '>']
        self.world_size = world_size
        self.window_size = window_size
        self.window_pos = window_pos
        self.entities = []
        self.entity_index = 0
        self.entity_display_map = {'-1': '\u02e3'}
        self.debug = debug

    def derive_view(self, db):
        if self.scene_state == SceneStates.title:
            t = Template(db['menus']['title_screen'])
            s = t.substitute(o1=self.selection_list[0], o2=self.selection_list[1], o3=self.selection_list[2])  # noqa:E501

            return s
        elif self.scene_state == SceneStates.help_screen:
            return db['menus']['help']
        elif self.scene_state == SceneStates.seed_prompt:
            return db['menus']['seed_prompt']
        elif self.scene_state == SceneStates.game:
            world_matrix = self.generate_world_matrix()
            world_display = self.generate_world_display(world_matrix)

            return world_display
        elif self.scene_state == SceneStates.inventory:
            inventory_matrix = self.generate_inventory_matrix()
            inventory_display = self.generate_inventory_display(inventory_matrix)  # noqa:E501

            return inventory_display

    def process_input(self):
        option = ''
        if self.scene_state == SceneStates.seed_prompt:
            option = input().strip().lower()
        else:
            option = msvcrt.getwch()
        print(option)
        if option == '\\':
            exit(0)

        if self.scene_state == SceneStates.title:
            # Process menu navigation
            if option == 's':
                self.selection_list = cycle_list(self.selection_list, down=True)  # noqa:E501
            elif option == 'w':
                self.selection_list = cycle_list(self.selection_list)
            elif option == 'e':
                if self.selection_list.index('>') == 2:
                    self.scene_state = SceneStates.seed_prompt
                elif self.selection_list.index('>') == 1:
                    self.scene_state = SceneStates.help_screen
                elif self.selection_list.index('>') == 0:
                    exit(0)
        elif self.scene_state == SceneStates.seed_prompt:
            generated_seed = random.randrange(sys.maxsize)
            if option != '':
                random.seed(int(option))
                generated_seed = option
            else:
                random.seed(generated_seed)
            self.seed = generated_seed
            self.add_player()

            for i in range(50):
                self.add_random_enemy()
            for i in range(50):
                self.add_random_mountain()
            self.scene_state = SceneStates.game
        elif self.scene_state == SceneStates.help_screen:
            if option == 'q':
                self.scene_state = SceneStates.title
        elif self.scene_state == SceneStates.game:
            # Process player movement
            if option == 'w':
                for entity in self.entities:
                    if entity.get_name() == 'player':
                        entity.set_position(y_pos=1)
                        if self.detect_world_bounds_collision(entity):
                            entity.set_position(y_pos=-1)
            elif option == 's':
                for entity in self.entities:
                    if entity.get_name() == 'player':
                        entity.set_position(y_pos=-1)
                        if self.detect_world_bounds_collision(entity):
                            entity.set_position(y_pos=1)
            elif option == 'a':
                for entity in self.entities:
                    if entity.get_name() == 'player':
                        entity.set_position(x_pos=-1)
                        if self.detect_world_bounds_collision(entity):
                            entity.set_position(x_pos=1)
            elif option == 'd':
                for entity in self.entities:
                    if entity.get_name() == 'player':
                        entity.set_position(x_pos=1)
                        if self.detect_world_bounds_collision(entity):
                            entity.set_position(x_pos=-1)
            elif option == '`':
                self.debug = not self.debug

    def add_player(self):
        player = Player([0, 0], 100, 100, self.entity_index)
        self.entity_display_map[str(self.entity_index)] = player.get_display_char()  # noqa:E501
        self.entities.append(player)  # noqa:E501
        self.entity_index += 1

    def add_random_enemy(self):
        random_pos = [random.randint(0, self.world_size[1] - 1), random.randint(0, self.world_size[0] - 1)]  # noqa:E501
        enemy = Enemy(f'enemy_{self.entity_index}', 20, 2, random_pos, '\u029b', self.entity_index)  # noqa:E501
        self.entity_display_map[str(self.entity_index)] = enemy.get_display_char()  # noqa:E501
        self.entities.append(enemy)  # noqa:E501
        self.entity_index += 1

    def add_random_mountain(self):
        random_pos = [random.randint(0, self.world_size[1] - 1), random.randint(0, self.world_size[0] - 1)]  # noqa:E501
        mountain = Structure(f'mountain_{self.entity_index}', '', StructuresEnum.mountain, random_pos, '\u005e', self.entity_index)  # noqa:E501
        self.entity_display_map[str(self.entity_index)] = mountain.get_display_char()  # noqa:E501
        self.entities.append(mountain)  # noqa:E501
        self.entity_index += 1

    def detect_world_bounds_collision(self, entity):
        if entity.get_position()[0] > self.world_size[1] - 1:
            return True
        elif entity.get_position()[0] < 0:
            return True
        elif entity.get_position()[1] > self.world_size[0] - 1:
            return True
        elif entity.get_position()[1] < 0:
            return True

        return False

    def detect_window_change(self, entity, x_pos=0, y_pos=0):
        if entity.get_position()[0] >= self.window_pos[0] + self.window_size[0]:  # noqa:E501
            self.window_pos[0] += self.window_size[0]
        elif entity.get_position()[0] < self.window_pos[0]:  # noqa:E501
            self.window_pos[0] -= self.window_size[0]
        if entity.get_position()[1] >= self.window_pos[1] + self.window_size[1]:  # noqa:E501
            self.window_pos[1] += self.window_size[1]
        elif entity.get_position()[1] < self.window_pos[1]:  # noqa:E501
            self.window_pos[1] -= self.window_size[1]

    def generate_world_matrix(self):
        world_matrix = [[-1 for x in range(self.world_size[0])] for y in range(self.world_size[1])]  # noqa:E501

        for entity in self.entities:
            world_matrix[entity.get_position()[1]][entity.get_position()[0]] = entity.get_matrix_index()  # noqa:E501

        return world_matrix

    def generate_world_display(self, world_matrix):
        world_display = ''.join([' # ' for x in range(self.window_size[0] + 2)]) + '\n'  # noqa:E501

        for y in range(len(world_matrix)):
            if y >= self.window_pos[1] and y < self.window_pos[1] + self.window_size[1]:  # noqa:E501
                world_display += ' | '
                for x in range(len(world_matrix[y])):
                    if x >= self.window_pos[0] and x < self.window_pos[0] + self.window_size[0]:  # noqa:E501
                        world_display += f' {self.entity_display_map[str(world_matrix[y][x])]} '  # noqa:E501
                world_display += ' | \n'
        world_display += ''.join([' # ' for x in range(self.window_size[0] + 2)])  # noqa:E501
        return world_display

    def get_player(self):
        for entity in self.entities:
            if entity.get_name() == 'player':
                return entity
        return None

    def start(self):
        pass

    def render(self):
        self.start()

        while True:
            clear()

            # Read db at start of frame
            db = self.jso.read()

            player = self.get_player()
            if player:
                if self.debug:
                    print('#-DEBUG MODE-#')
                    print(player.get_position())
                    print(self.seed)
                self.detect_window_change(player)

            # Get view based on scene state
            view = self.derive_view(db)
            print(view)

            # Process user keyboard input
            self.process_input()

            # Write changes to db at end of frame
            self.jso.write(db)


class Entity:
    def __init__(self, name, display_char, position, matrix_index):
        self.name = name
        self.display_char = display_char
        self.position = position
        self.matrix_index = matrix_index

    def get_name(self):
        return self.name

    def get_display_char(self):
        return self.display_char

    def get_matrix_index(self):
        return self.matrix_index

    def get_position(self):
        return self.position

    def set_position(self, x_pos=0, y_pos=0):
        if self.position[0] + x_pos >= 0:
            self.position[0] = self.position[0] + x_pos
        if self.position[1] - y_pos >= 0:
            self.position[1] = self.position[1] - y_pos


class Item:
    pass


class Player(Entity):
    def __init__(self, position, health, stamina, matrix_index):
        Entity.__init__(self, 'player', '\u024e', position, matrix_index)
        self.jso = JSONOps('db.json')
        db = self.jso.read()
        db['player']['health'] = health
        db['player']['stamina'] = stamina
        self.jso.write(db)

    def take_damage(self, amount):
        db = self.jso.read()
        db['player']['health'] -= amount
        self.jso.write(db)

    def decrease_stamina(self, amount):
        db = self.jso.read()
        db['player']['stamina'] -= amount
        self.jso.write(db)

    def add_item(self, item: Item):
        db = self.jso.read()
        db['player']['inventory'].append(item)
        self.jso.write(db)

    def drop_item(self, item: Item):
        db = self.jso.read()
        db['player']['inventory'].pop(item)
        self.jso.write(db)


class JSONOps:
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path, "r") as fp:
            data = json.load(fp)
            return data

    def write(self, dump):
        with open(self.path, "w") as fp:
            json.dump(dump, fp, indent=4)


class NPC(Entity):
    pass


class Enemy(Entity):
    def __init__(self, name, health, strength, position, display_char, matrix_index):  # noqa: E501
        Entity.__init__(self, name, display_char, position, matrix_index)  # <<< IMPORTANT # noqa: E501
        self.jso = JSONOps('db.json')
        db = self.jso.read()
        db[name] = {}
        db[name]['health'] = health
        db[name]['strength'] = strength
        self.jso.write(db)

    def take_damage(self, amount):
        db = self.jso.read()
        db[self.name]['health'] -= amount
        self.jso.write(db)


class Structure(Entity):
    def __init__(self, name, description, structure_type, position, display_char, matrix_index):  # noqa: E501
        Entity.__init__(self, name, display_char, position, matrix_index)  # <<< IMPORTANT # noqa: E501
        self.jso = JSONOps('db.json')
        db = self.jso.read()
        if structure_type == StructuresEnum.mountain:
            db[name] = db['templates']['mountain']
        if structure_type == StructuresEnum.river:
            db[name] = db['templates']['river']
        if structure_type == StructuresEnum.town:
            db[name] = db['templates']['town']
        self.jso.write(db)


world = World(world_size=[50, 50], window_size=[10, 10], window_pos=[0, 0], debug=False)  # noqa: E501
# world_matrix = world.generate_world_matrix()
# for row in world_matrix:
#     print(row)
world.render()
