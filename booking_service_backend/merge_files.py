import os


def collect_project_code(target_folder="app", output_filename="project_code.txt"):
    root_dir = os.getcwd()
    source_dir = os.path.join(root_dir, target_folder)

    if not os.path.exists(source_dir):
        print(f"Error: folder '{target_folder}' was not found {root_dir}")
        return

    with open(output_filename, "w", encoding="utf-8") as outfile:
        for root, dirs, files in os.walk(source_dir):
            if "__pycache__" in dirs:
                dirs.remove("__pycache__")

            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, root_dir)

                    try:
                        with open(file_path, "r", encoding="utf-8") as infile:
                            outfile.write(f"\n{'=' * 60}\n")
                            outfile.write(f"PATH: {rel_path}\n")
                            outfile.write(f"{'=' * 60}\n\n")
                            outfile.write(infile.read())
                            outfile.write("\n")
                        print(f"Added: {rel_path}")
                    except Exception as e:
                        print(e)
    print(f"\nDone, file: {output_filename}")


if __name__ == "__main__":
    collect_project_code(target_folder="app")
