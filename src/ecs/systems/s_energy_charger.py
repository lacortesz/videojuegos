import esper
from src.create.prefab_creator import create_energy_display_label, create_text
from src.ecs.components.c_charger import CCharger, CChargerState
from src.ecs.components.tags.c_tag_energy_label import CTagEnergyLabel

def system_energy_charger(world:esper.World, delta_time:float, actived:bool) -> bool: 
    components = world.get_component(CCharger)
    c_c:CCharger
        
    for entity, c_c in components:       
        #print(" current_time: " + str(c_c.current_time) + " delta_time " + str(delta_time))
        on_charge = False        
        
        if c_c.state == CChargerState.NotInitialized:
            c_c.current_entity = get_current_label_entity(world)
            #c_c.current_entity = create_text(world, c_c.info, "100%")
            c_c.state = CChargerState.OnCharge
            
        #if c_c.state == CChargerState.NotInitialized and actived:
        #    c_c.state == CChargerState.OnCharge
            
        if c_c.state == CChargerState.OnCharge:
            c_c.current_time -= delta_time 
            if c_c.current_time <= 0 :
                c_c.current_time = c_c.framerate
                c_c.counter += 1  
                if c_c.counter <= 100:
                    world.delete_entity(c_c.current_entity)
                    c_c.current_entity = create_text(world, c_c.info, str(c_c.counter) + "%")
                        #world.delete_entity(current_entity) 
                else:
                    c_c.current_time = c_c.framerate
                    c_c.counter = 0
                    c_c.state = CChargerState.Charged
                           
                        #world.delete_entity(entity)
                   # print(" Aumento Contador: " + str(c_c.counter))        

        if c_c.state == CChargerState.Charged:
            create_energy_display_label(world, c_c.info, "100%")
            world.delete_entity(entity) 
                
        return on_charge
                
def get_current_label_entity(world:esper.World) -> int:
    energy_level_component = world.get_component(CTagEnergyLabel)
    print ("current_entity " + str(energy_level_component[0][0]))
    return energy_level_component[0][0]
                
                
                
                
                
                
                
                
    '''if c_c.counter > 1:
        world.delete_entity(c_c.current_entity)
    if c_c.counter <= 100:
        c_c.current_entity = create_text(world, text_info["especial_porcentage"], str(c_c.counter) + "%")
    else:
        c_c.counter = 0    
        c_c.current_time = c_c.framerate
        world.delete_entity(entity)'''
        
