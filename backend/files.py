import os

mm_path = os.path.expanduser('~') + "/.music-manager"
bucket_file = "bucketlist.txt"
album_file = "albums.txt"

def ensure_files_exist():
    if not os.path.isdir(mm_path):
        os.mkdir(os.path.expanduser('~') + "/.music-manager")

    bf_path = mm_path + "/" + bucket_file
    af_path = mm_path + "/" + album_file
    if not os.path.exists(bf_path):
        b = open(bf_path, "x")
    if not os.path.exists(af_path):
        a = open(af_path, "x")

def read_bucket_list():
    pass

def read_album_list():
    pass

def update_bucket_list():
    pass

def update_album_list():
    pass