#!/usr/bin/python3

objectives_name = "abcdefghijklmnopqrstuvwxyz"
CHUNK_SIZE = 4096  # Maximum message size the server can receive


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
    """Converts the robots coord into a string for the client."""
    res = "#3"
    for state in initial_state:
        if state[0] == 'at':
            res += state[1] + " "
            coord = state[2].split('-')
            res += coord[1] + " " + coord[2]
            res += ","
    return res[:-1]  # [:-1] to delete the last ','


# ça va dégager ça, on va envoyer un objet pickled en fait
def path_to_string(path, robot_list, nb_cells, width):
    """Converts the path of bitstring into a string for the client."""
    res = "#4"  # ID of move list
    for action in path:  # bitvector
        header = action[2][:nb_cells * len(robot_list)]
        for i in range(len(robot_list)):
            res += robot_list[i] + " "
            # Get the coords of 1 robot in the header
            sub_header = header[i*nb_cells:(i+1)*nb_cells]
            index = 0
            for j in sub_header:
                if j == 1:
                    break
                index += 1
            # Transform index into 2D coords
            c_x, c_y = int(index / width), index % width
            res += str(c_x) + " " + str(c_y) + ","
    return res[:-1]  # [:-1] to delete the last ','


def split_into_chunks(message):
    """Splits a string bigger than CHUNK_SIZE
    into smaller chunks of CHUNK_SIZE length maximum.
    """
    packet_id = message[:2]
    res = []
    buf = packet_id
    instrs = message[2:].split(',')
    for instr in instrs:
        if len(buf + instr + ",") < CHUNK_SIZE:
            buf += instr + ","
        else:
            res.append(buf[:-1])
            buf = packet_id
    return res


def build_message(obj_coord,
                  static_obj_coord,
                  robots_coord,
                  move_list):
    """Builds the message to be sent to the simulator."""
    message = []
    if obj_coord != "":
        message.append(obj_coord)
    if static_obj_coord != "":
        message.append(static_obj_coord)
    message.append(robots_coord)
    if len(move_list) > CHUNK_SIZE:
        move_list_tab = split_into_chunks(move_list)
        for ml in move_list_tab:
            message.append(ml)
    else:
        message.append(move_list)
    return message

if __name__ == "__main__":
    pass
