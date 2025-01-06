from datetime import datetime

def update_estados(datos,guardar_datos):
    for tema in datos["temas"]:
        for subtema in tema["subtemas"]:
            # Update the estado of subsubtemas
            for subsubtema in subtema["subsubtemas"]:
                deadline = datetime.strptime(subsubtema["deadline"], '%Y-%m-%d')
                delta = (deadline - datetime.today()).days
                
                # Calculate the estado based on the deadline
                if delta >= 30:
                    estado = 1.0
                elif delta >= 0:  # Ensure we handle deadlines in the past
                    estado = delta / 30
                else:
                    estado = 0.0
                
                subsubtema["estado"] = estado
                #print(f"Subsubtema estado: {estado}")

            # Update the estado of subtema
            total_subsubtemas = len(subtema["subsubtemas"])
            if total_subsubtemas > 0:
                subtema["estado"] = sum(subsubtema["estado"] for subsubtema in subtema["subsubtemas"]) / total_subsubtemas
            else:
                subtema["estado"] = 0.0
            #print(f"Subtema estado: {subtema['estado']}")

        # Update the estado of tema
        total_subtemas = len(tema["subtemas"])
        if total_subtemas > 0:
            tema["estado"] = sum(subtema["estado"] for subtema in tema["subtemas"]) / total_subtemas
        else:
            tema["estado"] = 0.0
        #print(f"Tema estado: {tema['estado']}")

    # Save the updated data
    guardar_datos(datos)