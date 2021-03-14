import yaml


def yml_data_with_filename_and_key(file_name, key):
    with open("./data/" + file_name + ".yaml", "r") as f:
        data = yaml.load(f)[key]
        case_data_list = list()
        for case_data in data.values():
            case_data_list.append(case_data)
        return case_data_list
