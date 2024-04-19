# FIS Alpin Snowboarding Database

[Enso](http://enso.org) project to download FIS results into `.csv` files
and to process them further.

## Download

To dowload one needs an installation of the [Enso Engine](http://enso.org) for
your operating system. Daily [version from Mar 26, 2024](https://github.com/enso-org/enso/releases/download/2024.1.1-nightly.2024.4.19/)
is known to work. If on Linux download [enso-bundle-2024.1.1-nightly.2024.4.19-linux-amd64.tar.gz](https://github.com/enso-org/enso/releases/download/2024.1.1-nightly.2024.4.19/enso-bundle-2024.1.1-nightly.2024.4.19-linux-amd64.tar.gz):

```bash
$ wget https://github.com/enso-org/enso/releases/download/2024.1.1-nightly.2024.4.19/enso-bundle-2024.1.1-nightly.2024.4.19-linux-amd64.tar.gz
# enso-bundle is downloaded to your disk
$ ls enso-bundle-*.gz
enso-bundle-2024.1.1-nightly.2024.4.19-linux-amd64.tar.gz
$ tar fxz enso-bundle-*.gz
# enso directory is created
$ ls enso
bin  dist  README.md  runtime  THIRD-PARTY
$ ./enso/bin/enso
$ ./enso/bin/enso run src/Download.enso
# downloads all the data and updates files in data directory
$ git status data/*.csv
```
