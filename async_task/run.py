import argparse
import subprocess
import sys


def main():
    arg_parse = argparse.ArgumentParser(description='Сохранение данных из сайта spimex')
    arg_parse.add_argument('--mode', choices=['async', 'sync'], default='async', help='Режим запуска (sync, async)')
    args = arg_parse.parse_args()

    mode = args.mode

    if mode == 'async':
        subprocess.run(['alembic', 'upgrade', 'head'], cwd='app')
        subprocess.run([sys.executable, 'app/main.py'])
    elif mode == 'sync':
        subprocess.run(['alembic', 'upgrade', 'head'], cwd='sync_app')
        subprocess.run([sys.executable, 'sync_app/main.py'])


if __name__ == '__main__':
    main()
