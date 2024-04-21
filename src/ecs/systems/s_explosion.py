import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tags.c_tag_explosion import CTagExplosion

def system_explosion(world: esper.World):
    components = world.get_components(CAnimation, CTagExplosion)
    for explosion_entity, (anim, _) in components:
        if anim.curr_frame == anim.animations_list[anim.curr_anim].end:
            world.delete_entity(explosion_entity)