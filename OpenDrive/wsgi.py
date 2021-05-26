from OpenDrive import create_app

if __name__ == "__main__":
    create_app('production').run(host='0.0.0.0')
