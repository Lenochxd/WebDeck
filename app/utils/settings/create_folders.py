def create_folders(config, folders_to_create):
    for folder in folders_to_create:

        config["front"]["buttons"][folder["name"]] = [
            {
                "image": "back10.svg",
                "image_size": "110%",
                "message": f"/folder {folder['parent_folder']}",
                "name": f"back to {folder['parent_folder']}",
            }
        ]

        void_count = int(config["front"]["width"]) * int(config["front"]["height"])
        for _ in range(void_count - 1):
            config["front"]["buttons"][folder["name"]].append({"VOID": "VOID"})

        print("NEW FOLDER :", folder["name"])
    folders_to_create = []
    return config