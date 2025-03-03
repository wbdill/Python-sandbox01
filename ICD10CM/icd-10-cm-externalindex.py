import xml.etree.ElementTree as ET
import csv

# Load the XML file
xml_file = "icd10cm-table-index-2025/icd-10-cm-eindex-2025.xml"
tree = ET.parse(xml_file)
root = tree.getroot()

# Open a CSV file to write
csv_externalindex = "output/ICD10CM_2025_ExternalIndex.csv"

# RowID - maintain original position within the XML file
# Letter
# Level - how many indentations or sub-levels is it with 0 being the parent
# Term - text describing the neoplasm
# SeeAlso - text of the "see" XML tag if it exists for the term
# NonEssModif - Non-essential modifier.  Text of the "nemod" XML tag if it exists for the term
# Code

#---------- Codes
with open(csv_externalindex, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["RowID", "Letter", "Level", "Term", "See", "SeeAlso", "NonEssModif", "Code"])

    # first row hard coded b/c it's outside of the terms collection
    rowid = 0

    for ltr in root.findall(".//letter"):
        letter = ltr.find("title").text
        for term in ltr.findall(".//mainTerm"):
            rowid = rowid + 1
            cterm = term.find("title").text
            see = term.find("see").text if term.find("see") is not None else ""
            seealso = term.find("seeAlso").text if term.find("seeAlso") is not None else ""
            nonessmodif = term.find("title/nemod").text if term.find("title/nemod") is not None else ""
            level = term.get("level") if term.get("level") is not None else "0"
            code = term.find("code").text if term.find("code") is not None else ""
            writer.writerow([rowid, letter, level, cterm, see, seealso, nonessmodif, code])
            
            for subterm in term.findall(".//term"):
                rowid = rowid + 1
                cterm = subterm.find("title").text
                see = subterm.find("see").text if subterm.find("see") is not None else ""
                seealso = subterm.find("seeAlso").text if subterm.find("seeAlso") is not None else ""
                nonessmodif = subterm.find("title/nemod").text if subterm.find("title/nemod") is not None else ""
                level = subterm.get("level")
                code = subterm.find("code").text if subterm.find("code") is not None else ""

                writer.writerow([rowid, letter, level, cterm, see, seealso, nonessmodif, code])                
        
print(f"Conversion complete! CSV saved as {csv_externalindex}")