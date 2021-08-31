import subprocess
import handlers
import os

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    (proceed, yaml_dict) = handlers.isactive()
    if proceed:
        for command in ['animated', 'sandwich']:
            url= yaml_dict.get(command).get("url")
            print(url)

            subprocess.run(['./get_gif.sh', url, command], cwd=base_dir)
