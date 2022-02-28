import requests
from flask import current_app as app
import json
from sqlalchemy import text

def create_container(ipcam_url, socket_port, cctv_id):
    body = {
        "AttachStderr": True,
	    "AttachStdin": True,
	    "AttachStdout": True,
	    "Cmd": [
		    "--ipcam", f"{ipcam_url}",
		    "--socketport", f"{socket_port}",
		    "--cctvid", f"{cctv_id}"
	    ],
	    "ExposedPorts": {
		    f"{socket_port}/tcp": {}
	    },
	    "HostConfig": {
		    "AutoRemove": True,
		    "DeviceRequests": [
			    {
				    "Capabilities": [["gpu"]],
				    "Count": 0,
				    "DeviceIDs": ["1"]
			    }
		    ],
            "PortBindings": {
                f"{socket_port}/tcp": [
                    {
                        "HostIp": "",
                        "HostPort": f"{socket_port}"
                    }
                ]
            }
        },
        "Image": app.config.config['docker']['image_name']
    }

    docker_server = app.config.config['docker']['server']
    port = app.config.config['docker']['port']
    docker_api_version = app.config.config['docker']['docker_api_version']
    container_name = app.config.config['docker']['container_name']

    res = requests.post(f'http://{docker_server}:{port}/{docker_api_version}/containers/create?name={container_name}-{cctv_id}', json=body)
    # res = requests.post('http://163.180.117.38:2375/v1.41/containers/create?name=fire-smoke', json=body)
    return res


def start_container(cctv_id):
    docker_server = app.config.config['docker']['server']
    port = app.config.config['docker']['port']
    docker_api_version = app.config.config['docker']['docker_api_version']

    res = requests.post(f'http://{docker_server}:{port}/{docker_api_version}/containers/fire-smoke-{cctv_id}/start')


def check_cctv():
    docker_server = app.config.config['docker']['server']
    port = app.config.config['docker']['port']
    docker_api_version = app.config.config['docker']['docker_api_version']
    container_name = app.config.config['docker']['container_name']

    db_cctv_list = []

    try:
        results = app.database.execute(text('''
            SELECT * FROM cctv
        ''')).fetchall()
        
    except Exception as exc:
        return exc


    for result in results:
        db_cctv_list.append(result['cctv_id'])

    res = requests.get(f'http://{docker_server}:{port}/{docker_api_version}/containers/json')
    results = json.loads(res.text)

    for result in results:
        if f'{container_name}' in result['Names'][0]:
            a = result['Names'][0].rfind('-')
            cctv_id = int(result['Names'][0][a+1:])

            if cctv_id not in db_cctv_list:
                res = requests.post(f'http://{docker_server}:{port}/{docker_api_version}/containers/{container_name}-{cctv_id}/stop')
                
            else:
                pass
            