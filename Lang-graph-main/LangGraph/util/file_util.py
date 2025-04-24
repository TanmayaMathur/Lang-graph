import os
import uuid
from datetime import datetime

class FileUtils:
    @staticmethod
    def upload_file(file: bytes, file_path: str, file_name: str) -> None:
        """Upload a file to the specified path."""
        target_file = os.path.dirname(file_path)
        if not os.path.exists(target_file):
            os.makedirs(target_file)
        with open(os.path.join(file_path, file_name), 'wb') as out:
            out.write(file)

    @staticmethod
    def get_folder() -> str:
        """Get the current date folder name in yyyy-MM-dd format."""
        return datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def random_uuid() -> str:
        """Generate a random UUID."""
        return str(uuid.uuid4()) 