# Guía de Instalación y Uso

## Pre-requisitos
Asegúrate de tener instalado Python 3.7 o superior en tu sistema. También necesitarás tener instalado git para clonar el repositorio.

## Instalación
1. Primero, clona el repositorio a tu máquina local con el siguiente comando en tu terminal:
   ```
   git clone https://github.com/victormolla14/sitemap-to-chat.git
   ```
2. Navega al directorio del proyecto:
   ```
   cd sitemap-to-chat
   ```
3. Crea un entorno virtual de Python para instalar las dependencias necesarias:
   ```
   python3 -m venv venv
   ```
4. Activa el entorno virtual. En Unix o MacOS, ejecuta:
   ```
   source venv/bin/activate
   ```
   En Windows, ejecuta:
   ```
   .\venv\Scripts\activate
   ```
5. Instala las dependencias del proyecto:
   ```
   pip install -r requirements.txt
   ```
   Si el archivo `requirements.txt` no existe en el repositorio, tendrás que instalar las dependencias manualmente. Basándonos en el código proporcionado, estas son las dependencias necesarias:
   ```
   pip install nest_asyncio python-dotenv
   ```
   Tienes que instalar la biblioteca `langchain` también. Como no está disponible públicamente, tendrás que instalarla manualmente o contactar al propietario del repositorio para obtener más información.

6. Crea un archivo `.env` en la raíz del proyecto y añade tu clave de API de OpenAI de la siguiente manera:
   ```
   OPENAI_API_KEY=your-key-here
   ```

## Uso
Para usar la aplicación, simplemente ejecuta el archivo `main.py` con Python:

```
python main.py
```

Cuando se ejecute el script, te pedirá que introduzcas una URL de sitemap y una pregunta. La URL del sitemap se utilizará para cargar los documentos y la pregunta se utilizará para obtener una respuesta basada en esos documentos.

La primera vez que ejecutes el script con un sitemap en particular, se generará un vectorstore basado en los documentos cargados desde el sitemap y se guardará en un directorio llamado `db`. En ejecuciones posteriores, si el vectorstore ya existe, se cargará desde el disco en lugar de regenerarlo.

## Nota
El código utiliza la biblioteca `langchain` que no está disponible públicamente. Por lo tanto, es posible que encuentres problemas si intentas ejecutar el código tal como está. Te recomendaría ponerse en contacto con el propietario del repositorio para obtener más detalles sobre cómo obtener y utilizar esta biblioteca.


# Funcionamiento

Este proyecto se centra en proporcionar una interfaz de chat que permite realizar consultas y obtener respuestas basadas en los datos de un sitemap proporcionado.

## Código

El código principal de la aplicación se encuentra en `main.py` y utiliza varios módulos y clases para manejar diferentes aspectos de la funcionalidad.

### main.py

```python
import os
from urllib.parse import urlparse
from loader import DocumentLoader
from retrieval_chain import RetrievalChainHandler
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
import nest_asyncio

nest_asyncio.apply()

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
```

El script comienza importando los módulos necesarios y configurando el entorno. Se usa `dotenv` para cargar las variables de entorno, y se aplica `nest_asyncio` para permitir que asyncio se ejecute en los notebooks y en otros contextos donde el loop de eventos ya está en ejecución.

El punto clave aquí es que se establece la clave API para OpenAI usando una variable de entorno, que se usa más adelante en el script para acceder a la funcionalidad de OpenAI.

```python
def main_app(sitemap, query):
    parsed_uri = urlparse(sitemap)
    domain = parsed_uri.netloc

    persist_directory = os.path.join("db", domain)

    documents = None
    if not os.path.exists(persist_directory):
        document_loader = DocumentLoader(sitemap)
        document = document_loader.load_document()

        text_splitter = CharacterTextSplitter(chunk_size=1024, chunk_overlap=64)
        documents = text_splitter.split_documents(document)

        retrieval_chain_handler = RetrievalChainHandler(documents, persist_directory)
        retrieval_chain_handler.generate_vectorstore() # generamos y guardamos el vectorstore
    else:
        retrieval_chain_handler = RetrievalChainHandler(None, persist_directory)

    vectorstore = retrieval_chain_handler.get_vectorstore()

    answer = retrieval_chain_handler.execute_chain(vectorstore, query)
    return answer
```

La función `main_app` se encarga de la lógica principal del script. Toma un sitemap y una consulta como entrada.

El sitemap se analiza para obtener el dominio, que se usa para crear una ruta al directorio de persistencia.

Si el directorio de persistencia no existe, esto significa que los documentos aún no se han cargado para este sitemap. En este caso, se utiliza `DocumentLoader` para cargar los documentos del sitemap y se utiliza `CharacterTextSplitter` para dividir los documentos en fragmentos más pequeños.

Después, se crea un `RetrievalChainHandler` con los documentos y la ruta al directorio de persistencia, y se utiliza para generar un "vectorstore", que es una representación vectorial de los documentos que se puede usar para realizar consultas de información.

Si el directorio de persistencia ya existe, esto significa que los documentos ya se han cargado y el vectorstore ya se ha generado. En este caso, simplemente se crea un `RetrievalChainHandler` sin documentos, ya que los documentos ya están almacenados en el vectorstore.

Finalmente, la función `execute_chain` del `RetrievalChainHandler` se utiliza para realizar la consulta y obtener una respuesta. Esta respuesta luego se devuelve.

### loader.py

El módulo `loader` contiene la clase `DocumentLoader`, que se encarga de cargar documentos desde un sitemap. Usa `SitemapLoader` de la

 biblioteca `langchain` para hacer esto. Se manejan errores durante la carga de documentos.

### retrieval_chain.py

El módulo `retrieval_chain` contiene la clase `RetrievalChainHandler`, que se encarga de varias tareas relacionadas con la gestión y utilización de los documentos y sus representaciones vectoriales.

Genera un vectorstore a partir de los documentos, lo recupera y también maneja la ejecución de la cadena de recuperación, que realiza la consulta real y devuelve una respuesta.


FYI: Este Readme ha sido generado 100% por ChatGPT.