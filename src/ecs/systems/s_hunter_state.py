import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_state import CHunterState, HunterState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_hunter import CTagHunter

def system_hunter_state(world:esper.World, player_entity:int):
    components = world.get_components(CTransform, CAnimation, CHunterState)
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)
    pl_rect = CSurface.get_area_relative(pl_s.area, pl_t.pos)
    
    for _, (c_t, c_a, c_hst) in components:
        if c_hst.state == HunterState.IDLE:
            _do_idle_state(c_t, c_a, c_hst, pl_t)
        elif c_hst.state == HunterState.MOVE:
            _do_move_state(c_t, c_a, c_hst, pl_t)

def _do_idle_state(c_t:CTransform, c_a:CAnimation, c_pst:CHunterState, pl_t:CTransform):
    _set_animation(c_a, 1)
    if (c_t.pos - pl_t.pos).magnitude() < 100:
        c_pst.state = HunterState.MOVE
        
def _do_move_state(c_t:CTransform, c_a:CAnimation, c_pst:CHunterState, pl_t:CTransform):
    _set_animation(c_a, 0)
    if (c_t.pos - pl_t.pos).magnitude() > 200:
        c_pst.state = HunterState.IDLE

def _set_animation(c_a:CAnimation, num_amim:int):
    if c_a.curr_anim == num_amim:
        return
    c_a.curr_anim = num_amim
    c_a.curr_anim_time = 0
    c_a.curr_frame = c_a.curr_frame = c_a.animations_list[c_a.curr_anim].start
    
    