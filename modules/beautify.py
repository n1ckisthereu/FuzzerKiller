from email import message


def render():
    return """
______                      _   ___ _ _           
|  ___|                    | | / (_) | |          
| |_ _   _ ___________ _ __| |/ / _| | | ___ _ __ 
|  _| | | |_  /_  / _ \ '__|    \| | | |/ _ \ '__|
| | | |_| |/ / / /  __/ |  | |\  \ | | |  __/ |   
\_|  \__,_/___/___\___|_|  \_| \_/_|_|_|\___|_|   
                                                  
"""

def formatError(
    status_code,
    message
):
    return {
        "status": status_code,
        "message": message
    }

def returnMessage(
    status_code,
    message
):
    return {
        "status": status_code,
        "message": message
    }
