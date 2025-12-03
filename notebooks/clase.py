
import pandas as pd
import matplotlib.pyplot as plt
import missingno as msno
#Cargue un parquet con datos meteorologicos y renombre aceptando un diccionario columnas
class Renombre:
    """Esta clase recibe un parquet con datos meteorologicos y acepta un diccionario para renombrar columnas, regresa el nombre de las columnas, el numero de datos cargados y el rango de fechas del Df
    renombre: recibe un diccionario para cambiar el nombre de las columnas, por defecto:None"""
    def __init__(self, filepath, renombre=None):
        self.data = pd.read_parquet(filepath)
       
        if renombre !=None:
            self.data.rename(columns=renombre, inplace=True)
        
        self.fecha_in = self.data.index.min()
        self.fecha_fin   = self.data.index.max()
        self.columnas = self.data.columns
        print(f"Nombres de columnas:{self.columnas}")
        print(f"Numero de datos cargados: {len(self.data)}")
        print(f"Rango de fechas: {self.fecha_in}, {self.fecha_fin}")

    def view(self, n=366):
        """"Regresa una vista del DF. 
        n: es el número de columnas a visualizar, por defecto: 366"""
        return self.data.head(n)
        
        #GRAFICA CON VALORES MENSUALES QUE MUESTRE EL VALOR PROMEDIO DE UNA COLUMNA, N-VECES LA DESVIACION ESTANDAR, ESPECIFICADO POR EL USUARIO, VISUALICE LOS MAXIMOS Y MINIMOS MENSUALES SI QUIEN USA LA FUNCION LO ESPECIFICA.
    def Mensual(self, columna: str, n:float =1, max_min:bool =False):
        """Genera una grafica mensual de la columna especificada que muestra el promedio mensual
        Parametros:
        columna:(str)
        Nombre de la columna que se desee graficar.
        n: (opcional, float)
        número de veces que se multiplica la desviacion estandar, si no se especifica, por defecto n=1
        max_min: (opcional, bool)
        Por defecto: False. Si es True genera los puntos máximos y minimos mensuales en  la grafica.
        """
        mensual = self.data[columna].resample("ME") 
        prom = mensual.mean()
        desv = mensual.std() * n
        desv_min = prom - desv
        desv_max = prom + desv
        fig, ax = plt.subplots(figsize=(12,4))
        ax.plot(prom.index, prom, 'o-',label = "Promedio Mensual")
        plt.fill_between(prom.index, desv_min, desv_max, alpha=0.2)
        plt.title(f"{columna} Promedio mensual")
        plt.xlabel("Mes")
        plt.ylabel(f"{columna}")
        if max_min:
            maxi= mensual.max()
            mini = mensual.min()
            plt.plot(maxi.index, maxi,  'o',label="Maximo Mensual")
            plt.plot(mini.index, mini, 'o',label = "Minimo Mensual")
        plt.show()

        
#4 - Grafico del Dia 
    def diario(self, columna:str , regresar_df: bool =False, dia_destacado:str =None):
        """Genera una grafica de los valores diarios por hora de la columna especificada. Opcionalmente puede resaltarse un dia particular.
        Parametros:
        columna:(str)
        Nombre de la columna que se desee graficar.
        regresar_df: (opcional, str)
        Por defecto: False. Si es True, regresa un dataframe con las columnas utilizadas en el calculo y filtradas al periodo seleccionado.
        Si es false, solo se muestra la grafica
        dia_destacado= (Opcional, datetime o str)
        Día que se desea resaltar en la grafica, puede ser str en formato "YY-MM-DD", 
        Por defecto: None. Si se especifica un dia, genera una linea color azul en la grafica. Si es None, no se resaltará ningún día
        """
        datos =self.data.copy()
        
        if dia_destacado is not None:
            dia_destacado = pd.to_datetime(dia_destacado).date()
        dias = datos[columna].groupby(datos.index.date)
        fig, ax = plt.subplots(figsize=(12,5))
        if regresar_df:
            return datos[[columna]]
            
        for fecha, serie in dias:
            ejex = serie.index.strftime("%H:%M")
            if dia_destacado is not None and any(serie.index.date == dia_destacado):
                ax.plot(ejex, serie.values,color="blue")
            else:
                ax.plot(ejex, serie.values,color="gray", alpha=0.1)
        plt.xlabel("Hora del dia")
        plt.xticks(plt.xticks()[0][0::12])
        plt.ylabel(f"{columna}")
        plt.title(f"{columna} Diario con enfasis en el dia {dia_destacado}")
        plt.show()

#5 - Heatmap To
    def heatmap(self, columna: str ='To', regresar_df: bool =False):
        """Genera un mapa de calor de la columna especificada. Por defecto, 'To'.
        Parametros:
        columna:(str)
        Nombre de la columna que se desee graficar. Por defecto, columna='To'
        regresar_df: (opcional, bool)
        Por defecto: False. Si es True, regresa un dataframe con las columnas utilizadas en el calculo y filtradas al periodo seleccionado.
        Si es false, solo se muestra el mapa de calor.        
        """
        datos_asfreq = self.data[[columna]].copy()
        mapa_asfreq = datos_asfreq[columna].groupby(
            by=[datos_asfreq.index.month, datos_asfreq.index.hour]
        ).mean().unstack().T
        valormin = mapa_asfreq.min().min()
        valormax = mapa_asfreq.max().max()
        fig, ax = plt.subplots(figsize=(12,4))
        im = ax.imshow(mapa_asfreq, aspect=.2,cmap="jet",vmin=valormin,vmax=valormax)
        cbar = ax.figure.colorbar(im, ax=ax)
        ax.set_ylabel("horas")
        ax.set_xlabel("meses")
        ax.set_title(f"Heatmap de {columna}")
        if regresar_df:
            return self.data[[columna]]
#Radiación
    def radiacion(self, columnas: str =["Ig","Ib","Id"], inicio: str =None, fin: str=None, regresar_df: bool =False):
        """Calcula la energia de cada una de las componentes de la radiacion solar para el periodo de tiempo determinado.
        Parametros:
        columnas:(opcional, str)
        Lista de nombres de las columnas que contienen datos de radiacion
        por defecto: ["Ig", "Ib", "Id"].
        inicio: (opcional, datetime o str)
        Fecha incial del periodo a analizar. Puede ser str en formato "YY-MM-DD", si no se especifica, se usa el inicio del dataframe
        fin: (opcional, datetime o str)
        Fecha final del periodo a analizar. Puede ser str en formato "YY-MM-DD", si no se especifica, se usa el final del dataframe
        regresar_df: (opcional, bool)
        Por defecto: False. Si es True, regresa un dataframe con las columnas utilizadas en el calculo y filtradas al periodo seleccionado.
        Si es false, solo se muestra la grafica
        """
        datos =self.data.copy()
        if inicio is not None:
            datos= datos[datos.index>=pd.to_datetime(inicio)]
        if fin is not None:
            datos= datos[datos.index<=pd.to_datetime(fin)]
        dt_horas = 10/60
        energias ={}
        for col in columnas:
            if col in datos.columns:
                energias[col] = (datos[col].fillna(0).values * dt_horas).sum()
        energia_df = pd.DataFrame(energias, index=["Energia (Wh/m2)"])
        fig, ax = plt.subplots(figsize=(12,4))
        ax.bar(energia_df.columns, energia_df.loc["Energia (Wh/m2)"])
        ax.set_ylabel("Energia (Wh/m2)")
        ax.set_title(f"Energía de radiación solar del {inicio} al {fin}")
        plt.show()
        if regresar_df:
            return datos[columnas]