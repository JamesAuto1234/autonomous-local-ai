import time
import requests
from loguru import logger

def wait_for_health(port: int, timeout: int = 300) -> bool:
    """
    Wait for the service to become healthy with optimized retry logic.
    """
    health_check_url = f"http://localhost:{port}/health"
    start_time = time.time()
    wait_time = 0.5  # Start with shorter wait time for faster startup detection
    last_error = None
    
    logger.info(f"Waiting for service health at {health_check_url} (timeout: {timeout}s)")
    
    while time.time() - start_time < timeout:
        try:
            # Use shorter timeout for faster failure detection
            response = requests.get(health_check_url, timeout=3)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if response_data.get("status") == "ok":
                        elapsed = time.time() - start_time
                        logger.info(f"Service healthy at {health_check_url} (took {elapsed:.1f}s)")
                        return True
                except ValueError:
                    # If JSON parsing fails, just check status code
                    pass
                    
        except requests.exceptions.ConnectionError:
            last_error = "Connection refused"
        except requests.exceptions.Timeout:
            last_error = "Request timeout"
        except requests.exceptions.RequestException as e:
            last_error = str(e)[:100]
        
        # Log progress every 30 seconds to avoid spam
        elapsed = time.time() - start_time
        if elapsed > 0 and int(elapsed) % 30 == 0:
            logger.debug(f"Still waiting for health check... ({elapsed:.0f}s elapsed, last error: {last_error})")
        
        time.sleep(wait_time)
        # Exponential backoff with cap at 10 seconds
        wait_time = min(wait_time * 1.5, 10)
    
    logger.error(f"Health check failed after {timeout}s. Last error: {last_error}")
    return False