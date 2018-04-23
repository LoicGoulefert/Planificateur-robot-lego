#!/usr/bin/python3

objectives_name = "abcdefghijklmnopqrstuvwxyz"


def path_to_string(path):
    """Converts the path into a string
    for the client.
    """
    res = "#4"  # ID of move list
    for action in path:  # (move, (x, cell), (y, cell))
        for a in action[1:]:
            res += a[0]
            coord = a[1].split('-')
            res += " " + coord[1] + " " + coord[2]
            res += ","
    return res[:-1]  # [:-1] to delete the last ','


def goals_to_string(goals):
    """Converts the goals into a string
    for the client.
    """
    i = 0  # index for objectives name
    res = "#1"
    for goal in goals:
        coord = goal[2].split('-')
        res += objectives_name[i] + " "
        res += coord[1] + " " + coord[2] + ","
        i += 1
    return res[:-1]  # [:-1] to delete the last ','


def robots_coord_to_string(initial_state):
    """Converts the robots coord into a string
    for the client.
    """
    res = "#3"
    for state in initial_state:
        if state[0] == 'at':
            res += state[1] + " "
            coord = state[2].split('-')
            res += coord[1] + " " + coord[2]
            res += ","
    return res[:-1]  # [:-1] to delete the last ','


def build_message(config_file,
                  obj_coord,
                  static_obj_coord,
                  robots_coord,
                  move_list):
    """Builds the message to be sent to the simulator."""
    message = []
    message.append("#c" + config_file)
    if obj_coord != "":
        message.append(obj_coord)
    if static_obj_coord != "":
        message.append(static_obj_coord)
    message.append(robots_coord)
    message.append(move_list)
    return message

if __name__ == "__main__":
    pass
