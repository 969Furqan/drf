import time
import logging
logger = logging.getLogger(__name__)

class RequestTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        start_time = time.time()
        
        respone = self.get_response(request)
        
        delay_time = time.time() - start_time
        
        logger.info(f"request to {request.path}, took {delay_time:.2f} seconds")
        return respone
        