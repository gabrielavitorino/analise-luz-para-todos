import subprocess
import sys


def run(script: str) -> None:
    subprocess.run([sys.executable, script], check=True)


if __name__ == "__main__":
    run("src/download_data.py")
    run("src/process_data.py")
    run("src/generate_charts.py")
    print("Pipeline concluído.")
