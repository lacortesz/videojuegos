import esper
from src.create.prefab_creator import create_energy_display_label, create_text
from src.ecs.components.c_charger import CCharger, CChargerState
from src.ecs.components.tags.c_tag_energy_label import CTagEnergyLabel

def system_energy_charger(world:esper.World, delta_time:float, actived:bool) -> bool: 
    components = world.get_component(CCharger)
    c_c:CCharger
        
    for entity, c_c in components:       
        on_charge = False        
        
        if c_c.state == CChargerState.NotInitialized:
            c_c.current_entity = create_text(world, c_c.full_info, c_c.full_info["text"])
            c_c.state = CChargerState.Initialized
            on_charge = False    

        if c_c.state == CChargerState.Initialized or c_c.state == CChargerState.Charged:
            if actived:
                c_c.state = CChargerState.OnCharge
                on_charge = True 
            
        if c_c.state == CChargerState.OnCharge:
            c_c.current_time -= delta_time 
            on_charge = True 
            if c_c.current_time <= 0 :
                c_c.current_time = c_c.framerate
                c_c.counter += 1  
                world.delete_entity(c_c.current_entity)
                if c_c.counter < 100: 
                    c_c.current_entity = create_text(world, c_c.on_charge_info, str(c_c.counter) + "%")                 
                else:
                    c_c.state = CChargerState.Charged
                    on_charge = False
                    c_c.current_entity = create_text(world, c_c.full_info, c_c.full_info["text"])
    
        if c_c.state == CChargerState.Charged:
            c_c.current_time = c_c.framerate
            c_c.counter = 0
                              
        return on_charge
                
def get_current_label_entity(world:esper.World) -> int:
    energy_level_component = world.get_components(CTagEnergyLabel)
    for entity in energy_level_component:
        print ("current_entity " + str(entity[0]))
    return 

