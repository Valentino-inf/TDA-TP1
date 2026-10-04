#!/bin/bash

ZIP_NAME="entrega_tp1_grupo_17.zip"

if [ ! -f "informe.pdf" ]; then
    echo "Error: No se encontró el archivo informe.pdf en el directorio actual."
    echo "Asegurate de incluir el informe antes de generar el zip de la entrega."
    exit 1
fi

echo "Generando $ZIP_NAME..."

# Eliminar zip anterior si existe
if [ -f "$ZIP_NAME" ]; then
    rm "$ZIP_NAME"
fi

# Generar el zip excluyendo archivos y carpetas que no son código fuente ni el informe
zip -r "$ZIP_NAME" . \
    -x "*.git*" \
    -x "*.venv*" \
    -x "*.idea*" \
    -x "*__pycache__*" \
    -x "*.gitignore" \
    -x "*enunciado.pdf" \
    -x "*generar_entrega.sh" \
    -x "$ZIP_NAME" \
    -x "pruebas/resultados/*" \
    -x "pruebas/resultados"

if [ $? -eq 0 ]; then
    echo "¡Entrega generada con éxito en $ZIP_NAME!"
else
    echo "Error al generar el archivo zip."
    exit 1
fi
