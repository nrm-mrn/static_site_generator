import os, shutil


def main():
    working_dir = os.getcwd()
    target_dir = "public"
    target_path = os.path.join(working_dir, target_dir)
    source_path = os.path.join(working_dir, "src", "static")

    def copy_content(source_path, target_path):
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
        os.mkdir(target_path)
        for obj in os.listdir(source_path):
            obj_path = os.path.join(source_path, obj)
            if os.path.isfile(obj_path):
                shutil.copy(obj_path, target_path)
            else:
                target_path = os.path.join(target_path, obj)
                copy_content(obj_path, target_path)

    copy_content(source_path, target_path)


main()
