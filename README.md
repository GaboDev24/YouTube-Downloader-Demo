# YT Downloader

> Descarga videos y audio de YouTube con una interfaz gráfica limpia y moderna.  
> Desarrollado con Python + CustomTkinter · Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp)

---

## ✨ Características

| Función | Descripción |
|---|---|
| 📥 Descarga de video | Descarga en MP4, en la calidad que elijas (hasta 4K según disponibilidad) |
| 🎵 Descarga de audio | Extrae el audio en MP3 a 192 kbps |
| 🔍 Vista previa | Muestra miniatura, título, canal y duración antes de descargar |
| 📊 Progreso en tiempo real | Barra de progreso con velocidad y tiempo restante |
| 📁 Carpeta personalizable | Elige dónde guardar los archivos |
| 🖱️ Barra de desplazamiento | La interfaz es totalmente scrollable, apta para pantallas pequeñas |
| ✅ Formatos soportados | `youtube.com/watch`, `youtu.be`, `youtube.com/shorts` |

---

## 🖥️ Capturas

> La aplicación tiene un diseño oscuro con acentos en cyan y violet, siguiendo un sistema de diseño moderno.

---

## ⚙️ Requisitos del sistema

- **Python** 3.10 o superior
- **FFmpeg** instalado y disponible en el PATH (necesario para mezclar video + audio y convertir a MP3)
  - Windows: [ffmpeg.org/download.html](https://ffmpeg.org/download.html) o `winget install ffmpeg`
  - Linux: `sudo apt install ffmpeg`
  - macOS: `brew install ffmpeg`

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/yt-downloader.git
cd yt-downloader
```

### 2. Crear un entorno virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
python main.py
```

---

## 📦 Dependencias

Las dependencias están listadas en [`requirements.txt`](./requirements.txt):

```
yt-dlp         # Motor de descarga de YouTube
customtkinter  # Interfaz gráfica moderna (basada en tkinter)
Pillow         # Procesamiento de imágenes (miniaturas)
requests       # Descarga de miniaturas por HTTP
```

Instálalas con:

```bash
pip install -r requirements.txt
```

---

## 🔨 Compilar como ejecutable (.exe)

Puedes empaquetar la aplicación en un solo archivo ejecutable usando [PyInstaller](https://pyinstaller.org):

### 1. Instalar PyInstaller

```bash
pip install pyinstaller
```

### 2. Compilar

```bash
pyinstaller --onefile --windowed --name "YT-Downloader" main.py
```

O usando el `.spec` incluido (que ya recoge todos los assets de CustomTkinter):

```bash
pyinstaller main.spec
```

### 3. Resultado

El ejecutable aparecerá en `dist/YT-Downloader.exe`.

> **Nota:** FFmpeg **no** se incluye en el ejecutable. El usuario final debe tenerlo instalado en el PATH.

---

## 📂 Estructura del proyecto

```
yt-downloader/
├── main.py              # Código principal de la aplicación
├── main.spec            # Configuración de PyInstaller
├── requirements.txt     # Dependencias de Python
├── DESIGN.md            # Sistema de diseño (tokens, paleta, componentes)
├── .gitignore
└── README.md
```

---

## 🎨 Sistema de diseño

La interfaz sigue el **Design System base** documentado en [`DESIGN.md`](./DESIGN.md):

| Token | Valor |
|---|---|
| Acento principal | `#00d4ff` (cyan) |
| Acento secundario | `#8b5cf6` (violet) |
| Fondo profundo | `#0a0a0f` |
| Tarjetas | `#12121e` |
| Texto principal | `#e8e8f0` |
| Tipografía | Segoe UI (sistema) |

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| [Python 3.10+](https://python.org) | Lenguaje principal |
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | Interfaz gráfica moderna |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Motor de descarga |
| [Pillow](https://python-pillow.org) | Procesamiento de imágenes |
| [Requests](https://docs.python-requests.org) | Peticiones HTTP |
| [FFmpeg](https://ffmpeg.org) | Procesamiento de audio/video |

---

## ❓ Preguntas frecuentes

**¿Por qué necesito FFmpeg?**  
yt-dlp descarga el video y el audio por separado en alta calidad, y FFmpeg los combina en un único archivo MP4. Para MP3, FFmpeg extrae el audio del stream descargado.

**¿Funciona con YouTube Shorts?**  
Sí, el programa admite URLs de tipo `youtube.com/shorts/...`.

**¿Puedo descargar listas de reproducción (playlists)?**  
No actualmente. El programa está diseñado para videos individuales.

**¿El ejecutable incluye FFmpeg?**  
No. FFmpeg debe instalarse por separado en el sistema.

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**.  
Úsalo, modifícalo y compártelo libremente.

---

<div align="center">
  Desarrollado con ♥ por <strong>GaboDev</strong>
</div>
