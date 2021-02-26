from pathlib import Path
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Copy files from an s3 path to local disk')
parser.add_argument('--coco', dest='coco', action='store_true')
parser.add_argument('s3_path', type=str)

def download_path(s3_path, folder=''):
    s3_path = s3_path + folder
    rel_path = Path(s3_path[5:])
    rel_path.mkdir(parents=True, exist_ok=True)
    cmd = f"aws s3 sync {s3_path} '{rel_path}'"
    print(cmd)
    subprocess.call(cmd, shell=True)

if __name__ == '__main__':
    args = parser.parse_args()

    if args.coco:
        download_path(args.s3_path, '/annotations')
        download_path(args.s3_path, '/images')
    else:
        download_path(args.s3_path)