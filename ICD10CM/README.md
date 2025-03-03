# ICD-10-CM ReadMe

Goal: Parse ICD-10-CM XML files to flat CSV files for easy import into a SQL DB.

# Files

**Tabular** - core file with all of the codes

**Index** - like a book index with term lookup alphabetically.  Lists the base code which then can be referenced in the tabular file

**Neoplasms** - lookup of neoplasms by anatomical site with 6 code columns

**Drug** - alphabetical list of drugs with 6 code columns

**EIndex** - External cause of injuries index


## Source Files
All of the source files were from the public available CDC website/FTP server.

### CDC website
https://www.cdc.gov/nchs/icd/icd-10-cm/files.html

### CDC FTP server
https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Publications/ICD10CM/2025-Update/

### Specifically this file: 
https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Publications/ICD10CM/2025-Update/icd10cm-table-index-April-2025.zip 
(about 20MB)
