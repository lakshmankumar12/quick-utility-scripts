#!/usr/bin/python3

import argparse
import os
import subprocess

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Start Docker-based desktop environment")
    parser.add_argument("-n", "--name", help="Container name")
    parser.add_argument("-p", "--port", default="6080", help="Local port to forward")
    parser.add_argument("-w", "--writedir", help="Directory to mount for downloads")
    parser.add_argument("-P", "--passwd", default="", help="VNC password")
    parser.add_argument("-S", "--sudo", action="store_true", help="Run Docker command with sudo")
    parser.add_argument("-D", "--dryrun", action="store_true", help="Dry Run.. just print docker command")
    parser.add_argument("what", nargs="?", help="choose container", default="chrome", choices=["desktop", "chrome"])

    args = parser.parse_args()

    extra_args = []
    target_port = 12345
    pass_var_name = "PASSWORD"
    cont_name = "royzheng/chrome:latest"
    write_target = "/config/Downloads"

    if args.what == "desktop":
        target_port = 80
        pass_var_name = "VNC_PASSWORD"
        cont_name = "dorowu/ubuntu-desktop-lxde-vnc"
        write_target = "/root/Downloads"
    elif args.what == "chrome":
        extra_args.extend(["-e", "PORT=12345"])
        if not args.passwd:
            args.passwd = "password"

    if not args.name:
        args.name = f"lakshman_{args.what}"

    if not args.writedir:
        args.writedir = f"/tmp/{args.name}/Downloads"

    os.makedirs(args.writedir, exist_ok=True)

    docker_cmd = [
        "docker", "run", "-d", "--rm",
        "--name", args.name,
        "-p", f"{args.port}:{target_port}",
        "-v", "/dev/shm:/dev/shm",
        "-v", f"{os.path.expanduser('~')}:/hosthome:ro",
        "-v", f"{args.writedir}:{write_target}",
        "--add-host", "myhost:host-gateway"
    ]
    docker_cmd.extend(extra_args)

    env_file_created = False
    env_file = f"/tmp/{args.name}/env"
    if args.passwd:
        with open(env_file, "w") as f:
            f.write(f"{pass_var_name}={args.passwd}\n")
        docker_cmd.extend(["--env-file", env_file])
        env_file_created = True

    # Add image name
    docker_cmd.append(cont_name)

    # Prepend sudo if requested
    if args.sudo:
        docker_cmd.insert(0, "sudo")

    # Print and execute the command
    action = "running: "
    if args.dryrun:
        action = "Command:\n\n"
    print(f"{action}{' '.join(docker_cmd)}")
    if not args.dryrun:
        subprocess.run(docker_cmd)
    else:
        print(f"\nmkdir -p {args.writedir}")
        if env_file_created:
            print(f"cat <<EOF > {env_file}")
            with open(env_file) as fd:
                print(fd.read(), end='')
            print ('EOF')
        print()

    # Clean up env file if it was created
    if env_file_created and os.path.exists(env_file):
        os.remove(env_file)

if __name__ == "__main__":
    main()
