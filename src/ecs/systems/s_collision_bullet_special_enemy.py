import esper
from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet_special import CTagBulletSpecial
from src.ecs.components.tags.c_tag_enemy import CTagEnemy



def system_collission_bullet_special_enemy(world:esper.World, explosion_info:dict):
    enemies_components = world.get_components(CSurface, CTransform, CTagEnemy)
    bullets_components = world.get_components(CSurface, CTransform, CTagBulletSpecial)
    
    for enemy_entity, (ec_s, ec_t, _) in enemies_components:
        ene_rect = CSurface.get_area_relative(ec_s.area, ec_t.pos)
        for bullet_entity, (bc_s, bc_t, _) in bullets_components:              
            bull_rect = bc_s.area.copy()
            bull_rect.topleft = bc_t.pos
            if  ene_rect.colliderect(bull_rect):
                
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)
                create_explosion(world, ene_rect, explosion_info, False)