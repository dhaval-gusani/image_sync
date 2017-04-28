import os
import argparse
from shutil import copyfile

SEPARATOR = os.sep
BASE_NODE1_DIR = ''
BASE_NODE2_DIR = ''
MODE = ''


def _process_file_diffs_(diff_list, source_dir, dest_dir):
    for diff in diff_list:
        if MODE == 'execute':
            print('Copying: ' + source_dir + SEPARATOR + diff)
            copyfile(source_dir + SEPARATOR + diff, dest_dir + SEPARATOR + diff)
        else:
            print("Difference: " + source_dir + SEPARATOR + diff)


def _get_corresponding_dest_dir(node, source_dir, dest_dir):
    return dest_dir + node[len(source_dir):]


def _sync_uni_direction_(source_dir, dest_dir):
    for dirpath, dirnames, filenames in os.walk(source_dir):
        dest_dirpath = _get_corresponding_dest_dir(dirpath, source_dir, dest_dir)

        if not os.path.isdir(dest_dirpath):
            if MODE == 'execute':
                os.makedirs(dest_dirpath)
            else:
                print('Difference: ' + dirpath + SEPARATOR)
                continue

        dest_sub_directories = os.listdir(dest_dirpath)
        files_diff = list(set(filenames) - set(dest_sub_directories))

        _process_file_diffs_(files_diff, dirpath, dest_dirpath)


def _sync_directories_():
    _sync_uni_direction_(BASE_NODE1_DIR, BASE_NODE2_DIR)
    _sync_uni_direction_(BASE_NODE2_DIR, BASE_NODE1_DIR)


def _parse_arguments_():
    """
    Parses command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-n1', '--node1', help='Directory path for node 1', action='store', required=True)
    parser.add_argument('-n2', '--node2', help='Directory path for node 2', action='store', required=True)
    parser.add_argument('-m', '--mode', help='Mode for this run <dry-run> or <execute>', action='store', required=True)
    return parser.parse_args()


if __name__ == '__main__':
    args = _parse_arguments_()
    MODE = args.mode
    BASE_NODE1_DIR = args.node1
    BASE_NODE2_DIR = args.node2
    _sync_directories_()
