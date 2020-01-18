# pwbm - Personal WayBack Machine

The goal of pwbm is to make an easy to use appliance which can be fed URLs which it scrapes periodically. The content is saved in a similar manner to the popular "Wayback machine". Howver as this is a 'personal' wayback machine, you control the URLs which are scanned and when. The archive is held locally and can be easily managed.

Note: Unlike the "real" wayback machine, `pwbm` does not seek to crawl the entire web, nor does it spider entire websites. It only archives specific URLs given to it. This is by design.

## Installation

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

### How it works

It's super basic. `pwbm` just iterates through a list of URLs in a file, spawning `monolith` and saving the results in a datestamped file in a folder specific to the host and path. 

```
$ tree ~/snap/pwbm/common/archive/
/home/alan/snap/pwbm/common/archive/
└── ubuntu.com
    └── 2020-01-18T13:32:39+00:00-index.html

1 directory, 1 file
```
