# CRP File Header
 Type                    |                     | Description                                                                                                                                                 
-------------------------|---------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------
 byte[4]                 | CRP File Signature. | Equal to "CRAP"                                                                                                                                             
 uint16                  | File format version | Currently equals 6.                                                                                                                                         
 pstr                    | Package name        | Encoded using UTF-8.                                                                                                                                        
 pstr                    | Author Name         | The package author's name, encrypted. TODO                                                                                                                  
 uint32                  | Package version     | TODO                                                                                                                                                        
 pstr                    | Main Asset Name     | A string representing the title of the main asset in this package. Encoded using UTF-8.                                                                     
 uint32                  | File Count          | The number of files contained in this package.                                                                                                              
 uint64                  | Data Offset         | The location in this file where the file data starts. This is added to each file's individual offset, and is usually right after the end of the crp header. 
 asset_entry[file_count] | Asset Entries       | A list of asset entries. The length of this list is defined by the File Count above.                                                                        

## Asset Entry
 Type   |          | Description                                                                                                               
--------|----------|---------------------------------------------------------------------------------------------------------------------------
 pstr   | Name     | Name of the asset file. Encoded using UTF-8.                                                                              
 pstr   | Checksum | The asset's checksum, encoded in ASCII hexadecimal. TODO.                                                                 
 uint32 | Type     | This determines what type of asset this is, and how it should be parsed. See the `Asset Types` table below.               
 uint64 | Offset   | The offset, in number of bytes, of where this asset is located in the CRP. This is added to the offset in the CRP header. 
 uint64 | Size     | The size of the file, in bytes.                                                                                           

 ## Asset Types

  Value | Description            
-------|------------------------
 1     | Object                 
 2     | Material               
 3     | Texture                
 4     | Static Mesh            
 50    | Text                   
 51    | Assembly               
 52    | Data                   
 53    | Package                
 80    | Locale                 
 100   | User                   
 101   | Save Game              
 102   | Custom Map             
 103   | Custom Asset           
 104   | Color Correction (LUT) 
 105   | District Style         
 106   | Map Theme              
 107   | Map Theme Map          
 108   | Scenario               

 # Parsing the rest

 With this information we can parse the asset entries using the `parse.py` script into:
 ```json
{
  "Asset Entries": [
    {
      "Checksum": "b321fe84dc6cf13a0f06ca7a092b95f1",
      "Name": "Regal Hills Map - TUTORIAL 1_Data",
      "Offset": 0,
      "Size": 4299928,
      "Type": 52
    },
    {
      "Checksum": "b9bfec90b063d6eedbed9b2eca92f5fc",
      "Name": "Regal Hills Map - TUTORIAL 1_SteamPreview",
      "Offset": 4299928,
      "Size": 222274,
      "Type": 3
    },
    {
      "Checksum": "7af8d8cfca8a9583ce7b30909438db12",
      "Name": "Regal Hills Map - TUTORIAL 1_Snapshot",
      "Offset": 4522202,
      "Size": 91065,
      "Type": 3
    },
    {
      "Checksum": "53618af93c142b9782f7432ff467b273",
      "Name": "Regal Hills Map - TUTORIAL 1",
      "Offset": 4613267,
      "Size": 2048,
      "Type": 101
    }
  ],
  "Author Name": "",
  "Data Offset": 417,
  "File Count": 4,
  "Main Asset Name": "Regal Hills Map - TUTORIAL 1",
  "Package Name": "970134826",
  "Package Version": 0,
  "Signature": "CRAP",
  "Version": 5
}
```
And outputting 4 files:
* `{Main Asset Name}_Snapshot` - Texture
* `{Main Asset Name}_SteamPreview` - Texture
* `{Main Asset Name}_Data` - Data
* `{Main Asset Name}` - Save Game

**From this point on you need to have the necessary types from `ColossalManaged.dll` and `Assembly-CSharp.dll`**

The latter 2 are the ones that matter, we'll focus on the `Save Game` type first.

You can read it using a `BinaryReader`:
- Boolean, can't recall what it's used for
- String, the type (`SaveGameMetaData`)
- String, discarded
- Int32, the item count


Instantiate a new `SaveGameMetaData`


#### Loop over the item count:


Read:
- Boolean, again, can't recall what it's used for
- String, the type
- String, the field name (if the name is `saveRef`, replace with `assetRef`... `saveRef` is legacy... applies to `SystemMapMetaData`, `MapMetaData`, `SaveGameMetadata`)

If the type is an array:
- Read Int32, the size
- Get element type of the type
- Make an array of the element type with the size
- Loop over the size
- - Read & Deserialize and add to array
- Add array to `SaveGameMetaData` instance

If the type is not an array:
- Read & Deserialize
- Add to `SaveGameMetaData` instance

This is not even close to being fully complete or accurate, I haven't even fully parsed it myself

I have:
- achievementsDisabled
- assetRef - needs `{Main Asset Name}_Data`
- assets (not complete! only `ModInfo[]`)
- cash
- cityName
- environment
- getBuildableArea (not correct I think)
- getBuiltin (not correct I think)
- getEnvironment
- getPopulation
- getTags
- getTimeStamp
- imageRef - needs `{Main Asset Name}_Snapshot`
- mapThemeRef
- mods
- population
- steamPreviewRef - needs `{Main Asset Name}_SteamPreview`
- timeStamp

Deserializing and dealing with assets gets kind of annoying... still working on it
