import traceback


def add_values_to_json(json_file, values):
    a = []
    for value in values:
        i = value.split(" - ")
        k = []
        for j in i:
            j.replace(" ", "-")
            k.append(j)
            value = " - ".join(k)
        a.append(value)

    # to remove duplicated
    # from list
    res = []
    for i in a:
        if i not in res:
            res.append(i)

    for value in res:
        try:
            json_file[value].extend(res)
        except Exception as e:
            print("%s not listed in JSON file." % e)
            json_file.update({value: res})

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
