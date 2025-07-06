import openpyxl

def export_to_excel(data, output_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["File Name", "BPM"])
    for row in data:
        ws.append(row)
    wb.save(output_path)
