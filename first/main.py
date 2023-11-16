import concurrent.futures
import logging
import pathlib as pl
import threading


class Worker:
    def __init__(self, dir: pl.Path):
        self.dict_of_known_fileformat = {(".png", ".jpg", ".jpeg", ".svg"): "IMAGES",
                                         (".avi", ".mp4", ".mov", ".mkv"): "VIDEOS",
                                         (".mp3", ".ogg", ".wav", ".amr"): "AUDIO",
                                         (".gz", ".zip", ".tar"): "ARCHIVES",
                                         (".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"): "DOCUMENTS", (): "UNKNOWN"
                                         }

        self.main_dir = dir
        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        self.threads = []
        self.count = 0

    def change_directory(self, file_path: pl.Path):
        for extensions, category in self.dict_of_known_fileformat.items():
            if file_path.suffix in extensions:
                target_dir = self.main_dir / category
                if not file_path.parent == target_dir:
                    new_name = f"{self.count}{file_path.stem}{file_path.suffix}"
                    file_path.rename(target_dir / new_name)
                    self.count += 1
                return
        unknown_dir = self.main_dir / "UNKNOWN"
        if not file_path.parent == unknown_dir:
            new_name = f"{self.count}{file_path.stem}{file_path.suffix}"
            file_path.rename(unknown_dir / new_name)
            self.count += 1

    def find_all_dirs(self, pb: pl.Path):
        logging.info(f'Thread :id ={threading.get_ident()}')
        logging.info(f'Thread :name ={threading.current_thread().name}')

        for item in pb.iterdir():
            if item.is_dir():
                self.threads.append(self.pool.submit(self.find_all_dirs, item))
            else:
                self.threads.append(self.pool.submit(self.change_directory, item))

    def organize_dirs(self, start_dir: pl.Path):
        for category in self.dict_of_known_fileformat.values():
            target_dir = self.main_dir / category
            target_dir.mkdir(parents=True, exist_ok=True)

        self.find_all_dirs(start_dir)
        for i in self.threads:
            i.result()
        self.delete_empty_folders(start_dir)

    def delete_empty_folders(self, dir_path: pl.Path):
        logging.info(f'Thread :id ={threading.get_ident()}')
        logging.info(f'Thread :name ={threading.current_thread().name}')
        for folder in dir_path.iterdir():
            if folder.is_dir():
                self.delete_empty_folders(folder)
        if not any(dir_path.iterdir()):
            dir_path.rmdir()


def main():
    logging.basicConfig(level=logging.DEBUG)
    start_dir = pl.Path(r"C:\Users\Miran\Desktop\Нова папка")

    w = Worker(start_dir)
    w.organize_dirs(start_dir)


if __name__ == "__main__":
    main()
