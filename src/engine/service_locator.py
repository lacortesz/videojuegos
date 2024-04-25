from src.engine.services.images_services import ImagesService
from src.engine.services.sounds_service import SoundsServices
from src.engine.services.fonts_services import FontsService

class ServiceLocator:
    images_service = ImagesService()
    sounds_service = SoundsServices()
    fonts_service = FontsService()
    
    