from obswebsocket import requests as obsrequests
from app.utils.logger import log

def set(obs, scene_name):
    scenes = obs.call(obsrequests.GetSceneList())
    for scene in scenes.getScenes():
        if scene["sceneName"].lower().strip() == scene_name.lower().strip():
            obs.call(
                obsrequests.SetCurrentProgramScene(sceneName=scene["sceneName"])
            )
            log.success(f"Switched to scene '{scene['sceneName']}'")
            return True
    log.warning(f"Scene '{scene_name}' not found.")
    raise ValueError(f"Scene '{scene_name}' not found.")
