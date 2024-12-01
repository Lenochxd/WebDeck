from obswebsocket import obsws

from app.utils.global_variables import set_global_variable
from app.utils.settings.get_config import get_config


def reload_obs():
    # Set up the OBS WebSocket client
    config = get_config()
    obs_host = config["settings"]["obs"]["host"]
    obs_port = int(config["settings"]["obs"]["port"])
    obs_password = config["settings"]["obs"]["password"]

    obs = obsws(obs_host, obs_port, obs_password)
    
    set_global_variable("obs_host", obs_host)
    set_global_variable("obs_port", obs_port)
    set_global_variable("obs_password", obs_password)

    return obs_host, obs_port, obs_password, obs