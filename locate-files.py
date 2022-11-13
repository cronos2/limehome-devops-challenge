from argparse import ArgumentParser
from pathlib import Path
from typing import Iterable, Optional
from os import makedirs

import boto3


def build_parser():
    parser = ArgumentParser(
        description=(
            'Locates files inside a S3 bucket that match a given substring, and'
            ' stores them locally in the specified staging area.'
        )
    )

    parser.add_argument('substring', help='The substring to look for')
    parser.add_argument('bucket_name', help='The name of the bucket to look in')
    parser.add_argument(
        '-s',
        '--staging-area',
        required=False,
        help='Where to store the files that matched the substring (defaults to /tmp/<bucket_name>)',
    )

    return parser


class FileLocator:
    s3_client = boto3.client('s3')
    s3 = boto3.resource('s3')

    def __init__(self, substring: str, bucket_name: str, staging_area: str):
        self.substring = substring
        self.bucket_name = bucket_name
        self.bucket = self.s3.Bucket(bucket_name)
        self.staging_area = Path(staging_area)

    def locate_files(self) -> Iterable[tuple[str, Path]]:
        makedirs(self.staging_area, exist_ok=True)
        for object_key in self.list_objects():
            output_path = self.handle_file(object_key)

            if output_path is not None:
                yield (object_key, output_path)

    def list_objects(self) -> Iterable[str]:
        # paginate the results in case there are too many objects in the bucket
        paginator = self.s3_client.get_paginator('list_objects_v2')

        for page in paginator.paginate(Bucket=self.bucket_name):
            for object_entry in page['Contents']:
                yield object_entry['Key']

    def handle_file(self, object_key: str) -> Optional[Path]:
        output_path = self.download_file(object_key)
        match_found = self.grep_file(output_path)

        if not match_found:
            output_path.unlink()
            return None

        return output_path


    def download_file(self, object_key: str) -> Path:
        output_path = self.staging_area / object_key
        self.bucket.download_file(
            Key=object_key,
            Filename=str(output_path),
        )

        return output_path

    def grep_file(self, file_path: Path) -> bool:
        with file_path.open() as f:
            for line in f.readlines():
                if self.substring in line:  # found a match
                    return True

            return False


def main():
    parser = build_parser()
    args = parser.parse_args()
    staging_area = (
        args.staging_area if args.staging_area is not None
        else f'/tmp/{args.bucket_name}'
    )

    locator = FileLocator(args.substring, args.bucket_name, staging_area)

    for matching_file, output_path in locator.locate_files():
        print(matching_file, output_path)


if __name__ == '__main__':
    main()
