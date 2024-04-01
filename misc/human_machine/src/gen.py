import os
import random
import base64


def generate_random_string(length):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choice(characters) for _ in range(length))


def generate_and_save_files(folder_path, num_files):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for i in range(1, num_files + 1):
        random_string = generate_random_string(random.randint(20, 40))
        encoded_string = base64.b64encode(random_string.encode()).decode()

        file_name = f"file_{i}.txt"
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, "w") as file:
            file.write(encoded_string)

        print("Saved", i, "file:", encoded_string)


if __name__ == "__main__":
    folder_path = "files"
    num_files = 100000

    generate_and_save_files(folder_path, num_files)
    print(f"{num_files} files generated and saved in the '{folder_path}' folder.")
