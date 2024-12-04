# BDD-Merlino-TP
TP de Base de datos - Cátedra Merlino

# Backend

El backend esta desarrollado con Flask que interactúa con bases de datos SQLite y MongoDB. Permite realizar operaciones CRUD en ambas bases de datos.  

## Requisitos  

Asegúrate de tener instalados los siguientes componentes en tu sistema:  

- **Python 3.7 o superior**  
- **MongoDB** (Si no lo tienes, puedes instalarlo desde [MongoDB Community Edition](https://www.mongodb.com/try/download/community))  

## Instalación  

### 1. Crea un entorno virtual  

Crea un entorno virtual de python para aislar las dependencias del proyecto:  

```bash  
cd backend
python -m venv venv
venv\Scripts\activate       # En Windows
source venv/bin/activate    # En linux
```
### 2. Instala las dependencias

Con el entorno virtual activado, instala las dependencias del proyecto:

```bash  
pip install -r requirements.txt  
```

## Ejecución

### 1. Inicia MongoDB

Asegúrate de que el servicio de MongoDB esté corriendo.

- En Linux:

```bash  
    sudo service mongod start 
```  

- En Windows, inicia MongoDB mediante la aplicacion de MongoDB Community.

### 2. Ejecuta la aplicación

```bash  
cd src  
python app.py  
```

# Frontend

El backend esta desarrollado con Node.js y el framework Astro.

## Ejecucion

### 1. Ejecutar la aplicacion

Para ejecutar la aplicacion, asegurarse de tener instalado node.js.

Luego pararse en la carpeta ``Front``, ejecutando el comando (o abriendo una terminal en ella):
```
cd Front
```

Posteriormente, instalar las dependencias mediante node.js:
```
npm install
```

Por último, levantar la app:
```
npm start
```
