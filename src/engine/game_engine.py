import pygame
import esper
import json

from src.create.prefab_creator import create_input_player, create_square, create_level, create_player_square
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_input_command import CInputCommand, CommandPhase


class GameEngine:
    def __init__(self) -> None:
        pygame.init()
        
        #Config data in dicts
        self.window = self.read_json('window.json')
        self.level = self.read_json('level_01.json')
        self.enemies = self.read_json('enemies.json')
        self.player = self.read_json('player.json')
        
        self.screen = pygame.display.set_mode((self.window['size']['w'], self.window['size']['h']))
        #self.screen = pygame.display.set_mode((self.window['size']['w'], self.window['size']['h']), pygame.SCALED)
        pygame.display.set_caption(self.window['title'])
        
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window['framerate']
        self.delta_time = 0
        
        self.ecs_world = esper.World()

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        self._player_entity = create_player_square(self.ecs_world, self.player, self.level["player_spawn"])
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        create_level(self.ecs_world, self.level)
        create_input_player(self.ecs_world)
               
    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_enemy_spawner(self.ecs_world, self.enemies, self.delta_time)
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)
        
    def _draw(self):
        self.screen.fill((self.window['bg_color']['r'], self.window['bg_color']['g'], self.window['bg_color']['b']))      
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        pygame.quit()
        
    def read_json(self, file):
        f = open('assets/cfg/' + file, encoding = "utf-8")
        dictionary = json.loads(f.read())
        f.close()
        return dictionary

    def _do_action(self, c_input:CInputCommand):
        print(c_input.name + " " + str(c_input.phase))
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.x -= self.player["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.x += self.player["input_velocity"]
        
        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.x += self.player["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.x -= self.player["input_velocity"]
            
        if c_input.name == "PLAYER_UP":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.y -= self.player["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.y += self.player["input_velocity"]
                
        if c_input.name == "PLAYER_DOWN":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.y += self.player["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.y -= self.player["input_velocity"]