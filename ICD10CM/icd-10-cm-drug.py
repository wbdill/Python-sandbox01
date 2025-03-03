import xml.etree.ElementTree as ET
import csv

# Load the XML file
xml_file = "icd10cm-table-index-2025/icd-10-cm-drug-2025.xml"
tree = ET.parse(xml_file)
root = tree.getroot()

# Open a CSV file to write
csv_drugs = "output/ICD10CM_2025_Drugs.csv"

# RowID - maintain original position within the XML file
# Letter
# Level - how many indentations or sub-levels is it with 0 being the parent
# Term - text describing the neoplasm
# SeeAlso - text of the "see" XML tag if it exists for the term
# NonEssModif - Non-essential modifier.  Text of the "nemod" XML tag if it exists for the term
# (remaining fields) - col2 - col7 corresponding to their respective column header.  See the PDF file for desired output

#---------- Codes
with open(csv_drugs, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["RowID", "Letter", "Level", "Term", "SeeAlso", "NonEssModif", "PoisoningAccidental", "PoisoningIntentionalSelfHarm", "PoisoningAssault", "PoisoningUndetermined", "AdverseEffect", "Underdosing"])

    # first row hard coded b/c it's outside of the terms collection
    rowid = 0

    for ltr in root.findall(".//letter"):
        letter = ltr.find("title").text
        for term in ltr.findall(".//mainTerm"):
            rowid = rowid + 1
            cterm = term.find("title").text
            seealso = term.find("seeAlso").text if term.find("seeAlso") is not None else ""
            nonessmodif = term.find("title/nemod").text if term.find("title/nemod") is not None else ""
            level = term.get("level") if term.get("level") is not None else "0"
            col2 = term.find("cell[@col='2']").text if term.find("cell[@col='2']") is not None else ""
            col3 = term.find("cell[@col='3']").text if term.find("cell[@col='3']") is not None else ""
            col4 = term.find("cell[@col='4']").text if term.find("cell[@col='4']") is not None else ""
            col5 = term.find("cell[@col='5']").text if term.find("cell[@col='5']") is not None else ""
            col6 = term.find("cell[@col='6']").text if term.find("cell[@col='6']") is not None else ""
            col7 = term.find("cell[@col='7']").text if term.find("cell[@col='7']") is not None else ""
            writer.writerow([rowid, letter, level, cterm, seealso, nonessmodif, col2, col3, col4, col5, col6, col7])
            
            for subterm in term.findall(".//term"):
                rowid = rowid + 1
                cterm = subterm.find("title").text
                seealso = subterm.find("see").text if subterm.find("see") is not None else ""
                nonessmodif = subterm.find("title/nemod").text if subterm.find("title/nemod") is not None else ""
                level = subterm.get("level")
                col2 = subterm.find("cell[@col='2']").text if subterm.find("cell[@col='2']") is not None else ""
                col3 = subterm.find("cell[@col='3']").text if subterm.find("cell[@col='3']") is not None else ""
                col4 = subterm.find("cell[@col='4']").text if subterm.find("cell[@col='4']") is not None else ""
                col5 = subterm.find("cell[@col='5']").text if subterm.find("cell[@col='5']") is not None else ""
                col6 = subterm.find("cell[@col='6']").text if subterm.find("cell[@col='6']") is not None else ""
                col7 = subterm.find("cell[@col='7']").text if subterm.find("cell[@col='7']") is not None else ""
                writer.writerow([rowid, letter, level, cterm, seealso, nonessmodif, col2, col3, col4, col5, col6, col7])                
        
print(f"Conversion complete! CSV saved as {csv_drugs}")