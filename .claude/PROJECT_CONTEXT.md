# Contexto del Proyecto - Congreso Anestesiología 2026

<!-- ESTADO:INICIO — bloque estructurado que lee el orquestador (Lucy) para el
     seguimiento de proyectos. NO borrar los marcadores ni cambiar los nombres de
     los campos: se parsean. El texto libre del resto del archivo no se toca.
     Está vacío a propósito: lo completa el primer /park, con datos reales. -->
```yaml
esfera: "Trabajo"
objetivo: "Llegar al 12/10 con el programa del XXIV Congreso publicado sin errores y todos los talleres con su equipo de instructores completo"
estado: activo
ultima_actividad: 2026-08-31
proxima_accion: "Cubrir los 8 lugares de instructor que quedaron libres en los 4 Talleres de Enfermeria despues de las bajas"
deadline: 2026-10-12
esperando:
  - de: "Dra. Andrea Gastelu"
    que: "Definicion firme sobre Enfermeria Sesion 3 - avisó que no puede pero dejo abierto 'Si falta gente puedo!'"
    desde: 2026-08-31
```
<!-- ESTADO:FIN -->

## Última sesión
- **Fecha**: 2026-08-31
- **Branch**: main
- **Estado**: funcional, en uso · producción verificada (worker + Pages)

## Descripción
Programa interactivo y editable del XXIV Congreso Uruguayo de Anestesiología (12-16 Octubre 2026).
Single-file HTML con CSS y JS inline. Desplegado en GitHub Pages con backend en Cloudflare Workers KV.

## Trabajando en
Nada activo en código. Lo que sigue es operativo: cubrir los 8 lugares de instructor que quedaron libres en los 4 Talleres de Enfermería tras aplicar las bajas, y resolver el caso de Andrea Gastelú.

## Completado esta sesión (2026-08-31) — cancelar un taller ahora libera el lugar
Reporte de Willy: "las cancelaciones se registran pero el nombre del instructor continúa asignado al taller". 9 casos reales, todos en los 4 Talleres de Enfermería (commit `24abfe3` + backfill de KV).

**Causa raíz** (`postulacion.html`, en `enviar()`): al confirmar `no_puede` el form sólo hacía push a `e.confirmaciones`. Nunca tocaba `instructores`/`coordinators`/`asistentes` ni `faltan`. Lo cosmético era el nombre visible en el programa público; lo grave era el cupo: Sesiones 1 y 2 tenían `faltan=0` con dos cancelaciones cada una, así que postulacion.html anunciaba "Instructores completo" y nadie podía anotarse a un lugar realmente vacío.

Tres problemas, no uno:
- **Auto-baja**: `no_puede` ahora saca a la persona de los tres campos de equipo y suma +1 a `faltan` sólo si estaba en `instructores`. Idempotente para los reintentos del PUT (`saco` viene en false la segunda vez). Además marca su postulación como `baja`: sin eso, al perder el lugar `estadoPostulacion()` la devolvía a PENDIENTE y el comité podía re-aprobar a quien acababa de avisar que no puede.
- **Baja quirúrgica** (`sinPersona()`, gemelo en los dos archivos): una entrada puede empaquetar varias personas bajo una estación — `'RCP: Dra. Andrea Gastelú · Dra. Lucía Devera'`. `quitarDelEquipo()` filtraba la ENTRADA ENTERA con `mismaPersona()`, así que dar de baja a Lucía Devera se llevaba puesta a Andrea Gastelú. Bug latente que se disparaba con el primer uso; 3 de los 9 casos lo tocaban.
- **Alcanzabilidad**: 8 de los 9 casos no tenían postulación (los asignó el comité directo) y el panel de Postulaciones sólo itera `e.postulaciones` → el botón para quitarlos era inalcanzable. Se agregó `cancelacionesPendientes()` + bloque "Avisaron que no pueden, pero siguen asignados" en `showEventDetails()`, con `quitarCancelado()` en un clic.

**Datos de prod**: 8 de 9 corregidos (backup `backups-agenda/events-prod-20260831-185143-pre-cancelaciones.json`, guarda que verifica 65 eventos y que sólo cambien los ids 1-4; verificado post-PUT). Cupos resultantes: S1 `faltan` 0→2, S2 0→1, S3 1→3, S4 1→2.

## Completado esta sesión (2026-08-28) — vista móvil del programa
Reporte de Florencia sobre el link público: "los Talleres de Serious Game solo aparece uno" + "no se actualiza". Un solo reporte, TRES causas independientes; ninguna era de datos (commit 11a6f9f + deploy worker eddb1f4c):
- **Turnos ocultos**: el jueves tiene 7 tracks → `.events-area` mide 7×158=1106px contra 390px de viewport, y el scroll horizontal no tenía ninguna señal visual. Se agregó gradiente en el borde derecho + aviso "→ deslizá para ver más talleres", sólo en mobile y sólo cuando el día desborda de verdad (`marcarDiasConScroll()` mide `scrollWidth` con rAF y re-mide en resize).
- **8 horas vacías**: `getDayTimeRange()` tomaba el mínimo de todos los eventos y `LASRA · BabyBlocks Regional` (id 47) tiene `time:''`/`startHour:0` → el jueves se dibujaba desde las 00:00. Ahora los eventos sin horario salen del timeline a una banda `.day-untimed` arriba del día con el chip "Horario a confirmar".
- **Datos cacheados**: el worker no mandaba `Cache-Control` en `/events` y el `fetch` de index.html no pedía `no-store`. Arreglado en las dos puntas. `postulacion.html` y `formulario.html` ya busteaban caché con `?t=`; index.html era el único que no.

## Completado sesión 2026-08-27 — circuito de postulaciones
- `03758ed` postulacion.html era write-only (reporte de Natalia Freijido: "te anotás y después no figurás"): ahora lee su propio estado, se aprueba desde el programa y discrimina cupos
- `be3a919` panel general de postulaciones + fix de alcanzabilidad (los botones Aprobar/Rechazar estaban gateados por `editMode`, pero en ese modo el clic de la tarjeta va a `editEvent`, no al detalle)
- `e865032` alta manual de postulaciones desde el panel
- `6cf97ac` slots de equipo dinámicos (el form truncaba a 6 instructores) + backup prod
- `cc8e9ce` taller sin cupos de formación ya no genera postulaciones rol "formación" (Enfermería son estaciones de habilidades: todos instructores)
- `4307231` normalización de nombres: la alternancia `dr|dra` dejaba una "a" suelta

## Completado sesión 2026-08-24
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
- [ ] Cubrir los 8 lugares de instructor que quedaron libres en los 4 Talleres de Enfermería (S1: 2, S2: 1, S3: 3, S4: 2)
- [ ] Resolver el caso de Andrea Gastelú (Enfermería Sesión 3): avisó `no_puede` con motivo "Si falta gente puedo!", no es baja limpia. Se dejó asignada a propósito; aparece en el bloque nuevo del detalle con "Quitar y liberar cupo"
- [ ] Reutilización SAU anual: definir alcance (¿programa en blanco / talleres-tipo / instructores frecuentes / plantilla clonable?) y luego implementar
- [ ] (Opcional) Borrar el worker "hello world" o dejar el viejo huérfano — no molesta

## Notas técnicas
- Datos se guardan en Cloudflare Workers KV, NO en localStorage
- **Una entrada de equipo puede empaquetar VARIAS personas** bajo una estación (`'RCP: Dra. Andrea Gastelú · Dra. Lucía Devera'`). Nunca sacar a alguien con `filter(x => !mismaPersona(x, n))`: se lleva puesta a la compañera. Usar `sinPersona()`, que parte por `·`, filtra el tramo y re-prepende la etiqueta de estación. Por lo mismo `instructores.length` NO es la cantidad de cupos ocupados: el bueno es `faltan`, curado a mano
- **`urllib` de Python da 403 contra el worker; `curl` funciona.** Para tocar datos de prod: GET/PUT con curl, Python sólo para transformar
- **Eventos sin horario**: `sinHorario(ev)` = `time` vacío. NO usar `endHour<=startHour` como criterio: hay 3 eventos con duración 0 pero dos (Ceremonia Inaugural 19:00, Entrega de Premios 17:00) sí tienen hora y deben quedarse en el timeline
- **titleTrackMap NO alcanza para alinear turnos**: normalizar la key quitando "(Turno N)" no cambia nada — el track preferido sólo se usa si está libre, y en cada cluster ya está ocupado. Simulado sobre los 65 eventos reales
- **Verificar la vista real**: bajar el index.html de Pages, inyectar los eventos de KV con un `<script>` y sacar `--screenshot` con chrome headless a 390px. OJO: hay 4 ocurrencias de `</body>` (las primeras dentro de template literals del exportador PDF) — inyectar en la ÚLTIMA (`rfind`), si no se rompe el JS y la página renderiza vacía
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
