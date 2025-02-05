import os
import subprocess
from typing import final

from bot import logger
from bot.api.gdrive import GoogleDriveManager
from bot.api.scheduler import Scheduler
from bot.api.tar import TarManager
from bot.config import SA_FILE_PATH, MYSQL_USER, MYSQL_PASS


@final
class BackupManager(object):
    _gd_manager: GoogleDriveManager
    _tar_manager: TarManager
    _scheduler = Scheduler()

    def __init__(
            self,
            timestamp: str,
            source_dir: str,
            destination_dir: str,
    ):
        self._scopes = [r"https://www.googleapis.com/auth/drive"]
        self._sa_file_path = rf"{SA_FILE_PATH}"
        self._gd_manager = GoogleDriveManager(scopes=self._scopes, sa_file_path=self._sa_file_path)
        self._filename = f"backup-{timestamp}"
        self._tar_manager = TarManager(source_dir=source_dir, destination_dir=destination_dir, tar_name=self._filename)

    def create_backup(self) -> bool:
        logger.info("Starting backup procedure")
        filepath = self._tar_manager.create_tar()
        if filepath is None:
            logger.error("Backup procedure failed, filepath is None")
            return False

        logger.info("Creating mysql dump")
        self.create_mysql_dump(filepath)

        folder_id = self._gd_manager.get_folder()["id"]
        self._gd_manager.upload_file(folder_id, self._filename, filepath)
        logger.info("Backup procedure successfully ended")

        return True

    def create_mysql_dump(self, backup_dir: str):
        backup_file = os.path.join(backup_dir, f"{self._filename}.sql")
        command = f"mysqldump -u {MYSQL_USER} -p'{MYSQL_PASS}' --all-databases > {backup_file}"

        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                logger.info(f"Backup created: {backup_file}")
            else:
                logger.error(f"Error creating backup: {result.stderr}")
                return None
        except subprocess.CalledProcessError as e:
            logger.error(f"Subprocess error: {e}")
            return None

        return backup_file

    def run_backup_task(self, time: str):
        self._scheduler.add_tasks(time, self._gd_manager.clear_old_files)
        self._scheduler.add_tasks(time, self.create_backup)
        self._scheduler.run()
