import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface

def system_animation(world:esper.World, delta_time:float):
    components = world.get_components(CSurface, CAnimation)
    
    for _, (c_s, c_a) in components:
        # 1. disminuir el valor del curr_time de la animacion
        c_a.curr_anim_time -= delta_time
        # 2. Cuando curr_time <= 0
        if c_a.curr_anim_time <= 0:
            # RESTAURAR EL TIEMPO
            c_a.curr_anim_time = c_a.animations_list[c_a.curr_anim].framerate
            # CAMBIO DE FRAME
            c_a.curr_frame += 1
            # Limitar el frame en sus propiedades Start y End
            if c_a.curr_frame > c_a.animations_list[c_a.curr_anim].end:
                c_a.curr_frame = c_a.animations_list[c_a.curr_anim].start
            # Calcular la nueva subarea del rectangulo de sprote
            rect_surf = c_s.surf.get_rect()
            c_s.area.w = rect_surf.w / c_a.number_frames
            c_s.area.x = c_s.area.w * c_a.curr_frame