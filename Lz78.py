import subprocess

def run_lz78(mode, input_file, output_file):
    try:
        result = subprocess.run(
            ["./lz78", mode, input_file, output_file],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print("Ошибка:", e.stderr)
