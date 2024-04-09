import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner, Event
from src.create.prefab_creator import crear_cuadrado_enemigo

def system_enemy_spawner(world:esper.World, enemies:dict, delta_time:float):
    components = world.get_component(CEnemySpawner)

    c_esp:CEnemySpawner
            
    for _, c_esp in components:
        c_esp.ahora += delta_time
        event:Event
        for event in c_esp.events:
            if c_esp.ahora >= event.time and not event.actived:
                event.actived = True                   
                crear_cuadrado_enemigo(world, event.position, enemies[event.enemy_type])    
    
