import traceback


def add_values_to_json(json_file, values):
    for value in values:
        try:
            json_file[value].extend(values)
        except Exception as e:
            print("%s not listed in JSON file." % e)
            json_file.update({value: values})
    return json_file


def rm_header_dups_json(json_file):
    for a in json_file.keys():
        idx = 0
        for i in json_file[a]:
            if a == i:
                del json_file[a][idx]
                idx -= 1
            idx += 1
    return json_file
