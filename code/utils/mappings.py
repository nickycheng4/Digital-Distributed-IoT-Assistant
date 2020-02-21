from .synonym_acronym import handle_syn_acr

command_device = {
    "TV": ["set", "change", "turn"],
    "AC": ["set"],
    "light": ["turn"],
    "tank": ["fill"],
    "door": ["open", "close"],
    "drone": ["take off", "land", "set"],
    "speaker":['turn'],
    "camera":[]
}

parameter_device = {
    "TV": ["channel", "volume", "brightness"],
    "AC": ["temperature"],
    "drone": ["speed", "altitude"],
    "speaker": ['sound'],
    'light':[],
    'tank':[],
    'door':[],
    'camera':[]
}

trigger_device = {
    "TV": [],
    "AC": [''],
    "drone": [],
    "speaker": ['sound'],
    'light':['brightness'],
    'tank':[],
    'door':[],
    'camera':['see']
}


def final_device(command):
    i = 1
    temp = command[i]
    if command[i] not in parameter_device:
        for item in parameter_device.keys():
            if command[i] in parameter_device[item]:
                
                command[i] = item
                return command,temp

        if command[i] not in command_device.keys():

            syn, acr = handle_syn_acr(command[i])
            if syn:
                for item in syn:
                    if item in command_device.keys():
                        command[i] = item
                        return command,temp
            elif acr:
                if acr[0] in command_device.keys():
                    command[i] = acr[0]
                    return command,temp
    return command,temp


def final_action(command):
    i = 0
    if command[1] not in command_device.keys():
        return command

    if command[i] not in command_device[command[1]]:
        syn, acr = handle_syn_acr(command[i])
        if syn:
            for item in syn:
                if item in command_device[command[1]]:
                    command[0] = item
                    return command
        elif acr:
            if acr[0] in command_device[command[1]]:
                command[0] = item
                return command
    return command

def trigger_condition(command):
    result_device = None
    result_target = None
    redun = ['is','the','really']
    if command[-1] != 'No condition':

        words = command[-1].split()
        for i in range(len(words)):
            for device in trigger_device:
                if words[i] in trigger_device[device] or words[i] == device:
                    result_device = device.capitalize()
                    result_target = ' '.join([item for item in words[i+1:] if item not in redun]).capitalize()

    return result_device, result_target

def gen_order(command,temp):
    total = {'Condition related':[],'Action related': []}
    result_device, result_target = trigger_condition(command)
    if not result_device:
        total['Condition related'] = ['No condition']
    else:
        total['Condition related'] = [result_device, result_target]
    total['Action related'] = [command[1].capitalize()]
    if command[1] != temp:
        total['Action related'].append(temp.capitalize())
    if command[2] != 'No parameter':
        total['Action related'] += [command[2].capitalize()]
    string_mode = total['Condition related'] + total['Action related']
    #print(total,string_mode)
    arrow_order = ' ==> '.join(string_mode)
    return total,arrow_order




