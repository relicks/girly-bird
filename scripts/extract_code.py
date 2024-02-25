import glob
import os


def extract_code(package_path: str, output_file: str) -> None:
    with open(output_file, "w", encoding="utf-8") as outfile:
        for root, _dirs, _files in os.walk(package_path):
            for file in glob.glob(os.path.join(root, "*.py")):
                file_path = os.path.relpath(file, package_path)
                with open(file, encoding="utf-8") as inner_file:
                    lines = inner_file.readlines()
                    file_path_unix = file_path.replace("\\", "/")
                    outfile.write(f"###! {file_path_unix} ---START---\n")
                    for i, line in enumerate(lines):
                        line_number = str(i + 1).zfill(3)  # Pad line numbers with zeros
                        outfile.write(f"{line_number}: {line}")
                    outfile.write(f"###! {file_path_unix} ---END---\n")
                    outfile.write("\n\n")


if __name__ == "__main__":
    package_path = "./src/chilly_bird"
    output_file = "./out/extracted_code.txt"

    extract_code(package_path, output_file)
