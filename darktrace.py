import xml.dom.minidom as md
import flask
from flask import render_template
import json

#load the cheatsheet.json file for generating the tooltips (contains info on each permission: permission name, description and if it directly involves PII)
#info taken from: https://developer.android.com/reference/android/Manifest.permission
with open ("cheatsheet.json") as f:
    cheatsheet = json.load(f)

# TODO: go back to using an external file (whitelist.json) for the whitelisted permissions and hardware features

whitelistedPermissions = [
    "android.permission.BLUETOOTH",
    "android.permission.INTERNET"
    ]
whitelistedHardware = [
    "android.hardware.bluetooth_le",
    "android.hardware.bluetooth"
    ]

#load and parse the AndroidManifest.xml
manifest = md.parse('output/AndroidManifest.xml')

def generateReport (packageName, score, permissions, features):
    #flask stuff I guess
    app = flask.Flask('my app')
    
    with app.app_context():
        # generate the report using flask template
        report = render_template('report.html', title = packageName, score = score, permissions = permissions, features = features)

        #write the report to an html file in the reports folder
        reportFile = open ('reports/' + packageName + '.html', 'w')
        reportFile.write(report)
        reportFile.close()

def main ():
    # score, and lists containing the uses-permissions and uses-feature that the app uses
    score = 0
    permissions = []
    features = []

    # number of used features and permissions; used for calculating the score
    permissionNumber = manifest.getElementsByTagName('uses-permission').length
    featureNumber = manifest.getElementsByTagName('uses-feature').length

    #temporary number of used features and used hardware features to be compared against the actual number of hardware features and permissions used by the app
    tempPermissionNumber = 0
    tempFeatureNumber = 0

    #print (permissionNumber, featureNumber)

    #get the package name (com.foo.bar)
    for x in manifest.getElementsByTagName('manifest'):
        packageName = x.getAttribute('package')

    """
    ----------USES PERMISSION---------------
    """

    for permission in manifest.getElementsByTagName('uses-permission'):
        #check against the whitelisted items in the whitelist.json file
        if permission.getAttribute('android:name') in whitelistedPermissions:
            tempPermissionNumber += 1

            #save the permission to the permissions dictionary to generate the report later
            #if it was found in the whitelist, save it as whitelisted: true
            #if it was found in the whitelist, we can also provide a tooltip with more info on the permission

            #gathering additonal info on permission from cheatsheet.json
            #first check if the permission is in the cheatsheet
            if permission.getAttribute("android:name") in cheatsheet:
                #if so, create a string to pass to flask that will later be the tooltip for this specific permission

                # infoString = "Description: " + cheatsheet[permission.getAttribute("android:name")]["info"] + " - Directly collects PII?: " + cheatsheet[permission.getAttribute("android:name")]["pii"] + " - Protection Level: " + cheatsheet[permission.getAttribute("android:name")]["protection-level"]
                infoString = "Description: " + cheatsheet[permission.getAttribute("android:name")]["info"]

                permissions.append({"name": permission.getAttribute('android:name'), "whitelisted": "true", "info": infoString})

            else:
                #if permission not found in cheatsheet, don't pass tooltip info to flask, it should handle it and not generate the tooltip
               # if it wasn't found in the cheatsheet, don't generate tooltip
                # infoString = "Description: " + "no info found" + " - Directly collects PII?: no info found " + " - Protection Level: no info found" 
                infoString = "Description: " + cheatsheet[permission.getAttribute("android:name")]["info"]

                permissions.append({"name": permission.getAttribute('android:name'), "whitelisted": "true", "info": infoString})
        else: 
            #if it wasn't found in the whitelist, save it as whitelisted: false
            # but first, check if it is found in the cheatsheet

            if permission.getAttribute("android:name") in cheatsheet:
                #if so, create a string to pass to flask that will later be the tooltip for this specific permission
                # infoString = "Description: " + cheatsheet[permission.getAttribute("android:name")]["info"] + " - Directly collects PII?: " + cheatsheet[permission.getAttribute("android:name")]["pii"] + " - Protection Level: " + cheatsheet[permission.getAttribute("android:name")]["protection-level"]
                infoString = "Description: " + cheatsheet[permission.getAttribute("android:name")]["info"]

                permissions.append({"name": permission.getAttribute('android:name'), "whitelisted": "false", "info": infoString})

            else:
                #if permission not found in cheatsheet, don't pass tooltip info to flask, it should handle it and not generate the tooltip
                # if it wasn't found in the cheatsheet, don't generate tooltip
                infoString = "Description: " + "no info found" + " - Directly collects PII?: no info found " + " - Protection Level: no info found" 
                permissions.append({"name": permission.getAttribute('android:name'), "whitelisted": "false", "info": infoString})
    

    """
    ----------USES FEATURE---------------
    """

    # Iterate over all the uses-feature nodes
    for permission in manifest.getElementsByTagName('uses-feature'):
        if permission.getAttribute('android:name') in whitelistedHardware:
            tempFeatureNumber += 1

            #save each used feature to the permissions dictionary to generate the report
            features.append({"name": permission.getAttribute('android:name'), "whitelisted": "true"})
            
        else: 
            features.append({"name": permission.getAttribute('android:name'), "whitelisted": "false"})


    """
    ----------SCORING SYSTEM---------------
    """

    featureAndPermission = permissionNumber + featureNumber
    tempFeatureAndPermission = tempPermissionNumber + tempFeatureNumber

    score = featureAndPermission - tempFeatureAndPermission

    print (packageName, '\t\t', score)

    generateReport(packageName, score, permissions, features)

if __name__ == '__main__':
    main()