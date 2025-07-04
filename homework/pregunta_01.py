"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""
import os
import re
import pandas as pd

def pregunta_01():
    base_dir = os.path.dirname(__file__)
    txt_path = os.path.join(base_dir, "..", "files", "input", "clusters_report.txt")
    
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    data_lines = lines[4:]
    
    rows = []
    current_row = None
    
    def parse_first_line(line):

        pattern = r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s*(.*)$"
        match = re.match(pattern, line)
        if not match:
            return None
        
        cluster_str = match.group(1)
        cant_str = match.group(2)
        porc_str = match.group(3)
        palabras_str = match.group(4)
        
        porc_str = porc_str.replace(",", ".")
        porc_float = float(porc_str)
        
        return {
            "cluster": int(cluster_str),
            "cantidad_de_palabras_clave": int(cant_str),
            "porcentaje_de_palabras_clave": porc_float,
            "principales_palabras_clave": palabras_str.strip()
        }
    
    for line in data_lines:
        if not line.strip():
            continue
        
        first_line_data = parse_first_line(line)
        if first_line_data:
            if current_row is not None:
                rows.append(current_row)
            current_row = first_line_data
        else:

            if current_row is not None:
                extra = line.strip()
                current_row["principales_palabras_clave"] += " " + extra

    if current_row is not None:
        rows.append(current_row)

    for r in rows:
        texto = re.sub(r"\s+", " ", r["principales_palabras_clave"]).strip()
        if texto.endswith("."):
            texto = texto[:-1]
        r["principales_palabras_clave"] = texto
    
    df = pd.DataFrame(rows, columns=[
        "cluster",
        "cantidad_de_palabras_clave",
        "porcentaje_de_palabras_clave",
        "principales_palabras_clave"
    ])
    
    return df