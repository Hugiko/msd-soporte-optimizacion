"""Avisos a Discord por webhooks (en segundo plano: nunca bloquea ni detiene el optimizador).

Canales (enlaces en discord_webhooks.json, que NO se sube a GitHub):
  - "top":    UN mensaje con la ficha del mejor diseno, que se EDITA cada vez que hay uno mejor.
  - "arbol":  una imagen nueva del arbol cuando cambia su estructura.
  - "todo":   la ficha de cada diseno calculado (y los avisos importantes).
"""
import os, json, time, queue, threading, datetime

COLORS = {"valido": 0x1A9850, "cerca_del_limite": 0xFDAE61, "descartado": 0xD73027, "fallido": 0x777777,
          "filtrado": 0x9E9E9E, "top": 0x1A9850, "alerta": 0xC0392B, "info": 0x1F6FB5}


class _Null:
    """Sustituto cuando Discord esta desactivado o no hay enlaces: no hace nada."""
    enabled = False

    def __getattr__(self, name):
        return lambda *a, **k: None


class DiscordNotifier:
    enabled = True

    def __init__(self, hooks, state_path, log, prefix="", record_path=None):
        import requests
        self.rq = requests
        self.hooks = {k: v for k, v in hooks.items() if isinstance(v, str) and v.startswith("https://discord")}
        self.state_path = state_path
        self.log = log
        self.prefix = prefix
        self.record_path = record_path          # en las pruebas: guarda los mensajes enviados para borrarlos despues
        self.st = json.load(open(state_path)) if os.path.exists(state_path) else {}
        self.q = queue.Queue()
        self.th = threading.Thread(target=self._loop, daemon=True)
        self.th.start()

    # ------------------------------------------------------------------ envio con limites y reintentos
    def _save(self):
        tmp = self.state_path + ".tmp"
        json.dump(self.st, open(tmp, "w"), indent=1)
        os.replace(tmp, self.state_path)

    def _request(self, method, url, payload, files):
        for attempt in range(6):
            try:
                fh = []
                multipart = {"payload_json": (None, json.dumps(payload), "application/json")}
                for i, path in enumerate(files):
                    f = open(path, "rb"); fh.append(f)
                    multipart[f"files[{i}]"] = (os.path.basename(path), f)
                try:
                    r = self.rq.request(method, url, files=multipart, timeout=60)
                finally:
                    for f in fh:
                        f.close()
                if r.status_code == 429:                      # limite de Discord: esperar lo que pida
                    wait = float(r.json().get("retry_after", 2.0))
                    time.sleep(min(wait, 60) + 0.5)
                    continue
                if r.status_code >= 500:
                    time.sleep(5 * (attempt + 1)); continue
                return r
            except Exception:
                time.sleep(5 * (attempt + 1))
        return None

    def _send(self, channel, payload, files=(), edit_key=None):
        url = self.hooks.get(channel)
        if not url:
            return
        files = [f for f in files if f and os.path.exists(f)]
        payload.setdefault("username", "Optimizador soporte MSD")
        payload["attachments"] = [{"id": i, "filename": os.path.basename(f)} for i, f in enumerate(files)]
        mid = self.st.get(edit_key) if edit_key else None
        r = None
        if mid:                                               # editar el mensaje existente
            r = self._request("PATCH", f"{url}/messages/{mid}", payload, files)
            if r is not None and r.status_code == 404:
                r = None; mid = None
        if not mid:
            r = self._request("POST", f"{url}?wait=true", payload, files)
            if r is not None and r.ok:
                new_id = r.json().get("id")
                if edit_key:
                    self.st[edit_key] = new_id; self._save()
                if self.record_path and new_id:
                    rec = json.load(open(self.record_path)) if os.path.exists(self.record_path) else []
                    rec.append([channel, new_id]); json.dump(rec, open(self.record_path, "w"))
        if r is None or not r.ok:
            code = None if r is None else r.status_code
            self.log(f"  (Discord: no se pudo enviar al canal '{channel}' [codigo {code}]; el optimizador sigue)")

    def _loop(self):
        while True:
            item = self.q.get()
            try:
                self._send(*item)
            except Exception as e:
                self.log(f"  (Discord: {e!r})")
            finally:
                self.q.task_done()

    def flush(self, timeout=90):
        t0 = time.time()
        while not self.q.empty() and time.time() - t0 < timeout:
            time.sleep(0.5)
        time.sleep(1)

    # ------------------------------------------------------------------ mensajes
    def top(self, title, fields, image, footer, url=None):
        emb = dict(title=self.prefix + title, color=COLORS["top"], fields=fields, footer=dict(text=footer),
                   timestamp=datetime.datetime.utcnow().isoformat())
        if url:
            emb["url"] = url
        if image:
            emb["image"] = dict(url=f"attachment://{os.path.basename(image)}")
        self.q.put(("top", dict(embeds=[emb]), [image] if image else [], "top_message_id"))

    def tree(self, image, text):
        emb = dict(title=self.prefix + "Arbol genealogico de la busqueda", description=text, color=COLORS["info"],
                   image=dict(url=f"attachment://{os.path.basename(image)}"),
                   timestamp=datetime.datetime.utcnow().isoformat())
        self.q.put(("arbol", dict(embeds=[emb]), [image], None))

    def design(self, title, cat, fields, description, image):
        emb = dict(title=self.prefix + title, color=COLORS.get(cat, COLORS["info"]), fields=fields,
                   description=description[:1000], timestamp=datetime.datetime.utcnow().isoformat())
        if image:
            emb["image"] = dict(url=f"attachment://{os.path.basename(image)}")
        self.q.put(("todo", dict(embeds=[emb]), [image] if image else [], None))

    def alert(self, text):
        emb = dict(title=self.prefix + "Aviso del optimizador", description=text[:1800], color=COLORS["alerta"],
                   timestamp=datetime.datetime.utcnow().isoformat())
        self.q.put(("todo", dict(embeds=[emb]), [], None))

    def delete_recorded(self):
        """Borra los mensajes enviados durante una prueba (para dejar los canales limpios)."""
        if not self.record_path or not os.path.exists(self.record_path):
            return 0
        n, left, codes = 0, [], {}
        for channel, mid in json.load(open(self.record_path)):
            url = self.hooks.get(channel)
            done = False
            if url:
                for _ in range(8):
                    try:
                        r = self.rq.delete(f"{url}/messages/{mid}", timeout=30)
                    except Exception:
                        time.sleep(3); continue
                    if r.status_code == 429:
                        try:
                            wait = float(r.json().get("retry_after", 2))
                        except Exception:
                            wait = 5.0
                        time.sleep(min(wait, 60) + 0.5); continue
                    codes[r.status_code] = codes.get(r.status_code, 0) + 1
                    done = r.ok or r.status_code == 404          # 404 = ya no existe
                    break
            n += done
            if not done:
                left.append([channel, mid])                      # se conserva para reintentar
            time.sleep(0.6)                                      # no saturar el limite de borrados
        if left:
            json.dump(left, open(self.record_path, "w"))
        else:
            os.remove(self.record_path)
        self.log(f"Discord: borrados {n}; pendientes {len(left)}; codigos {codes}")
        return n


def make(root, top_dir, log, test=False):
    path = os.path.join(root, "discord_webhooks.json")
    cfg = json.load(open(os.path.join(root, "config.json"), encoding="utf-8-sig"))
    if not cfg.get("discord", True) or not os.path.exists(path):
        return _Null()
    try:
        hooks = json.load(open(path, encoding="utf-8-sig"))
        return DiscordNotifier(hooks, os.path.join(top_dir, "discord_estado.json"), log,
                               prefix="[PRUEBA] " if test else "",
                               record_path=os.path.join(top_dir, "discord_mensajes_prueba.json") if test else None)
    except Exception as e:
        log(f"(Discord desactivado: {e!r})")
        return _Null()
