async function loadInfo() {
    const url = document.getElementById('url').value;
    if (!url) return alert('Pegá un link');

    const res = await fetch('/info', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
    });

    const data = await res.json();
    if (data.error) return alert(data.error);

    document.getElementById('info').classList.remove('hidden');
    document.getElementById('title').textContent = data.title;
    document.getElementById('thumb').src = data.thumbnail;

    const qualitySelect = document.getElementById('quality');
    qualitySelect.innerHTML = '';

    data.formats.forEach(f => {
        const opt = document.createElement('option');
        opt.value = f.format_id;
        opt.textContent = f.quality;
        qualitySelect.appendChild(opt);
    });

    // CONFIGURACIÓN ÚNICA DE BOTONES
    document.getElementById('videoBtn').onclick = () => {
        const endpoint = `/download?url=${encodeURIComponent(url)}&format=${qualitySelect.value}`;
        startDownload(endpoint);
    };

    document.getElementById('audioBtn').onclick = () => {
        const endpoint = `/download?url=${encodeURIComponent(url)}&audioFormat=mp3`;
        startDownload(endpoint);
    };
}

function startDownload(endpoint) {
    const progressBar = document.getElementById('progress');
    progressBar.classList.remove('hidden');
    progressBar.value = 0;

    const eventSource = new EventSource(endpoint);

    eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        progressBar.value = data.progress;

        if (data.file) {
            eventSource.close();
            window.location.href = `/get-file?file=${encodeURIComponent(data.file)}`;
        }
    };

    eventSource.onerror = () => {
        eventSource.close();
        alert("Error en la descarga. Revisa la consola del servidor.");
    };
}