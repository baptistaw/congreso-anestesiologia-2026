# Contexto del Proyecto - Congreso Anestesiología 2026

## Última sesión
- **Fecha**: 2026-03-17
- **Branch**: main
- **Estado**: funcional, en uso

## Descripción
Programa interactivo y editable del XXIV Congreso Uruguayo de Anestesiología (12-16 Octubre 2026).
Single-file HTML con CSS y JS inline. Desplegado en GitHub Pages con backend en Cloudflare Workers KV.

## Trabajando en
Persistencia de datos y alineación de talleres en timeline.

## Completado esta sesión
- Guardado automático en Cloudflare Workers KV (sin tokens, sin git push)
- Worker desplegado: https://congresosau-api.baptistaw.workers.dev (migrado 2026-08-24 desde la cuenta huérfana contacto-f4a.workers.dev, sin acceso de deploy)
- KV namespace ID: 4afd6229e0b4412ab2bfecc50527b921 (cuenta baptistaw@gmail.com, aec1d767…). El viejo (083f37c9…) quedó en la cuenta huérfana.
- Fix: talleres repetidos AM/PM se alinean en la misma columna del timeline
- Eliminado dependencia de localStorage para persistencia (ahora usa cloud)
- Probado y funcionando: editar desde GitHub Pages guarda directo en la nube

## Completado sesiones anteriores
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
- [ ] Llenar instructores en cada taller
- [ ] Revisar que la vista timeline se vea bien en mobile
- [ ] Considerar mejorar la legibilidad de tarjetas angostas cuando hay muchos tracks simultáneos

## Notas técnicas
- Datos se guardan en Cloudflare Workers KV, NO en localStorage
- Worker: GET/PUT en /events, CORS habilitado, sin auth (protegido por código 1904 en el frontend)
- Código de acceso a edición: 1904 (hardcoded en JS)
- PIXELS_PER_HOUR = 70 para el timeline
- Los eventos usan startHour/endHour como decimales (ej: 8.5 = 08:30)
- assignTracks() usa titleTrackMap para mantener talleres repetidos en la misma columna
- saveData() tiene debounce de 2s para no saturar la API de Cloudflare
- Cuenta Cloudflare: baptistaw@gmail.com (account ID aec1d76775501f6a87f8f7976805096b), subdomain baptistaw.workers.dev, auth via `npx wrangler login`. OJO: el worker original vivía en OTRA cuenta (subdomain contacto-f4a) creada con otro login inaccesible; por eso se migró.
- events.json existe en el repo (creado via GitHub API) pero ya NO se usa; los datos viven en KV

## Ideas capturadas
