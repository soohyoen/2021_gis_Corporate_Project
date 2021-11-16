import json

def load_conf():
    with open('conf.json') as f:
        config = json.load(f)

    return config

if __name__ == '__main__':
    conf = load_conf()