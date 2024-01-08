# kombat-lt

KOMBAT live tracker is based on the KOMBAT algorithm, formerly integrated in Siril 1.2.
It is here used to track a pattern (eg. planetary surface1), and to propose a guiding through KStars control handset.

## Why?

I wrote this program because I use ```KStars``` for DSO astrophotography, especially because of its specific features (support of focuser,
astrometry alignment, etc.) but I prefer ```FireCapture``` when I switch to planetary sessions. And when I use its internal guiding, it seems to conflict
which ```Ekos``` and the tracking stops.

## Installation

```
$ pip install -r requirements
$ ./kombat-lt.py # can be ran
```

## Usage

My routine:

* Run ```KStars```, set up aligment and focusing, select target,
* Open the Mount Control,
* Start a terminal and minimize it (eg. so that only 3 lines are visible),
* Run ```FireCapture``` and adjust settings (gain, etc.),
* For a more accurate guiding, use the 100% view,
* Identify a target zone that could be used for tracking (not to close to screen's border nor to another window above),
* Make a screenshot of this zone and keep it in clipboard,
* Close the screenshot app!
* Use the terminal to start ```./kombat-lt.py```