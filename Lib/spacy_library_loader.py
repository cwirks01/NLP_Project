import json
import os


def load_lib(repoDir=None):
    '''
    input a path to the repository/library directory
    :param repoDir:
    :return: json library
    '''
    repo_dir = repoDir
    if repo_dir is not None:
        try:
            repo_file_list = os.listdir(repo_dir)
            if not repo_file_list in [[], [''], '', None]:
                for repo_file in repo_file_list:
                    if repo_file.startswith("data"):
                        with open(os.path.join(repo_dir, repo_file), 'r+') as json_file:
                            return json.load(json_file)
            else:
                # Use default library
                default_path = os.path.join(os.getcwd(), "repo")
                repo_file_list = os.listdir(default_path)
                for repo_file in repo_file_list:
                    if repo_file.startswith("data"):
                        with open(os.path.join(default_path, repo_file), 'r+') as json_file:
                            return json.load(json_file)
        except Exception as e:
            print("%s \nNew Repo folder and/or JSON file will be created!" % e)
            pass
            # if not os.path.exists(repo_dir):
            #     os.mkdir(repo_dir)
            return {}
    else:
        return {}

    return {}


def save_lib(repo_lib):
    ROOT = os.getcwd()
    main_dir = os.path.dirname(ROOT)
    repo_file_dir = os.path.join(main_dir, 'repo')
    json_repo_filepath = os.path.join(repo_file_dir, "regex_library.json")
    try:
        json.dump(repo_lib, json_repo_filepath, sort_keys=True, ensure_ascii=False, indent=4)
    except IOError as e:
        print("%s \nNew Repo folder and/or JSON file will be created!" % e)
        if not os.path.exists(repo_file_dir):
            os.mkdir(repo_file_dir)
        json.dump(repo_lib, json_repo_filepath, sort_keys=True, ensure_ascii=False, indent=4)

    return
