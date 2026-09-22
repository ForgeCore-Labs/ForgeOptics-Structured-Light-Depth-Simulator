'''
the http-reuqest for headless mode process
make sure you run
.\ForgeOptics.exe --headless --host 127.0.0.1 --backend cuda --port 8080

'''
import os, sys
import urllib.request
import urllib.error
import json

url = "http://127.0.0.1:8080/render"
status_url = "http://127.0.0.1:8080/status"

def status_check() -> bool:
    try:
        with urllib.request.urlopen(status_url, timeout=3) as response:
            body = response.read().decode('utf-8')
            status_data = json.loads(body)
            # Returns True only if 'ok' is True AND 'busy' is False
            return status_data.get("ok", False) and not status_data.get("busy", True)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        # Debug line: uncomment this if it still returns False to see why!
        print(f"Connection failed: {e}")
        return False


def load_json(file_path):
    '''load dict -> json string -> raw bytes'''
    with open(file_path, "r", encoding="utf-8") as f:
        scene_data = json.load(f)
    # modif-scene settings here
    json_bytes = json.dumps(scene_data).encode("utf-8")
    return json_bytes

def structure_light_process(scene_config: str):
    '''http-request-process'''
    data = load_json(scene_config)
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req) as response:
        print(response.status)
        print(response.read().decode('utf-8'))

def batch():
    # single-item test:
    # single_test_file_path = r"...\scene_1.json"
    # structure_light_process(single_test_file_path)

    scenes_dir = r"scene folder path"
    for index, item in enumerate( os.listdir(scenes_dir)):
        scene_path = os.path.join(scenes_dir, item)
        structure_light_process(scene_path)
    pass

def main():
    if status_check():
        print("DEBUG-->ready to process!")
        batch()
    else:
        print("ERROR-->server is down!")

if __name__ == "__main__":
    main()
