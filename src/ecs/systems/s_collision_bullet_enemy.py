import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_bullet import CTagBullet


def system_collission_bullet_enemy(world:esper.World):
    enemies_components = world.get_components(CSurface, CTransform, CTagEnemy)
    bullets_components = world.get_components(CSurface, CTransform, CTagBullet)
    
    for enemy_entity, (ec_s, ec_t, _) in enemies_components:
        ene_rect = ec_s.surf.get_rect(topleft = ec_t.pos)
        for bullet_entity, (bc_s, bc_t, _) in bullets_components:              
            bullet_rect = bc_s.surf.get_rect(topleft = bc_t.pos)
            if  ene_rect.colliderect(bullet_rect):
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)