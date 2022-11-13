# S3 File locator

## Description
A simple Python tool that allows searching for files in an S3 bucket whose contents match a given substring. The program outputs a list of matching files (if any) and downloads them to a configurable _staging area_ for further inspection.

## Dependencies
The tool requires Python 3.9+ and the [Boto3 AWS SDK](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) to be installed and available in order to interact with the S3 service. For managing Python installations for different versions you can use [pyenv](https://github.com/pyenv/pyenv). Once the correct version is installed and activated, Boto3 can be installed like this:

``` sh
pip3 install boto3
```

It also makes no assumptions about the potentially required credentials for accessing the contents of the bucket. It instead relies on [Boto3's standard mechanisms](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html) for credentials location and successful authorization. It is recommended that users of the tool obtain necessary AWS credentials via their preferred method and store them in `~/.aws/credentials`.

If the credentials file holds credentials for multiple profiles, the profile to be used can be specified via environment variables like so:

``` sh
AWS_PROFILE=<desired profile> python locate-files.py [...]
```

## Usage
Detailed usage instructions can be checked via the `--help` flag:

``` sh
$ python locate-files.py --help
usage: locate-files.py [-h] [-s STAGING_AREA] substring bucket_name

Locates files inside a S3 bucket that match a given substring, and stores them locally in the specified staging area.

positional arguments:
  substring             The substring to look for
  bucket_name           The name of the bucket to look in

optional arguments:
  -h, --help            show this help message and exit
  -s STAGING_AREA, --staging-area STAGING_AREA
                        Where to store the files that matched the substring (defaults to /tmp/<bucket_name)
```

## Development
In order to further develop the tool, you will first need to clone the repository:

``` sh
git clone https://github.com/cronos2/limehome-devops-challenge
```

Then, create a virtual environment via [`venv`](https://docs.python.org/3/library/venv.html) and install the dependencies:

``` sh
python3 -m venv .venv --upgrade-deps
source .venv/bin/activate
python -m pip install requirements.txt
```

