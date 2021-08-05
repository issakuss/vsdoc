# How to use Citation Picker for Zotero ("mblode.zotero" and makebib)
1. Open Zotero in remote computer, via VNC.

2. Press Alt + Shift + Z and call the picker.  
The picker will appear in VNC.

3. Edit makebib.md
You will find it in src/filters (you can change the directory if you want).
Replace the LIBRARY_ID, LIBRARY_TYPE, API_KEY, COLLECTION_ID.
You can check your LIBRARY_ID (userID) and create API_KEY here: https://www.zotero.org/settings/keys .
To gain the COLLECTION_ID, open your Zotero web library (https://www.zotero.org/{your user name}/library), select your collection, and find it in the URL.
COLLECTION_ID can be None, but the filter will take a long time to search all of your articles.
LIBRARY_TYPE must be 'user' or 'group'.
SAVE_PATH is relative path from working directory (Makefile's directory) to save .bib file.

4. Use makebib.py as filter
I recommend you use .yaml file as below:

```
filters:
- src/filters/inlini.py
- src/filters/makebib.py
```

## Example
@smallwoodDistinguishingHowWhy2013 says iroiro.
Are ha koudayo [@smallwoodDistinguishingHowWhy2013; @holzelHowDoesMindfulness2011; @tangSpecialIssueMindfulness2013].
Sounano, Majide? [SM\; @smallwoodDistinguishingHowWhy2013]
Un, Majimaji [see @smallwoodDistinguishingHowWhy2013]
Their paper [-@seliAttentionLapseMotorDecoupling2016] introduced arekore.
