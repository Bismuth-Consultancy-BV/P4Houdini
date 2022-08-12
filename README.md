# P4Houdini
![P4Houdini Banner](https://github.com/AMTA-Consultancy/P4Houdini/blob/main/misc/images/P4Houdini_Plugin.jpg)
Perforce Plugin for Houdini developed by AMTA Holding BV, Paul Ambrosiussen.

[![](https://img.shields.io/badge/twitter-%230077B5.svg?style=for-the-badge&logo=twitter)](https://twitter.com/ambrosiussen_p)
[![](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/paulambrosiussen/)

You can join the Discord to chat about the plugin: https://discord.gg/rKr5SNZJtM
By using the plugin or any of its contents, you are agreeing to the EULA and Terms of Service.

Please note that the plugin is currently offered to the beta-testers only, and not meant for re-distribution to others. (Except for others within your studio) The intention is to offer this plugin as a paid solution to a wider audience in the future.

## Aquiring a License
If you are an individual and want a node-locked license, you can simply purchase a license on Gumroad here: https://ambrosiussen.gumroad.com/l/p4houdini

If you are a studio and want access on multiple machines, please contact me at paul@ambrosiussen.com

## Important information about Houdini & Perforce!
Please make sure your hip and hda files that get submitted to perforce are marked as binary files and not text files!!
Hip and HDAs not marked as binary will not properly version on perforce, and will corrupt your files. (This has nothing to do with the plugin)
For more information on filetypes, see: https://www.perforce.com/manuals/p4sag/Content/P4SAG/defining-filetype-with-p4-typemap.html


## Installing for Houdini
To install the plugin for the first time, follow these steps:
1. Clone this repository and make note of the directory you have cloned it to.
2. Copy the `P4Houdini.json` file found in the repository root, and paste it in the $HOUDINI_USER_PREF_DIR/packages/ folder.
3. Edit the `P4Houdini.json` file you just pasted, and modify the `$P4HOUDINI` path found inside. Set the path to where you cloned the repository to in step one.
4. Launch Houdini and open the `P4Houdini` shelf. Click the `Install P4` shelf button. Restart Houdini once complete. If you are experiencing any issues in this step please see the troubleshooting section.
5. Set the depot by pressing the `Set Depot` shelf button. Browse to the root folder of your repo and hit accept. Additionally you can also manually set the path in the `P4Preferences.json` file. The variable to set is `P4Client_Root`.
6. Press the Activate License shelf tool and enter your license key (Site or Gumroad) to generate a p4houdini.license file.

## Configuring a P4 Repository
The plugin makes use of P4TICKETS. This means that it wil make use of already validated and authenticated sessions from the Perforce Visual Client. These tickets are valid by default for 12 hours. If the plugin has authentication issues, try logging in on P4V again. 
If you want to connect to a different depot / server using the plugin, you can configure to do so using P4CONFIG. There are two methods:
1. Create a `p4config.txt` in your repository root, or 2. Create a `.p4config` file.
The `p4config.txt` should contain the following data. Notice the [ ] sections. You should replace them with your data:

Remote Server:
```
P4IGNORE=p4ignore.txt
P4INITROOT=$configdir
P4PORT=[YOUR PERFORCE SERVER. EXAMPLE: ssl:perforce:1666]
P4CLIENT=[YOUR WORKSPACE NAME]
```

Local / Personal Server: (Windows)
```
P4IGNORE=p4ignore.txt
P4INITROOT=$configdir
P4PORT=rsh:DVCS/p4d.exe -i -J off -r "$configdir\.p4root"
P4CLIENT=[YOUR WORKSPACE NAME]
```

Local / Personal Server: (Linux)
```
P4IGNORE=p4ignore.txt
P4INITROOT=$configdir
P4PORT=rsh:/bin/sh -c "umask 077 && exec [~/Downloads/p4v-2022.2.2304646/lib/P4VResources/DVCS/p4d] -i -J off -r '"$configdir/.p4root'"
P4CLIENT=[YOUR WORKSPACE NAME]
```


It might be that for your specific perforce configuration you need different / additional settings. You can read about those here: https://www.perforce.com/manuals/cmdref/Content/CmdRef/P4CONFIG.html

## Using the Plugin
More detailed overview: https://www.ambrosiussen.com/p4houdini

- (Automatic) checking out and adding of hip files. (Triggers when saving a file)
- (Automatic) checking out and adding of hda files. (RMB menu when clicking on HDA)
- Submitting (partial) changelists from inside Houdini. (See shelf tool)
- Editing pending Changelists.
- Reverting HIP and HDAs to the latest version found on the repository.
- Check out files specified in any string parm using RMB Click > P4Houdini > Add/Checkout.
- Scanning hip file for files that are being written to, and allowing users to add or 
  check them out automatically preventing any permission errors during cook. Now also supporting $F expressions.
- Modify or set the description of a new or existing changelist while adding/checking out files
  as well as during submit.
- Make files writeable by RMB clicking items in the dialog that shows up when saving / adding one or multiple files.
- You can also automatically add files on ROPs using post-render scripts. 
  Check out the `examples/manual_managing_files.hip` for an example. You will see that the pre-frame and post-write parms have python expression in it which will ensure all files get checked out pre-write, or get added to the changelist after creation.


**Enable the P4Houdini shelf!**

![P4Houdini Shelf](https://github.com/AMTA-Consultancy/P4Houdini/blob/main/misc/images/P4Houdini_Shelf.jpg)

Click the `Set Depot` shelf tool to switch the plugin to your Perforce repository root.

The plugin root has a file called `P4Preferences.json`, which contains some settings you can configure.
`P4Client_Root` - This is the root of your Perforce depot. You can either edit the path here, or use the `Set Depot` shelf tool.
`P4CL_Default` - Allows you to set a default changelist name that will get added to the dropdown menu when selecting a changelist.
`P4Updates` - This dictionary contains booleans for automatic triggers that will happen when using Houdini. Setting these to false will no longer automatically
trigger the plugin to issue Perforce commands when for example saving a file. This allows you to for example have a purely manual workflow.

More features are being developed based on user requests. Please send me an email at paul@ambrosiussen.com, or open an issue here on Github.


## Troubleshooting
If you have an issue, either send me an email at paul@ambrosiussen.com, or open an issue here on Github.

## Privacy Statement
The plugin locally validates itself against information from sesictrl, as well as some host machine information. For non-site licenses, the plugin also validates the license periodically through the Gumroad API. In no cases does the plugin ever submit any of the aforementioned information to any online server. All information is kept locally in the generated encrypted license file. 

## DISCLAIMERS
Perforce and the API used by the plugin is owned and developed by Perforce Software, Inc. https://www.perforce.com/

Houdini is owned and developed by SideFX. https://www.sidefx.com/

## API

```
FUNCTIONS
    check_perforce_installed()
        Returns whether or not P4 dependencies are installed.
    
    file_checkout(file)
        Prompts the user to check out the specified file.
    
    file_edit_changelist(file)
        Prompts the user to edit the changelist belonging to the specified file.
    
    file_revert(file)
        Reverts the specified file to the state found on the depot.
    
    hda_after_save_automatic(file)
        Prompts the user to either check out or add the HDA definition
        after hitting save. It only does this if the plugin preferences
        have this enabled. This is used by event callbacks in pythonrc.py
    
    hda_revert(node)
        Reverts the specified node definition to what is found on the depot.
        Also matches the specified node instance to that.
    
    hip_after_save_automatic()
        Prompts the user to either add the HIP
        after hitting save. It only does this if the plugin preferences
        have this enabled. This is used by event callbacks in pythonrc.py
    
    hip_before_load_automatic()
        Automatically check if the file that is to be loaded is the latest version.
        If not it will prompt for an update. This is used by event callbacks in pythonrc.py
        NOTE: CURRENTLY NOT USED BECAUSE OF A BUG IN HOUDINI CAUSING A FREEZE.
    
    hip_before_save_automatic()
        Prompts the user to check out the HIP
        right before the file gets saved. This prevents any permission
        errors due to file locks. It only does this if the
        plugin preferences have this enabled.
        This is used by event callbacks in pythonrc.py
    
    hip_checkout_dependencies()
        Crawl through all nodes found in the currently open HIP file,
        and check if its node type name is found in the P4NodeCheckouts.json file.
        If it is, it will look for files in the P4NodeCheckouts.json parameters marked as write.
    
    hip_checkout_manual()
        Prompts the user to check out the currently open HIP file.
    
    hip_revert()
        Prompts the user to revert the currently open HIP file
        to the state it is on the depot. It will also
        reload the hip file automatically.
    
    node_file_automatic(node)
        For the given node, check out or add all files found in the known
        parameters described in P4NodeCheckouts.json
    
    submit_dialog()
        Prompts the user with the P4Houdini submit dialog.
```
