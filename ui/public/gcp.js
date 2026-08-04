// GCP registration view: mark passpoints in registered frames, then compute
// the SfM -> relative-UTM similarity transform via /api/gcp/compute.

let gcpPoints = [];
let gcpFrames = [];
let gcpObs = [];
let gcpSelectedPoint = null;
let gcpCurrentFrame = null;
let gcpImg = null;
let gcpScale = 1;
let gcpOffsetX = 0;
let gcpOffsetY = 0;
let gcpPanning = false;
let gcpPanStart = null;
let gcpReport = null;

function toggleGcpView() {
  const view = $('#gcp-view');
  const hidden = view.style.display === 'none' || !view.style.display;
  view.style.display = hidden ? 'flex' : 'none';
  if (hidden) {
    gcpLoadAll();
  }
}

function closeGcpView() {
  $('#gcp-view').style.display = 'none';
}

async function gcpLoadAll() {
  await Promise.all([gcpLoadPoints(), gcpLoadFrames(), gcpLoadObservations(), gcpLoadReport()]);
  gcpRenderPoints();
  gcpRenderFrames();
  gcpRenderObservations();
  gcpRenderReport();
  if (!gcpSelectedPoint && gcpPoints.length) {
    gcpSelectPoint(gcpPoints[0].gcp_id);
  }
}

async function gcpLoadPoints() {
  try {
    const res = await fetch('/api/gcp/points');
    const data = await res.json();
    gcpPoints = data.points || [];
  } catch (e) { gcpPoints = []; }
}

async function gcpLoadFrames() {
  try {
    const res = await fetch('/api/gcp/frames');
    const data = await res.json();
    gcpFrames = data.frames || [];
  } catch (e) { gcpFrames = []; }
}

async function gcpLoadObservations() {
  try {
    const res = await fetch('/api/gcp/observations');
    gcpObs = await res.json();
  } catch (e) { gcpObs = []; }
}

async function gcpLoadReport() {
  try {
    const res = await fetch('/api/gcp/report');
    if (res.ok) { gcpReport = await res.json(); }
    else { gcpReport = null; }
  } catch (e) { gcpReport = null; }
}

function gcpRenderPoints() {
  const list = $('#gcp-point-list');
  if (!gcpPoints.length) {
    list.innerHTML = '<div class="gcp-muted">Keine Passpunkte. Lade gcp_coordinates.csv nach data/01_raw/ und f&uuml;hre prepare_gcp aus.</div>';
    return;
  }
  list.innerHTML = gcpPoints.map(p => {
    const n = gcpObs.filter(o => o.gcp_id === p.gcp_id).length;
    const active = p.gcp_id === gcpSelectedPoint ? ' active' : '';
    return `<div class="gcp-point${active}" onclick="gcpSelectPoint('${p.gcp_id}')">
      <span class="gcp-point-id">${p.gcp_id}</span>
      <span class="gcp-point-meta">${n} Beob.</span>
    </div>`;
  }).join('');
}

function gcpSelectPoint(gcpId) {
  gcpSelectedPoint = gcpId;
  gcpRenderPoints();
  gcpDraw();
}

function gcpRenderFrames() {
  const list = $('#gcp-frame-list');
  if (!gcpFrames.length) {
    list.innerHTML = '<div class="gcp-muted">Keine registrierten Frames. COLMAP-SfM ausf&uuml;hren (erzeugt sparse_txt).</div>';
    return;
  }
  list.innerHTML = gcpFrames.map(f => {
    const active = f.name === gcpCurrentFrame ? ' active' : '';
    return `<div class="gcp-frame${active}" onclick="gcpLoadFrame('${f.name}')">
      <img class="gcp-thumb" src="${f.thumb}" loading="lazy" onerror="this.style.visibility='hidden'">
      <span class="gcp-frame-name">${f.name}</span>
    </div>`;
  }).join('');
}

async function gcpLoadFrame(name) {
  gcpCurrentFrame = name;
  $('#gcp-current-frame').textContent = name;
  gcpRenderFrames();
  const frame = gcpFrames.find(f => f.name === name);
  const url = frame ? frame.thumb : ('/api/file/data/02_frames/' + encodeURIComponent(name));
  gcpImg = new Image();
  gcpImg.onload = () => { gcpResetView(); gcpDraw(); };
  gcpImg.onerror = () => { gcpImg = null; gcpDraw(); };
  gcpImg.src = url;
}

function gcpResetView() {
  const canvas = $('#gcp-canvas');
  const wrap = $('#gcp-canvas-wrap');
  if (!gcpImg || !wrap) { gcpScale = 1; gcpOffsetX = 0; gcpOffsetY = 0; return; }
  const w = wrap.clientWidth - 8, h = wrap.clientHeight - 8;
  gcpScale = Math.min(w / gcpImg.naturalWidth, h / gcpImg.naturalHeight, 1);
  gcpOffsetX = (canvas.width - gcpImg.naturalWidth * gcpScale) / 2;
  gcpOffsetY = (canvas.height - gcpImg.naturalHeight * gcpScale) / 2;
  gcpDraw();
}

function gcpZoom(factor) {
  const canvas = $('#gcp-canvas');
  const rect = canvas.getBoundingClientRect();
  const cx = rect.width / 2, cy = rect.height / 2;
  const imgX = (cx - gcpOffsetX) / gcpScale;
  const imgY = (cy - gcpOffsetY) / gcpScale;
  gcpScale *= factor;
  gcpOffsetX = cx - imgX * gcpScale;
  gcpOffsetY = cy - imgY * gcpScale;
  gcpDraw();
}

function gcpResizeCanvas() {
  const canvas = $('#gcp-canvas');
  const wrap = $('#gcp-canvas-wrap');
  if (canvas && wrap) {
    canvas.width = wrap.clientWidth - 8;
    canvas.height = wrap.clientHeight - 8;
    gcpDraw();
  }
}

function gcpImgToScreen(u, v) {
  return [u * gcpScale + gcpOffsetX, v * gcpScale + gcpOffsetY];
}
function gcpScreenToImg(x, y) {
  return [(x - gcpOffsetX) / gcpScale, (y - gcpOffsetY) / gcpScale];
}

function gcpDraw() {
  const canvas = $('#gcp-canvas');
  if (!canvas) return;
  if (canvas.width === 0 || canvas.height === 0) gcpResizeCanvas();
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  if (!gcpImg) {
    ctx.fillStyle = '#8b8fa3';
    ctx.font = '14px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Kein Frame geladen', canvas.width / 2, canvas.height / 2);
    return;
  }
  ctx.imageSmoothingEnabled = true;
  ctx.drawImage(gcpImg, gcpOffsetX, gcpOffsetY, gcpImg.naturalWidth * gcpScale, gcpImg.naturalHeight * gcpScale);
  // Overlay marks for the current frame.
  const colors = ['#ff5e5e', '#5e9eff', '#5eff8a', '#ffe45e', '#c45eff', '#5ee0e0'];
  gcpObs.forEach(o => {
    if (o.image_name !== gcpCurrentFrame) return;
    const [sx, sy] = gcpImgToScreen(o.u, o.v);
    const isSel = o.gcp_id === gcpSelectedPoint;
    const color = colors[(gcpPoints.findIndex(p => p.gcp_id === o.gcp_id)) % colors.length] || '#ff5e5e';
    // reprojected position (green) if a report exists
    let reproj = null;
    if (gcpReport) {
      const g = gcpReport.per_gcp.find(g => g.gcp_id === o.gcp_id);
      if (g && g.observations) {
        const rob = g.observations.find(ro => ro.image_name === o.image_name);
        if (rob && rob.reprojected_uv) reproj = rob.reprojected_uv;
      }
    }
    if (reproj) {
      const [rx, ry] = gcpImgToScreen(reproj[0], reproj[1]);
      ctx.strokeStyle = '#45dfa4'; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(rx - 8, ry); ctx.lineTo(rx + 8, ry);
      ctx.moveTo(rx, ry - 8); ctx.lineTo(rx, ry + 8); ctx.stroke();
    }
    ctx.strokeStyle = color;
    ctx.lineWidth = isSel ? 3 : 2;
    ctx.beginPath(); ctx.moveTo(sx - 10, sy); ctx.lineTo(sx + 10, sy);
    ctx.moveTo(sx, sy - 10); ctx.lineTo(sx, sy + 10); ctx.stroke();
    ctx.beginPath(); ctx.arc(sx, sy, isSel ? 7 : 5, 0, 2 * Math.PI); ctx.stroke();
    ctx.fillStyle = color;
    ctx.font = '11px sans-serif'; ctx.textAlign = 'left';
    ctx.fillText(o.gcp_id, sx + 9, sy - 9);
  });
}

function gcpSetupCanvasEvents() {
  const canvas = $('#gcp-canvas');
  if (!canvas || canvas._gcpBound) return;
  canvas._gcpBound = true;
  canvas.addEventListener('mousedown', e => {
    if (e.button === 2 || e.shiftKey) { gcpPanning = true; gcpPanStart = { x: e.offsetX, y: e.offsetY, ox: gcpOffsetX, oy: gcpOffsetY }; }
  });
  canvas.addEventListener('mousemove', e => {
    const [u, v] = gcpScreenToImg(e.offsetX, e.offsetY);
    $('#gcp-cursor').textContent = `u=${u.toFixed(1)} v=${v.toFixed(1)}`;
    if (gcpPanning && gcpPanStart) {
      gcpOffsetX = gcpPanStart.ox + (e.offsetX - gcpPanStart.x);
      gcpOffsetY = gcpPanStart.oy + (e.offsetY - gcpPanStart.y);
      gcpDraw();
    }
  });
  canvas.addEventListener('mouseup', () => { gcpPanning = false; gcpPanStart = null; });
  canvas.addEventListener('mouseleave', () => { gcpPanning = false; gcpPanStart = null; });
  canvas.addEventListener('contextmenu', e => e.preventDefault());
  canvas.addEventListener('wheel', e => {
    e.preventDefault();
    const factor = e.deltaY < 0 ? 1.15 : 0.87;
    const [imgX, imgY] = gcpScreenToImg(e.offsetX, e.offsetY);
    gcpScale *= factor;
    gcpOffsetX = e.offsetX - imgX * gcpScale;
    gcpOffsetY = e.offsetY - imgY * gcpScale;
    gcpDraw();
  }, { passive: false });
  canvas.addEventListener('click', e => {
    if (!gcpImg || !gcpCurrentFrame || !gcpSelectedPoint) return;
    if (gcpPanning) return;
    const [u, v] = gcpScreenToImg(e.offsetX, e.offsetY);
    const frame = gcpFrames.find(f => f.name === gcpCurrentFrame);
    if (frame && (u < 0 || v < 0 || u >= frame.width || v >= frame.height)) return;
    gcpAddObservation(gcpSelectedPoint, gcpCurrentFrame, u, v);
  });
}

async function gcpAddObservation(gcpId, image, u, v) {
  try {
    const res = await fetch('/api/gcp/observation', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ gcp_id: gcpId, image_name: image, u: Number(u.toFixed(3)), v: Number(v.toFixed(3)) })
    });
    const data = await res.json();
    if (!res.ok || data.error) throw new Error(data.error || 'Observation konnte nicht gespeichert werden.');
    gcpReport = null;
    await gcpLoadObservations();
    gcpRenderPoints();
    gcpRenderObservations();
    gcpRenderReport();
    gcpDraw();
  } catch (e) {
    $('#gcp-report').innerHTML = `<div class="gcp-error">Fehler: ${e.message}</div>`;
  }
}

async function gcpDeleteObservation(gcpId, image) {
  try {
    const res = await fetch('/api/gcp/observation', {
      method: 'DELETE', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ gcp_id: gcpId, image_name: image })
    });
    const data = await res.json();
    if (!res.ok || data.error) throw new Error(data.error || 'Observation konnte nicht geloescht werden.');
    if (data.deleted) gcpReport = null;
    await gcpLoadObservations();
    gcpRenderPoints();
    gcpRenderObservations();
    gcpRenderReport();
    gcpDraw();
  } catch (e) {
    $('#gcp-report').innerHTML = `<div class="gcp-error">Fehler: ${e.message}</div>`;
  }
}

function gcpRenderObservations() {
  const list = $('#gcp-obs-list');
  if (!gcpObs.length) {
    list.innerHTML = '<div class="gcp-muted">Noch keine Beobachtungen. W&auml;hle einen Passpunkt und klicke ins Bild.</div>';
    return;
  }
  list.innerHTML = gcpObs.map(o => {
    let reproj = null;
    if (gcpReport) {
      const g = gcpReport.per_gcp.find(g => g.gcp_id === o.gcp_id);
      if (g && g.observations) {
        const r = g.observations.find(ro => ro.image_name === o.image_name);
        if (r) reproj = r.reprojection_px;
      }
    }
    return `<div class="gcp-obs">
      <span class="gcp-obs-gcp">${o.gcp_id}</span>
      <span class="gcp-obs-img" onclick="gcpLoadFrame('${o.image_name}')">${o.image_name}</span>
      <span class="gcp-obs-uv">(${o.u.toFixed(1)},${o.v.toFixed(1)})</span>
      ${reproj !== null ? `<span class="gcp-obs-reproj" title="Reprojektionsfehler">±${reproj.toFixed(1)}px</span>` : ''}
      <button class="gcp-obs-del" onclick="gcpDeleteObservation('${o.gcp_id}','${o.image_name}')">&times;</button>
    </div>`;
  }).join('');
}

async function gcpCompute() {
  const btn = $('#gcp-compute-btn');
  const rep = $('#gcp-report');
  btn.disabled = true; btn.textContent = '⏳ Berechne…';
  rep.innerHTML = '<div class="gcp-muted">Berechne Triangulation + Ähnlichkeitstransformation…</div>';
  try {
    const res = await fetch('/api/gcp/compute', { method: 'POST' });
    const data = await res.json();
    if (data.error) {
      rep.innerHTML = `<div class="gcp-error">Fehler: ${data.error}<br><pre>${(data.stderr || data.stdout || '').slice(0, 800)}</pre></div>`;
    } else {
      gcpReport = data;
      gcpRenderReport();
      gcpRenderObservations();
      gcpDraw();
    }
  } catch (e) {
    rep.innerHTML = `<div class="gcp-error">Request fehlgeschlagen: ${e.message}</div>`;
  } finally {
    btn.disabled = false; btn.textContent = '⚙ Matrix berechnen';
  }
}

function gcpRenderReport() {
  const rep = $('#gcp-report');
  if (!gcpReport) {
    rep.innerHTML = '<div class="gcp-muted">Noch kein Report. Nach Markierung "Matrix berechnen" klicken.</div>';
    return;
  }
  const r = gcpReport;
  const good = (r.total_rmse_m || 0) <= 0.10;
  rep.innerHTML = `
    <div class="gcp-report-row"><b>GCPs verwendet:</b> ${r.num_gcps_used}</div>
    <div class="gcp-report-row"><b>Beobachtungen:</b> ${r.num_observations}</div>
    <div class="gcp-report-row"><b>Skalierung:</b> ${r.scale}</div>
    <div class="gcp-report-row ${good ? 'gcp-ok' : 'gcp-warn'}"><b>Total RMSE:</b> ${r.total_rmse_m} m</div>
    <div class="gcp-report-row"><b>Max. Residuum:</b> ${r.max_residual_m} m</div>
    <div class="gcp-report-sub">Pro GCP:</div>
    ${r.per_gcp.filter(g => g.status === 'ok').map(g => `
      <div class="gcp-report-row"><span>${g.gcp_id}</span>
        <span>reproj ${g.reprojection_rmse_px}px</span>
        <span>${g.fit_residual_m} m</span></div>`).join('')}
    ${r.outliers_dropped && r.outliers_dropped.length ? `<div class="gcp-warn">Ausreißer verworfen: ${r.outliers_dropped.length}</div>` : ''}
    <div class="gcp-muted" style="margin-top:6px">matrix.txt geschrieben nach data/04_sfm/matrix.txt</div>`;
}

document.addEventListener('DOMContentLoaded', () => {
  // Bind canvas events and keep canvas sized once the view is opened.
  const observer = new MutationObserver(() => {
    if ($('#gcp-view').style.display !== 'none') { gcpSetupCanvasEvents(); gcpResizeCanvas(); }
  });
  const view = $('#gcp-view');
  if (view) observer.observe(view, { attributes: true, attributeFilter: ['style'] });
  window.addEventListener('resize', () => { if ($('#gcp-view').style.display !== 'none') gcpResizeCanvas(); });
});
