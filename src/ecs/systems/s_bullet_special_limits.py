import esper

from src.ecs.components.c_bullet_special_origin import COrigin
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet_special import CTagBulletSpecial


def system_bullet_special_limits(world:esper.World, bullet_info:dict):
    components = world.get_components(CTransform, COrigin, CTagBulletSpecial)
        
    for entity, (c_t, c_o, _) in components:
        limit = bullet_info["limit"]
        if c_t.pos.distance_to(c_o.start_pos) >= limit:
            world.delete_entity(entity)
        

