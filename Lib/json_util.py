import traceback


def ents_to_list(json_ents_file, values):
    a = []
    for value in values:
        i = value.split(" - ")
        k = []
        for j in i:
            j.replace(" ", "_")
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
        value = value.split(" - ")

        item = value[0]
        label = value[1]
        try:
            print("!!!!!HEREHEREHERE!!!!\n%s" % item)
            json_ents_file[label].extend([item])
        except Exception as e:
            print("%s \nNot listed in JSON file." % e)
            json_ents_file.update({label: [item]})

    return json_ents_file


def rm_list_dups_json(json_ents_list):
    # to remove duplicated
    # from list
    for i in json_ents_list:
        res = []
        for items in json_ents_list[i]:
            if items not in res:
                res.append(items)
                res.sort()

        json_ents_list.update({i: res})

    return json_ents_list


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
