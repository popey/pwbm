[![pwbm](https://snapcraft.io//pwbm/badge.svg)](https://snapcraft.io/pwbm)

# pwbm - Personal WayBack Machine

The goal of pwbm is to make an easy to use appliance which can be fed URLs which it scrapes periodically. The content is saved in a similar manner to the popular "Wayback machine". Howver as this is a 'personal' wayback machine, you control the URLs which are scanned and when. The archive is held locally and can be easily managed.

Note: Unlike the "real" wayback machine, `pwbm` does not seek to crawl the entire web, nor does it spider entire websites. It only archives specific URLs given to it. This is by design.

## Installation

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/pwbm)

`pwbm` is available as a snap in the Snap Store. The snap bundles everything needed to function, including `monolith`. Installation on Linux is as follows:

`snap install pwbm`

Note: due to the unfinished nature of `pwbm`, it's currently only available in the `edge` channel. 

Alternatively just clone this repo and run the shell script. You'll also need `monolith`.

## Usage

### Adding URLs

Simply run `pwbm` with a URL you'd like it to archive. This does not currently initiate a snapshot of that page.

`pwbm https://ubuntu.com/`

### Gathering page snapshots

Run `pwbm` to start a snapshot of every page.

`pwbm`

Results are stored in `$SNAP_USER_COMMON/archive` if instaled from a snap, or `./archive` if run outside of a snap. 

### How it works

It's super basic. `pwbm` just iterates through a list of URLs in a file, spawning `monolith` and saving the results in a datestamped file in a folder specific to the host and path. 

```
$ tree ~/snap/pwbm/common/archive/
/home/alan/snap/pwbm/common/archive/
└── ubuntu.com
    └── 2020-01-18T13:32:39+00:00-index.html

1 directory, 1 file
```

### Viewing results

Browse the files in the `archive/` folder and open them in a browse to view.

A convenience webserver has been added. It can be launched as follows, and presents the archive directory on port 8076.

`pwbm.server`

Visit `http://localhost:8076/` to view the snapshots.

## TODO

  - [ ] - More error checking
  - [x] - Add a webserver to make it more wayback-machine-like (and easy to use)
  - [ ] - Add option for manual pruning of archives
  - [ ] - Add option to remove URLs
  - [ ] - Add option to report on disk usage / number of snapshots / other stats
