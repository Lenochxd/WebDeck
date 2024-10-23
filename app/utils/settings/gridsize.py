from ..logger import log


def create_matrix(config):
    matrix = []
    for folder_count, (folder_name, folder_content) in enumerate(
        config["front"]["buttons"].items()
    ):
        row_count = 0
        matrix.append([])
        for count, button in enumerate(folder_content, start=1):
            if row_count >= len(matrix[folder_count]):
                matrix[folder_count].append([])
            matrix[folder_count][row_count].append(button)
            if count % int(config["front"]["width"]) == 0:
                row_count += 1
    matrix_height = len(matrix)
    matrix_width = len(matrix[0])
    return matrix


def unmatrix(config, matrix):
    for folder_count, folder in enumerate(matrix):
        folderName = list(config["front"]["buttons"])[folder_count]
        config["front"]["buttons"][folderName] = []
        for row in folder:
            for button in row:
                config["front"]["buttons"][folderName].append(button)

    return config


def update_gridsize(config, new_height, new_width):
    new_height, new_width = int(new_height), int(new_width)
    matrix = create_matrix(config)
    old_height, old_width = int(config["front"]["height"]), int(
        config["front"]["width"]
    )

    # if height has changed
    if old_height != new_height:

        # if the height has increased
        if new_height > old_height:
            difference = new_height - old_height
            for count, _ in enumerate(range(difference), start=1):
                for folder_name, folder_content in config["front"]["buttons"].items():
                    for _ in range(old_width):
                        # if count % 2 == 0:
                        #     folder_content.insert(0, {"VOID": "VOID"})
                        # else:
                        folder_content.append({"VOID": "VOID"})
            matrix = create_matrix(config)

        # if the height has decreased
        if old_height > new_height:
            difference = old_height - new_height
            log.debug("gridsize: Height decreased")
            for count, _ in enumerate(range(difference), start=1):
                for folder_count, folder in enumerate(matrix):
                    for row_count, row in enumerate(reversed(folder)):
                        if all(element == {"VOID": "VOID"} for element in row):
                            folder.pop(-row_count - 1)
                            break
                    else:
                        for col_count in range(len(folder[0])):
                            for row_count, row in enumerate(reversed(folder), start=1):
                                if folder[-row_count][col_count] == {"VOID": "VOID"}:
                                    num = row_count
                                    while num > 1:
                                        folder[-num][col_count] = folder[-num + 1][
                                            col_count
                                        ]
                                        num -= 1
                                    folder[-num][col_count] = {"DEL": "DEL"}
                                    break
                            else:
                                x = False
                                for colb_count in range(len(folder[0])):
                                    for rowb_count in range(len(folder)):
                                        if folder[rowb_count][colb_count] == {
                                            "VOID": "VOID"
                                        }:
                                            folder[rowb_count][colb_count] = folder[-1][
                                                col_count
                                            ]
                                            x = True
                                            break
                                    if x == True:
                                        break
                                if x == False:
                                    log.debug("gridsize: NOT ENOUGH SPACE")
                        folder.pop(-1)

    # if width has changed
    if old_width != new_width:

        # if the width has increased
        if new_width > old_width:

            difference = new_width - old_width
            new_matrix = matrix
            for count, _ in enumerate(range(difference), start=1):
                for folder_count, folder in enumerate(matrix):
                    for row_count, row in enumerate(folder):
                        # if count % 2 == 0:
                        #     new_matrix[folder_count][row_count].insert(0, {"VOID": "VOID"})
                        # else:
                        new_matrix[folder_count][row_count].append({"VOID": "VOID"})
            matrix = new_matrix

        if new_width < old_width:
            difference = old_width - new_width
            log.debug("gridsize: Width decreased")
            for count, _ in enumerate(range(difference), start=1):
                for folder in matrix:
                    for col_count in range(len(folder[0])):
                        if all(
                            folder[row_count][-col_count - 1] == {"VOID": "VOID"}
                            for row_count in range(len(folder))
                        ):
                            for row_count in range(len(folder)):
                                folder[row_count].pop(-col_count - 1)
                            break
                    else:
                        element_to_del = 0
                        for row in folder:
                            element_to_del += 1
                            for element_count, element in enumerate(row):
                                if element == {"VOID": "VOID"}:
                                    row.pop(element_count)
                                    element_to_del -= 1
                                    if element_to_del == 0:
                                        break
                        if element_to_del > 0:
                            for row in folder:
                                for element_count, element in enumerate(row):
                                    if element == {"VOID": "VOID"}:
                                        row.pop(element_count)
                                        element_to_del -= 1
                                        if element_to_del == 0:
                                            break
                                if element_to_del == 0:
                                    break
                        if element_to_del > 0:
                            log.debug("gridsize: NOT ENOUGH SPACE")

    config = unmatrix(config, matrix)
    log.success("Grid size updated successfully")
    log.info(f"Old grid size: {old_height}x{old_width}, New grid size: {new_height}x{new_width}")
    return config