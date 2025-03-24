import subprocess

def run_lz77(mode, input_file, output_file, windows_size, match_len):
    try:
        result = subprocess.run(
            ["./lz77", mode, input_file, output_file, str(windows_size), str(match_len)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print("Ошибка:", e.stderr)
