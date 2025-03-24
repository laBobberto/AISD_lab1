import subprocess

def run_bwt(mode, input_file, output_file, block_size):
    try:
        result = subprocess.run(
            ["./BWT", mode, input_file, output_file, str(block_size)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print("Ошибка:", e.stderr)


