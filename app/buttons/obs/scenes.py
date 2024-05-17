from obswebsocket import requests as obsrequests

def set(obs, scene_name):
    scenes = obs.call(obsrequests.GetSceneList())
    for scene in scenes.getScenes():
        if scene["sceneName"].lower().strip() == scene_name.lower().strip():
            print(f"Switching to {scene['sceneName']}")
            obs.call(
                obsrequests.SetCurrentProgramScene(sceneName=scene["sceneName"])
            )