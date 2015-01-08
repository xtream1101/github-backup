import os
import json
import argparse
import urllib.request


# set up args
parser = argparse.ArgumentParser(description='backup github account')
parser.add_argument('user', metavar='userA', type=str, help='github user account')
parser.add_argument('output_dir', metavar='/git_backups/', type=str, default='.',
                    help='path that the backups will be stored in')
parser.add_argument('-up', '--update', action='store_true', help='get list of users repos')
parser.add_argument('-m', '--mirror', action='store_true', help='mirror the repos')
args = parser.parse_args()

# get args
user = args.user
out_dir = args.output_dir
update = args.update
mirror = args.mirror

base_dir = out_dir+'/'+user+'/'
json_file = base_dir+'_'+user+'.json'


def get_json():
    """
    Read from local json file if update was not passed or file does not exist
    :return: dictionary of git data on each repo
    """
    if update or not os.path.isfile(json_file):
        request = 'https://api.github.com/users/'+user+'/repos'
        response = urllib.request.urlopen(request)
        user_json = response.readall().decode('utf-8')
        user_data = json.loads(user_json)
        save_json(user_data)
    else:
        with open(json_file) as json_data:
            user_data = json.load(json_data)
        print("Loaded from json file")
    return user_data


def save_json(data):
    """
    Save local json file. This way we do not need to always hit http://api.github.com
    :param data: dictionary of git data on each repo
    :return:
    """
    if not os.path.exists(os.path.dirname(json_file)):
        os.makedirs(os.path.dirname(json_file))
    with open(json_file, 'w') as save_file:
        json.dump(data, save_file, indent=4)


def save_repo(url, name):
    """
    Add new repo or update current
    :param url: git url to clone
    :param name: name of repo
    :return:
    """
    update_cmd = ""
    add_cmd = ""
    if mirror:
        repo_dir = base_dir+name+"_mirror"
        update_cmd = "remote update"
        add_cmd = "--mirror"
    else:
        repo_dir = base_dir+name
        update_cmd = "pull"

    if os.path.exists(repo_dir):
        os.system("git -C "+repo_dir+" "+update_cmd)
    else:
        os.system("git clone "+add_cmd+" "+url+" "+repo_dir)


if __name__ == "__main__":
    # Loop through repos to get the url and name to pass along
    for repo in get_json():
        print("Getting: "+repo['clone_url'])
        save_repo(repo['clone_url'], repo['name'])