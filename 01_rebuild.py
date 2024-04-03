import os
# change the dataset root and generated recreate tool path
# if your directory is not consisted with README
ROOT = "WorldCup"
TOOL = "ita_public_tools"
OUTPUT = "RecreatedLog"


def rebuild(root: str, tool: str, output: str):
    for file_name in os.listdir(root):
        file_path = os.path.join(root, file_name)
        recreate_executable_path = os.path.join(tool, os.path.join("bin", "recreate"))
        object_mappings_path = os.path.join(tool, os.path.join("state", "object_mappings.sort"))
        output_path = os.path.join(output, file_name[:-3]+".log")
        cmd = ["gzip", "-dc", file_path, "|", recreate_executable_path, object_mappings_path, ">", output_path]
        cmd_str = ""
        for c in cmd:
            cmd_str += c+" "
        os.system(cmd_str)


if __name__ == "__main__":
    if not os.path.exists(OUTPUT):
        os.makedirs(OUTPUT)
    rebuild(ROOT, TOOL, OUTPUT)
