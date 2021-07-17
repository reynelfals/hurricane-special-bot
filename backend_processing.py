import subprocess
import handlers

if __name__ == '__main__':
    (proceed, yaml_dict) = handlers.isactive()
    if proceed:
        for command in ['animated', 'sandwich']:
            url= yaml_dict.get(command).get("url")
            print(url)

            subprocess.call(['sh', './get_gif.sh', url, command])