"""Code extraction utilities."""

import os
from pathlib import Path


def extract_code(package_path: str, output_file: str) -> None:
    """Extract `*.py` source from the given package and write to `output_file`.

    Args:
    ----
        package_path: path to the package to extract code from
        output_file: path to the text file to write the output to

    """
    with Path(output_file).open("w", encoding="utf-8") as outfile:
        for root, _dirs, _files in os.walk(package_path):
            Path(root).glob("*.py")
            for file in Path(root).glob("*.py"):
                file_path = os.path.relpath(file, package_path)
                with Path(file).open(encoding="utf-8") as inner_file:
                    lines = inner_file.readlines()
                    file_path_unix = file_path.replace("\\", "/")
                    outfile.write(f"#=> {file_path_unix} ---START---\n")
                    for i, line in enumerate(lines):
                        line_number = str(i + 1).zfill(3)  # Pad line numbers with zeros
                        outfile.write(f"{line_number}: {line}")
                    outfile.write(f"#=> {file_path_unix} ---END---\n")
                    outfile.write("\n\n")


if __name__ == "__main__":
    extract_code(
        package_path="./src/chilly_bird", output_file="./out/extracted_code.txt"
    )
