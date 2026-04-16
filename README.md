# Torrent Renamer Tool 🛰️

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Una herramienta potente y sencilla para renombrar archivos `.torrent` utilizando su información interna (metadatos) y el tracker de origen. Ideal para organizar bibliotecas de torrents que tienen nombres crípticos como hashes hexadecimales.

## ✨ Características

- **Renombrado Inteligente**: Extrae el nombre real del contenido desde el interior del archivo torrent.
- **Identificación por Tracker**: Añade el nombre del tracker (ej. `[Tracker 1]`, `[Tracker 2]`) al principio del nombre del archivo.
- **Interfaz Gráfica (GUI)**: Fácil de usar con selector de carpetas y registro de actividad en tiempo real.
- **Modo Simulación**: Permite previsualizar los cambios antes de aplicarlos físicamente en el disco.
- **Ejecutable Independiente**: No requiere instalación de Python para el usuario final (versión `.exe`).
- **Manejo de Duplicados**: Evita colisiones de nombres añadiendo sufijos numéricos automáticamente.

## 🚀 Instalación y Uso

### Opción 1: Usando el Ejecutable (Windows)

1. Ve a la carpeta `dist/`.
2. Ejecuta `torrent_renamer_gui.exe`.
3. Selecciona la carpeta donde están tus archivos `.torrent`.
4. Haz clic en "Iniciar Proceso".

### Opción 2: Desde el Código Fuente (Python)

Si prefieres ejecutarlo manualmente:

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/torrent-renamer.git
   cd torrent-renamer
   ```
2. Instala las dependencias (opcional, solo para recompilar):
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación:
   ```bash
   python torrent_renamer_gui.py
   ```

## 🛠️ Desarrollo y Compilación

Para generar tu propio ejecutable `.exe`:

```bash
pyinstaller --onefile --windowed torrent_renamer_gui.py
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---
Hecho con ❤️ para mejorar la organización de tus archivos.
