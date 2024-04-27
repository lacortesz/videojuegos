import asyncio
import pygame
import esper
import json

from src.create.prefab_creator import create_bullet, create_energy_charger, create_input_player, create_special_bullets, create_level, create_player_square, create_text, create_energy_display_label
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_bullet_special_limits import system_bullet_special_limits
from src.ecs.systems.s_energy_charger import system_energy_charger
from src.ecs.systems.s_collision_bullet_enemy import system_collission_bullet_enemy
from src.ecs.systems.s_collision_bullet_special_enemy import system_collission_bullet_special_enemy
from src.ecs.systems.s_collision_player_enemy import system_collission_player_enemy
from src.ecs.systems.s_explosion_kill import system_explosion_kill
from src.ecs.systems.s_hunter_state import system_hunter_state
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_player_limits import system_player_limits
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_bullet_limits import system_bullet_limits
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.engine.service_locator import ServiceLocator


class GameEngine:
    def __init__(self) -> None:
        pygame.init()
        
        #Config data in dicts
        self.window = self.read_json('window.json')
        self.level = self.read_json('level_01.json')
        self.enemies = self.read_json('enemies.json')
        self.player = self.read_json('player.json')
        self.bullets = self.read_json('bullet.json')
        self.explosion = self.read_json('explosion.json')
        self.interface = self.read_json('interface.json')
        self.bullets_special = self.read_json('bullet_special.json')
        
        self.screen = pygame.display.set_mode((self.window['size']['w'], self.window['size']['h']))
        #self.screen = pygame.display.set_mode((self.window['size']['w'], self.window['size']['h']), pygame.SCALED)
        pygame.display.set_caption(self.window['title'])
        
        self.paused = False
        self.pause_entity = 0
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window['framerate']
        self.delta_time = 0
        self.on_energy_charge = False
        self.energy_charger_activated = False
        
        self.ecs_world = esper.World()

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            await asyncio.sleep(0)
        self._clean()

    def _create(self):
        self._player_entity = create_player_square(self.ecs_world, self.player, self.level["player_spawn"])
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self._player_c_t = self.ecs_world.component_for_entity(self._player_entity, CTransform)
        self._player_c_s = self.ecs_world.component_for_entity(self._player_entity, CSurface)
        
        #self._energy_display = create_energy_display(self.ecs_world, self.interface)
        
        create_level(self.ecs_world, self.level)
        create_input_player(self.ecs_world)  
        create_text(self.ecs_world, self.interface["title"], self.interface["title"]["text"])
        create_text(self.ecs_world, self.interface["instructions"], self.interface["instructions"]["text"])
        create_text(self.ecs_world, self.interface["special_title"], self.interface["special_title"]["text"])
        
        self.energy_label = create_energy_display_label(self.ecs_world, self.interface["special_energy_full"], "100")
        
        #create_enery_special(self.ecs_world, self.interface["special_level"], self.special_level_entity)
        #self.special_level_entity =  create_text(self.ecs_world, self.interface["special_level"])
        
               
    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):     
        if not self.paused:
            system_enemy_spawner(self.ecs_world, self.enemies, self.delta_time)
            system_movement(self.ecs_world, self.delta_time)  
            system_player_state(self.ecs_world, self.player)
            system_hunter_state(self.ecs_world, self._player_entity, self.enemies["Hunter"])    
            system_screen_bounce(self.ecs_world, self.screen)
            system_player_limits(self.ecs_world, self.screen)
            system_bullet_special_limits(self.ecs_world, self.bullets_special)
            system_collission_player_enemy(self.ecs_world, self._player_entity, self.level, self.explosion, self.player)
            system_bullet_limits(self.ecs_world, self.screen)
            system_collission_bullet_enemy(self.ecs_world, self.explosion)
            system_collission_bullet_special_enemy(self.ecs_world, self.explosion)
            system_energy_charger(self.ecs_world, self.delta_time, self.energy_charger_activated)
            system_animation(self.ecs_world, self.delta_time)
            system_explosion_kill(self.ecs_world)
            self.ecs_world._clear_dead_entities()
                
    def _draw(self):
        self.screen.fill((self.window['bg_color']['r'], self.window['bg_color']['g'], self.window['bg_color']['b']))      
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()
        
    def read_json(self, file):
        f = open('assets/cfg/' + file, encoding = "utf-8")
        dictionary = json.loads(f.read())
        f.close()
        return dictionary

    def _do_action(self, c_input:CInputCommand):
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
                
        if c_input.name == "PLAYER_FIRE":
            cuad_rect = self._player_c_s.surf.get_rect(topleft=self._player_c_t.pos) 
            current_bullets = len(self.ecs_world.get_components(CTagBullet))
            max_bullets = self.level["player_spawn"]["max_bullets"]
            if current_bullets < max_bullets:
                create_bullet(self.ecs_world, self.bullets, self._player_c_t.pos, 
                              self._player_c_s.area.size, c_input.mouse_position)
                
        if c_input.name == "PLAYER_FIRE_SPECIAL":
            bullets_components = self.ecs_world.get_components(CTransform, CTagBullet)
            for bullet_entity, (bc_t, _) in bullets_components:
                if len(bullets_components) > 0:
                    create_energy_charger(self.ecs_world, self.interface["special_energy_on_charge"])
                create_special_bullets(self.ecs_world, self.bullets_special, bc_t.pos)
                self.ecs_world.delete_entity(bullet_entity)       
                               
        if c_input.name == "PAUSE":
            if c_input.phase == CommandPhase.END:
                if not self.paused: 
                    self.paused = True
                    self.pause_entity = create_text(self.ecs_world, self.interface["paused"])
                else:
                    self.paused = False
                    self.ecs_world.delete_entity(self.pause_entity)
                    self.pause_entity = 0
                    
        
            

            