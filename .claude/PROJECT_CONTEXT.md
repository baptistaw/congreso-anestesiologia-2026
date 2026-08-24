# Contexto del Proyecto - Congreso Anestesiología 2026

## Última sesión
- **Fecha**: 2026-08-24
- **Branch**: main
- **Estado**: funcional, en uso · producción verificada tras migración de backend

## Descripción
Programa interactivo y editable del XXIV Congreso Uruguayo de Anestesiología (12-16 Octubre 2026).
Single-file HTML con CSS y JS inline. Desplegado en GitHub Pages con backend en Cloudflare Workers KV.

## Trabajando en
Nada activo. Próxima tarea: reutilización SAU anual (plataforma reusable año a año) — falta scopear alcance.

## Completado esta sesión (2026-08-24)
- Commit del trabajo pendiente: export PDF/Excel + gestor de formularios genérico + endpoint /kv en el worker + formulario.html (98b51f8)
- MIGRACIÓN DE BACKEND: el worker vivía en una cuenta Cloudflare huérfana (contacto-f4a) sin acceso de deploy. Se redesplegó congresosau-api en la cuenta propia (baptistaw@gmail.com) con KV nuevo, migrando los 65 eventos vía GET público → PUT. Reapuntadas TODAS las URLs (index.html, formulario.html, postulacion.html) a baptistaw.workers.dev (19c8b5b, bf0635c). Backup en backups-agenda/events-prod-20260824.json.
- Timeline mobile: scroll horizontal por día con ancho mínimo 158px por track (gutter de horas fijo); ya no se aplastan las tarjetas. Verificado con capturas headless 390/1280px (92da018)
- Instructores: se cargan self-service vía postulacion.html (los propios instructores se autopostulan y el form escribe a /events); backend corregido tras la migración

## Completado sesiones anteriores
- Guardado automático en Cloudflare Workers KV (sin tokens, sin git push)
- Fix: talleres repetidos AM/PM se alinean en la misma columna del timeline
- Eliminado dependencia de localStorage para persistencia (ahora usa cloud)
- Subtipos de taller con colores diferenciados (Simulación, Habilidades, Disc. Casos, Enfermería)
- Filtro genérico "Todos los Talleres" + filtros por subtipo
- Campos editables: Instructor 1-6, Instructor Asistente 1-4, Técnico en Simulación
- Técnico en Simulación (Lic. Mauricio Castro) por defecto en talleres de simulación
- Protección del modo edición con código numérico (1904)
- Botones de edición ocultos hasta activar modo edición con código
- Fix drag & drop (inline handlers, separación click/drag)
- Vista timeline: eventos posicionados por hora, simultáneos lado a lado
- Separación Pre-Congreso (Sáb, Dom, Lun, Mar) y Congreso (Mié, Jue, Vie) en secciones

## Pendientes inmediatos
- [ ] Reutilización SAU anual: definir alcance (¿programa en blanco / talleres-tipo / instructores frecuentes / plantilla clonable?) y luego implementar
- [ ] (Opcional) Borrar el worker "hello world" o dejar el viejo huérfano — no molesta

## Notas técnicas
- Datos se guardan en Cloudflare Workers KV, NO en localStorage
- Worker: GET/PUT en /events + endpoint genérico GET/PUT /kv/<key> (para formularios: keys "forms" y "resp_<formId>"; key restringida a [A-Za-z0-9_-], límite 900 KB). CORS habilitado, sin auth (protegido por código 1904 en el frontend)
- Hay DOS formularios: postulacion.html (instructores se autopostulan, escribe a /events) y formulario.html (renderer genérico del gestor de formularios, usa /kv). Link instructores: https://baptistaw.github.io/congreso-anestesiologia-2026/postulacion.html
- Timeline mobile: wrapper .day-scroll (overflow-x:auto) entre .day-content y .events-area; gutter fijo afuera; hour-lines dentro de .events-area; CSS var --tracks setea min-width por track
- Código de acceso a edición: 1904 (hardcoded en JS)
- PIXELS_PER_HOUR = 70 para el timeline
- Los eventos usan startHour/endHour como decimales (ej: 8.5 = 08:30)
- assignTracks() usa titleTrackMap para mantener talleres repetidos en la misma columna
- saveData() tiene debounce de 2s para no saturar la API de Cloudflare
- Cuenta Cloudflare: baptistaw@gmail.com (account ID aec1d76775501f6a87f8f7976805096b), subdomain baptistaw.workers.dev, auth via `npx wrangler login`. OJO: el worker original vivía en OTRA cuenta (subdomain contacto-f4a) creada con otro login inaccesible; por eso se migró.
- events.json existe en el repo (creado via GitHub API) pero ya NO se usa; los datos viven en KV

## Ideas capturadas
