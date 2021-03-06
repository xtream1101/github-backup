import os
import json
import argparse
import urllib.request
import time

# set up args
parser = argparse.ArgumentParser(description='backup github account')
parser.add_argument('user', metavar='userA', type=str, help='github user account')
parser.add_argument('output_dir', metavar='/git_backups/', type=str, default='.',
                    help='path that the backups will be stored in')
parser.add_argument('-f', '--format_dir', default="&user/&repo__&user", help='setup dir format of repos')
parser.add_argument('-up', '--update', action='store_true', help='get list of users repos')
parser.add_argument('-s', '--starred', action='store_true', help='get users starred reops')
parser.add_argument('-m', '--mirror', action='store_true', help='mirror the repos')
args = parser.parse_args()

# get args
user = args.user
base_dir = args.output_dir + '/'
format_dir = args.format_dir
starred = args.starred
update = args.update
mirror = args.mirror


def get_json(json_file, endpoint):
    """
    Read from local json file if update was not passed and the file exists
    :return: dictionary of git data on the repos
    """
    if update or not os.path.isfile(json_file):
        print("Fetching repo list form github")
        empty = False
        page = 1
        user_data = []
        while not empty:
            request = 'https://api.github.com/users/' + user + '/' + endpoint + '?page=' + str(page)
            response = urllib.request.urlopen(request)
            page_json = response.readall().decode('utf-8')
            repo_list = json.loads(page_json)
            if len(repo_list) > 0:
                user_data.extend(repo_list)
            else:
                empty = True
            # Saves 1 api call per user
            #   because each page is filled with 30 repos,
            #   so if a page has less you are on the last page
            if len(repo_list) < 30:
                empty = True
            page += 1
        save_json(json_file, user_data)
    else:
        with open(json_file) as json_data:
            user_data = json.load(json_data)
        print("Loaded from json file")
    return user_data


def save_json(file, data):
    """
    Save local json file. This way we do not need to always hit http://api.github.com
    :param data: dictionary of git data on each repo
    :return:
    """
    if not os.path.exists(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))
    with open(file, 'w') as save_file:
        json.dump(data, save_file, indent=4)


def save_all(json_file, endpoint, extra_dir=''):
    # Loop through repos to get the url and name to pass along
    for repo in get_json(json_file, endpoint):
        print("Getting: " + repo['ssh_url'])
        # Build save path
        save_name = format_dir.replace('&user', repo['owner']['login']).replace('&repo', repo['name'])
        if extra_dir:
            save_name = user + '/' + extra_dir + '/' + save_name.split('/')[-1]
        save_name = base_dir + save_name
        save_repo(repo['ssh_url'], save_name)


def save_repo(url, repo_dir):
    """
    Add new repo or update current
    :param url: git url to clone
    :param repo_dir: name of repo
    :return:
    """
    print(repo_dir)
    add_cmd = ""
    if mirror:
        repo_dir += "__mirror"
        update_cmd = "remote update"
        add_cmd = "--mirror"
    else:
        update_cmd = "pull"

    if os.path.exists(repo_dir):
        os.system("git -C " + repo_dir + " " + update_cmd)
    else:
        os.system("git clone " + add_cmd + " " + url + " " + repo_dir)


def humanize_time(secs):
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return '%02d:%02d:%02d' % (hours, mins, secs)

if __name__ == "__main__":
    start_time = time.time()
    repo_file = base_dir +  user + '_repos.json'
    starred_file = base_dir + user + '_starred.json'

    # Get all the repos of the user
    save_all(repo_file, 'repos')
    if starred:
        save_all(starred_file, 'starred', '_starred/')

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("\nTime Elapsed: " + humanize_time(elapsed_time) + "\n")

