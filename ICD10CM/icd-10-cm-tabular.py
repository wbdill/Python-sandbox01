import xml.etree.ElementTree as ET
import csv

# Load the XML file
#xml_file = "icd-10-cm-tabular-2025_ch2.xml"
xml_file = "icd10cm-table-index-2025/icd-10-cm-tabular-2025.xml"
tree = ET.parse(xml_file)
root = tree.getroot()

# Open a CSV file to write
csv_codes    = "output/ICD10CM_2025_codes.csv"
csv_chapters = "output/ICD10CM_2025_chapters.csv"
csv_sections = "output/ICD10CM_2025_sections.csv"

#---------- Codes
with open(csv_codes, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Code", "Description", "ChapterID", "SectionID"])

    # Loop through the XML structure
    for chapter in root.findall(".//chapter"):
        #chapter_name = chapter.find("desc").text if chapter.find("desc") is not None else ""
        chapter_id = chapter.find("name").text if chapter.find("name") is not None else ""
        for section in chapter.findall("section"):
            #section_name = section.find("desc").text if section.find("desc") is not None else ""
            section_id = section.get("id") if section.get("id") is not None else ""
            for code in section.findall(".//diag"):  # get all diag's regardless of how deeply nested
                icd_code = code.find("name").text if code.find("name") is not None else ""
                description = code.find("desc").text if code.find("desc") is not None else ""
                writer.writerow([icd_code, description, chapter_id, section_id])


#---------- Chapters 
with open(csv_chapters, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["ChapterID", "ChapterName"])

    for chapter in root.findall(".//chapter"):
        chapter_name = chapter.find("desc").text if chapter.find("desc") is not None else ""
        chapter_id = chapter.find("name").text if chapter.find("name") is not None else ""
        writer.writerow([chapter_id, chapter_name])

#---------- Sections 
with open(csv_sections, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["SectionID", "SectionName"])

    for chapter in root.findall(".//chapter"):
        for section in chapter.findall("section"):
            section_name = section.find("desc").text if section.find("desc") is not None else ""
            section_id = section.get("id") if section.get("id") is not None else ""
            writer.writerow([section_id, section_name])

print(f"Conversion complete! CSV saved as {csv_codes}")