const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3000;

// INSTALAR YTDLP EN UN "VENV" DE PYTHON (pip install yt-dlp)
const YTDLP_PATH = path.join(__dirname, 'venv', 'Scripts', 'yt-dlp.exe');
const DOWNLOADS_DIR = path.join(__dirname, 'downloads');

app.use(express.json());
app.use(express.static('public'));

if (!fs.existsSync(DOWNLOADS_DIR)) {
  fs.mkdirSync(DOWNLOADS_DIR);
}

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'index.html'));
});

app.get('/get-file', (req, res) => {
    const fileName = req.query.file;
    const filePath = path.join(DOWNLOADS_DIR, fileName);
    if (fs.existsSync(filePath)) {
        res.download(filePath); 
    } else {
        res.status(404).send('Archivo no encontrado');
    }
});

app.post('/info', (req, res) => {
  const { url } = req.body;
  if (!url) return res.status(400).json({ error: 'URL vacía' });

  const ytdlp = spawn(YTDLP_PATH, [
    '--no-warnings',
    '--no-playlist',
    '-j',
    url
  ]);

  let data = '';
  let errorData = '';

  ytdlp.stdout.on('data', chunk => { data += chunk; });
  ytdlp.stderr.on('data', chunk => { errorData += chunk; });

  ytdlp.on('close', (code) => {
    if (code !== 0 || !data.trim()) {
      console.error("Error de yt-dlp:", errorData);
      return res.status(500).json({ error: 'No se pudo obtener info del video. Verifica el link.' });
    }

    try {
      const info = JSON.parse(data);
      const formats = info.formats
        .filter(f => f.vcodec !== 'none' && f.acodec !== 'none')
        .map(f => ({
          format_id: f.format_id,
          quality: f.format_note || f.resolution
        }));

      res.json({
        title: info.title,
        thumbnail: info.thumbnail,
        formats
      });
    } catch (e) {
      console.error("Error parseando JSON:", e);
      res.status(500).json({ error: 'Error al procesar los datos del video' });
    }
  });
});


// DESCARGA + PROGRESO 
app.get('/download', (req, res) => {
    const { url, format, audioFormat } = req.query;

    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    const fileNameTemplate = `video_${Date.now()}`;
    const args = [
        '--newline',
        '--progress',
        '--print', 'after_move:filepath', 
        '-o', path.join(DOWNLOADS_DIR, `${fileNameTemplate}.%(ext)s`),
        url
    ];

    if (audioFormat) {
        args.splice(2, 0, '-x', '--audio-format', audioFormat);
    } else {
        args.splice(2, 0, '-f', format);
    }

    const ytdlp = spawn(YTDLP_PATH, args);
    let finalPath = '';

    ytdlp.stdout.on('data', data => {
        const line = data.toString();
        
        const match = line.match(/(\d+\.\d+)%/);
        if (match) {
            res.write(`data: {"progress": ${match[1]}}\n\n`);
        }

        if (line.includes(DOWNLOADS_DIR)) {
            finalPath = line.trim();
        }
    });

    ytdlp.on('close', () => {
        const fileName = path.basename(finalPath);
        res.write(`data: {"progress": 100, "file": "${fileName}"}\n\n`);
        res.end();
    });
});

app.listen(PORT, () => {
  console.log(`Servidor en http://localhost:${PORT}`);
});
