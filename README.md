# Proyecto final

- No usen chatgpt
- Crea un fork de este repositorio y agregale _nombre donde nombre es tu nombre para que puedas entregar la liga del repositorio.
- Los datos se encuentran en el link: https://drive.google.com/drive/folders/106hrTwEGPvbAWKYNCwP-Dw90nLCwrF0V?usp=sharing , selecciona un año y que no se repita entre tus compañeros.


## Fecha de entrega

3 de diciembre, miércoles, 4 pm


Para el proyecto final tendrás que realizar lo siguiente:

1. Limpiar el conjunto de datos de un año meteorológico del IER:
    - Importar los datos con tipos adecuados y fecha en formato datetime y en indice
    - Identificar datos faltantes
    - Exportar en formato parquet
    - Documentar proceso de importación, limpiza

2. Crear una clase que haga lo siguiente:
    - Cargue un parquet con datos meteorologicos y renombre aceptando un diccionario columnas de acuerdo a lo siguiente:
        - Ig para la radiación solar global
        - Id para la radiación solar difusa
        - Ib para la radiación solar directa
        - ws para wind speed
        - wd para dirección del viento
        - To para la temperatura exterior
        - rh para la humedad relativa
        - P para la presión atmosférica
    - Cargue los datos y guarde como una propiedad el inicio y final de los datos
    - reporte la cantidad de datos al cargarlos
    - tenga una propiedad llamada "columnas" que regrese las columnas con el nombre que tengan

3. Tenga un método que:
    - Haga una gráfica con valores mensuales que de una columna muestre:
        - valor promedio 
        -  n-veces la desviación estándard, especificada por quien usa la función, con un default n=1
        - visualice los valores máximos y mínimos mensuales si quien usa la función lo especifica, default no
    
4. Tenga un método que:
    - Visualice en el intervalo de un dia, una linea por cada día que contenga la serie temporal de la columna seleccionada por quien usa la función
    - regrese, si lo especifica quien usa la función, la serie temporal en un df con el indice como datetime 
    

5. Tenga un método que:
    - Visualice un mapa de calor de la columna especificada y que por default sea la temperatura To
    - regrese, si lo especifica quien usa la función, la serie temporal un df de los datos

6. Tenga un método que:
    - Calcule la energía de cada una de las componentes de la radiación solar para todo el periodo de tiempo del conjunto de datos o de un periodo específico si se indica, mediante los argumentos "inicio", "fin"
    - Regrese un dataframe si se especifica
    - Haga una gráfica de barras de las componentes de la radiación solar del periodo especificado e indique el periodo en la gráfica

7. Documentado con instrucciones por función, tipado y con una narrativa adecuada

8. Documentado en github utilizando uv, con un conjunto de datos que no sobrepase los 100 MB por archivo y publico

    
9. La clase debe estar implementada como un paquete local



