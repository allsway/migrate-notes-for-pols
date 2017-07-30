# migrate-notes-for-pols
Migrates missed PAID note fields to POLs that were migrated to Alma.  

###### migrate_pol_notes.py
Takes as arguments
   - initialization file config.txt 
   - a csv file of POL note data, in the format 'order record #', 'Note contents':
      
      `"RECORD #(ORDER)","BLOC",
      "o6498577","c"`

Run as `python move_libhas.py config.txt order_notes.csv`

###### config.txt
Configuration setup can be modified in the file config.txt. 
```
[Params]
apikey: apikey 
baseurl: https://api-na.hosted.exlibrisgroup.com
```
