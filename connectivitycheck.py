import os
import platform
import subprocess
import socket
import sys
import shutil

def install_required_modules():
    print("\n=== Installing Required Modules ===")

    try:
        import speedtest
        print("✅ speedtest-cli is already installed.")
    except ImportError:
        print("Installing speedtest-cli Python module...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "speedtest-cli"])
            print("✅ speedtest-cli installed successfully.")
        except subprocess.CalledProcessError:
            print("❌ Failed to install speedtest-cli. Please install manually.")

    os_type = platform.system().lower()

    if "linux" in os_type:
        print("\nInstalling system tools on Linux (requires sudo)...")
        packages = ["nmap", "iputils-tracepath", "traceroute"]
        for pkg in packages:
            if shutil.which(pkg.split("-")[0]):
                print(f"✅ {pkg} already installed.")
            else:
                print(f"Installing {pkg}...")
                os.system(f"sudo apt install -y {pkg}")
    elif "windows" in os_type:
        print("\nInstalling system tools on Windows (requires Chocolatey)...")
        if shutil.which("choco") is None:
            print("❌ Chocolatey not found. Please install from https://chocolatey.org/install and re-run.")
        else:
            if shutil.which("nping"):
                print("✅ nmap (nping) already installed.")
            else:
                print("Installing nmap via choco...")
                os.system("choco install nmap -y")
        print("✅ Note: tracert is built-in on Windows.")
    else:
        print("\n⚠️ Unknown OS. Please install manually:")
        print("   - speedtest-cli")
        print("   - nmap")
        print("   - tracepath/traceroute")

    print("\n✅ Installation complete.\n")

def cross_platform_ping(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    os.system(f"ping {param} 4 {host}")

def cross_platform_traceroute(host):
    print(f"\nRunning traceroute/tracepath for {host}...\n")
    os_type = platform.system().lower()

    if os_type == "windows":
        os.system(f"tracert {host}")
    else:
        if shutil.which("tracepath"):
            result = os.system(f"tracepath {host}")
            if result != 0 and shutil.which("traceroute"):
                print("⚠️ Tracepath failed. Trying traceroute...")
                os.system(f"traceroute {host}")
        elif shutil.which("traceroute"):
            os.system(f"traceroute {host}")
        else:
            print("❌ Neither tracepath nor traceroute is installed. Use Option 1 to install them.")

    print("\nNote:")
    print("• 'no reply' means intermediate routers may block traceroute ICMP/UDP packets.")
    print("• This is common with ISPs, cloud providers (AWS, Google), or firewalls.")
    print("• If early hops respond, your local connectivity is working.\n")

def check_connectivity(services):
    for name, host in services.items():
        print(f"\nPinging {name} ({host})...")
        cross_platform_ping(host)

def perform_speed_test():
    try:
        import speedtest
        print("\nRunning speed test...")
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        print(f"Download Speed: {download:.2f} Mbps")
        print(f"Upload Speed: {upload:.2f} Mbps\n")
    except ImportError:
        print("❌ speedtest-cli not installed. Use Option 1 to install it.\n")

def manual_ip_test():
    host = input("Enter IP or hostname to ping: ")
    cross_platform_ping(host)

def manual_nping_test():
    host = input("Enter IP or hostname for nping test: ")
    if shutil.which("nping"):
        os.system(f"nping {host}")
    else:
        print("❌ nping not found. Run Option 1 to install nmap/nping.")

def manual_port_test():
    host = input("Enter host/IP: ")
    try:
        port = int(input("Enter port number: "))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(3)
            sock.connect((host, port))
            print(f"✅ Port {port} on {host} is open.")
    except Exception as e:
        print(f"❌ Port {port} on {host} is not reachable.\nError: {e}")

def tracepath_test():
    host = input("Enter host or IP for traceroute/tracepath: ")
    cross_platform_traceroute(host)

def main():
    meeting_platforms = {
        "Webex": "webex.com",
        "Zoom": "zoom.us",
        "Microsoft Teams": "teams.microsoft.com",
        "Google Meet": "meet.google.com"
    }

    cloud_services = {
        "Azure": "azure.microsoft.com",
        "AWS": "aws.amazon.com",
        "Google Cloud": "cloud.google.com",
        "Cloudflare": "cloudflare.com",
        "Akamai": "akamai.com"
    }

    while True:
        print("""
=== Connectivity CLI Tool ===
1. Auto-Install Required Modules
2. Check Meeting Platform Connectivity
3. Check Cloud Service Connectivity
4. Perform Speed Test
5. Manual IP Test (Ping)
6. Manual IP Test (Nping)
7. Traceroute/Tracepath
8. Manual Port Test
9. Exit
""")
        choice = input("Select an option (1-9): ").strip()

        if choice == "1":
            install_required_modules()
        elif choice == "2":
            check_connectivity(meeting_platforms)
        elif choice == "3":
            check_connectivity(cloud_services)
        elif choice == "4":
            perform_speed_test()
        elif choice == "5":
            manual_ip_test()
        elif choice == "6":
            manual_nping_test()
        elif choice == "7":
            tracepath_test()
        elif choice == "8":
            manual_port_test()
        elif choice == "9":
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()

