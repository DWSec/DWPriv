# DWTrace
DWTrace is a tool designed to evaluate the privacy of Android applications and is aimed at gaining a better understanding of Android permissions in general. We have a  writeup on our research blog about why we developed the tool; it also included an example scenario of analysing the COVID-19 contact tracing apps: [link](https://research.darkwaves.io/privacy-tracing-and-tracking-on-android/).

![usage example](readme_media/terminal_example.gif)

If you then navigate to the "reports" folder, you'll notice an html file named like the app's package name, and if you open it:

![usage example](readme_media/output_example.gif)

We hope this tool can be a valid aid to assess quickly and easily if an app respects the users's privacy. 

## Features
### Scoring system
You might have noticed a number in the output when running DWTrace from the terminal: DWTrace allows you to define a whitelist of permissions that are allowed; it will then highlight, in the html report, whitelisted items (in green) and the rest in red, so that you can easily see if app is using a permission it's not supposed to

### Batch or single file mode
DWTrace can be run on a single apk file, or a folder of apps. These are, respectively, the ```--i``` and ```--f``` options

### Cheatsheet
There are a lot of possible permissions an app can request. To make it easier to know exactly what a permission is doing, in the report, when you hover over a permission, it will bring up a detailed description of what this permission does. In a future update of the software this will also be available for the uses-feature section of the report. In a future update, the whitelist will also be available as a standalone html file to quickly and easily get more info on any android permission.

### Whitelist
You might have noticed that some items in the output are highlighted in red and some in green. This is because DWTtrace allows you to define whitelisted items (that will be highlighted in green). More info on why you might want to use this feature in [this article](https://research.darkwaves.io/privacy-tracing-and-tracking-on-android/).
Currently, to edit the whitelist, you need to edit the ```dwtrace.py``` file; there exist two arrays, one called ```whitelistedPermissions```, and the other ```whitelistedHardware``` that you can edit to add any permissions you want. In a future update there will be an easy to reference cheatsheet in html format with all the Android permissions, and the whitelist will be moved to a separate json file. 

# Installation
* Clone the repository and cd into it
* create a new virtual envirornment with ```virtualenv env``` and then activate it ```env/Scripts/bin/activate```
* install the required python libraries with ```pip install -r requirements.txt```
* install axmldec: [link](https://github.com/ytsutano/axmldec); on Linux and Windows, move the executable in the same folder as run_dwtrace.py
