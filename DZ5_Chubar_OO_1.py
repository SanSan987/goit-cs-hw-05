import argparse
import asyncio
import os
import shutil
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

async def read_folder(source_folder: Path, output_folder: Path):
    tasks = []
    for item in source_folder.rglob('*'):
        if item.is_file():
            tasks.append(copy_file(item, output_folder))
    await asyncio.gather(*tasks)

async def copy_file(file_path: Path, output_folder: Path):
    try:
        ext = file_path.suffix[1:] if file_path.suffix else 'no_extension'
        destination = output_folder / ext
        destination.mkdir(parents=True, exist_ok=True)
        shutil.copy(file_path, destination / file_path.name)
        logging.info(f"Copied {file_path} to {destination / file_path.name}")
    except Exception as e:
        logging.error(f"Failed to copy {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Asynchronously sort files by extension")
    parser.add_argument("source_folder", type=str, help="Source folder path")
    parser.add_argument("output_folder", type=str, help="Output folder path")
    args = parser.parse_args()

    source_folder = Path(args.source_folder)
    output_folder = Path(args.output_folder)

    if not source_folder.is_dir():
        logging.error("Source folder does not exist or is not a directory")
        return

    asyncio.run(read_folder(source_folder, output_folder))

if __name__ == "__main__":
    main()
