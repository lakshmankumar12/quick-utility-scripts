import argparse
import os
import subprocess

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Start Docker-based desktop environment")
    parser.add_argument("--name", default="lakshman_desktop", help="Container name")
    parser.add_argument("--fwd_local_port", default="6080", help="Local port to forward")
    parser.add_argument("--WRITEDIR", help="Directory to mount for downloads")
    parser.add_argument("--passwd", default="", help="VNC password")
    parser.add_argument("--do_sudo", action="store_true", help="Run Docker command with sudo")

    # Parse arguments
    args = parser.parse_args()

    # Set default WRITEDIR if not provided
    if not args.WRITEDIR:
        args.WRITEDIR = f"/tmp/{args.name}/Downloads"

    # Create write directory
    os.makedirs(args.WRITEDIR, exist_ok=True)

    # Build Docker command
    docker_cmd = [
        "docker", "run", "-d", "--rm",
        "--name", args.name,
        "-p", f"{args.fwd_local_port}:80",
        "-v", "/dev/shm:/dev/shm",
        "-v", f"{os.path.expanduser('~')}:/hosthome:ro",
        "-v", f"{args.WRITEDIR}:/root/Downloads",
        "--add-host", "myhost:host-gateway"
    ]

    # Add env file if password is set
    env_file_created = False
    if args.passwd:
        with open("env", "w") as f:
            f.write(f"VNC_PASSWORD={args.passwd}\n")
        docker_cmd.extend(["--env-file", "./env"])
        env_file_created = True

    # Add image name
    docker_cmd.append("dorowu/ubuntu-desktop-lxde-vnc")

    # Prepend sudo if requested
    if args.do_sudo:
        docker_cmd.insert(0, "sudo")

    # Print and execute the command
    print("running:", " ".join(docker_cmd))
    subprocess.run(docker_cmd)

    # Clean up env file if it was created
    if env_file_created and os.path.exists("env"):
        os.remove("env")

if __name__ == "__main__":
    main()
