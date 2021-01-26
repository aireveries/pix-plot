from pathlib import Path
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Copy output files to s3')
parser.add_argument('s3_path', type=str)

if __name__ == '__main__':
    args = parser.parse_args()
    rel_path = Path(args.s3_path[5:])
    out_s3_path = f's3://aireverie-html/{rel_path}'
    cmd = f"aws s3 sync output {out_s3_path}"
    print(cmd)
    subprocess.call(cmd, shell=True)