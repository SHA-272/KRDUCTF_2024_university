import os
import base64

folder_path = input("Введите путь к папке: ")  # Ввод пути к папке


def decode_base64_and_check(file_path):
    with open(file_path, "rb") as file:
        encoded_content = file.read()
        try:
            decoded_content = base64.b64decode(encoded_content).decode("utf-8")
            if decoded_content.startswith("krdu"):
                return True
            else:
                return False
        except Exception as e:
            print(f"Ошибка декодирования файла {file_path}: {e}")
            return False


def process_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            if decode_base64_and_check(file_path):
                print(f"Файл {filename} начинается с 'krdu'")
                break
            else:
                print(f"Файл {filename} не содержит 'krdu' в начале")


# Запуск скрипта
process_files_in_folder(folder_path)
