#!/usr/bin/env python3
"""
Carga instructores, invitados y cronograma interno de los talleres del Congreso
Uruguayo, segun el PDF "TALLERES XXIV CONGRESO URUGUAYO DE ANESTESIOLOGIA 2026"
(Drive 1Qpvsha4K1JTEiV73fWU2XjRZrcOvUQWx), leido el 17/08/2026.

Convencion: los invitados van en `speakers` (la app los muestra como
"Invitados / Ponentes") y el plantel docente en `instructores`.

Uso:  python3 update-talleres-sau-2026-08-18.py entrada.json salida.json
"""
import json
import sys

# El formulario de edicion de la app soporta 6 instructores; no pasar de ahi.
MAX_INSTRUCTORES = 6


def main(src, dst):
    events = json.load(open(src, encoding="utf-8"))
    by_id = {e["id"]: e for e in events}
    log = []

    def touch(eid, **kw):
        e = by_id[eid]
        for k, v in kw.items():
            if e.get(k) != v:
                old = e.get(k)
                if isinstance(old, list) and not old:
                    old = "[]"
                log.append(f"  #{eid} {e['title'][:46]}\n       {k}: {old!r}\n         -> {v!r}")
            e[k] = v

    # ------------------------------------------------- Enfermería: agrupar a 6 slots
    log.append("Enfermería · se agrupan los instructores por módulo (el form admite 6)")
    for eid in (1, 2, 3, 4):
        touch(eid, instructores=[
            "Vía Aérea: Dra. Adriana López · Dra. Julieta Carreño",
            "Seguridad / Humanización: Dra. Beatriz Noya · Dr. Martin Abelleira",
            "RCP: Dra. Lucía Devera · Dra. Andrea Gastelú · Dr. Alexeeivksz Tourn",
        ])

    # ------------------------------------------------- Lunes 12 · PBM
    log.append("Lunes 12 · Sangrado Crítico PBM")
    touch(5, notes=(
        "Cronograma: 8:15-8:30 bienvenida y presentaciones · 8:30-8:45 contenedor seguro · "
        "8:45-9:15 repaso de fundamentos de ROTEM · 9:15-10:30 Módulo 2, taller de "
        "habilidades ROTEM en 3 grupos (A, B, C) · 10:30-11:00 coffee · 11:00-11:10 "
        "introducción a la simulación de alta fidelidad · 11:10-14:00 los 3 grupos rotan "
        "por 3 escenarios · 14:00-14:15 cierre · 14:15-14:30 debriefing de coordinadores "
        "e instructores. Las inscripciones cierran el 12 de setiembre."))

    # ------------------------------------------------- Martes 13 · PoCUS Pediátrica
    log.append("Martes 13 · PoCUS en Anestesia Pediátrica")
    pocus_ped = dict(
        speakers=["Dr. Tiago Rossi (invitado)"],
        instructores=["Dr. Juan Martino", "Dr. Ernesto Balverde",
                      "Dr. Renzo García", "Dra. Mariana Monteiro"],
    )
    touch(6, notes=(
        "4 estaciones: 8:45-9:25 cardiovascular, ecocardiografía básica, hemodinamia y "
        "punciones vasculares (Dr. Martino) · 9:25-10:05 pulmonar, principales patologías "
        "en pediatría (Dr. García) · 10:05-10:35 coffee · 10:35-11:05 valoración de ayuno, "
        "estómago en niños (Dr. Balverde) · 11:05-11:45 regional, raquídea ecoguiada y "
        "bloqueos más frecuentes (Dra. Monteiro)."), **pocus_ped)
    touch(7, notes=(
        "4 estaciones: 14:45-15:25 cardiovascular, ecocardiografía básica, hemodinamia y "
        "punciones vasculares (Dr. Martino) · 15:25-16:05 pulmonar, principales patologías "
        "en pediatría (Dr. García) · 16:05-16:35 coffee · 16:35-17:05 valoración de ayuno, "
        "estómago en niños (Dr. Balverde) · 17:05-17:45 regional, raquídea ecoguiada y "
        "bloqueos más frecuentes (Dra. Monteiro)."), **pocus_ped)

    # ------------------------------------------------- Martes 13 · Cardiovascular
    log.append("Martes 13 · Anestesia Cardiovascular")
    touch(8, instructores=["Dr. Juan Pablo Bouchacourt", "Dra. Julieta Carreño",
                           "Dr. Federico Acquistapace", "Dr. Stefano Fabbiani",
                           "Dr. Juan Carlos Valle Lisboa"],
          notes=("8:00-8:15 acreditaciones, identificación y división en grupos, bienvenida · "
                 "exposiciones · 9:30-10:00 coffee · 12:15-12:30 conclusiones y cierre."))

    # ------------------------------------------------- Miércoles 14 · VORTEX
    log.append("Miércoles 14 · Simulación Crisis en Adultos VORTEX")
    touch(17, speakers=["Dr. Rodrigo Rubio (invitado)"],
          notes=("8:45-9:15 actividad interactiva de repaso de conceptos VORTEX (serious "
                 "games) · 9:15-9:30 pausa · 9:30-12:45 simulación de eventos críticos de "
                 "vía aérea difícil. NOTA: el PDF lista para este grupo solo a Schioppi, "
                 "Cebriá y Lic. Castro; Da Fonte figura en la app pero no en el cronograma "
                 "publicado — confirmar."))
    touch(18, speakers=["Dr. Rodrigo Rubio (invitado)"],
          notes=("14:15-14:45 actividad interactiva de repaso de conceptos VORTEX (serious "
                 "games) · 14:45-15:00 pausa · 15:00-18:15 simulación de eventos críticos "
                 "de vía aérea difícil."))

    # ------------------------------------------------- Jueves 15 · TIVA
    log.append("Jueves 15 · TIVA")
    touch(27, speakers=["Dr. David Ramírez (invitado)"],
          notes=("8:00-8:30 acreditaciones, identificación y división en 4 grupos, "
                 "bienvenida · 8:30-10:00 ¿Cómo elijo mi estrategia de TIVA? (Dr. Ramírez) · "
                 "10:00-10:30 coffee con exposición de bombas de TCI · 10:30-12:45 práctica "
                 "en 4 estaciones: 1) cómo evito errores y eventos adversos, 2) ¿puedo saber "
                 "qué está pasando en el cerebro?, 3) cómo adapto mi TIVA cuando la "
                 "situación es compleja, 4) cirugía con características especiales · "
                 "12:45-13:00 conclusiones y cierre con todo el grupo."))

    # ------------------------------------------------- Jueves 15 · Obstetricia
    log.append("Jueves 15 · Simulación Crítica en Obstetricia")
    touch(28, speakers=["Dr. Mauricio Vasco (invitado)", "Dr. Pablo Santillán (invitado)"],
          instructores=["Dra. Nathalia Araujo", "Dra. Leticia Duarte", "Dra. Andrea Gastelú"],
          notes=("14:00-14:15 acreditaciones, división de grupos, bienvenida y briefing "
                 "general · 14:15-14:30 contenedor seguro · 14:30-15:15 rotación de talleres "
                 "de habilidades: PoCUS en RCP materna, ROTEM (Dr. Vasco) y reanimación · "
                 "15:15-15:45 coffee · 15:45-18:15 escenarios de simulación en simultáneo "
                 "(2 escenarios) · 18:15-18:30 cierre grupal y mensajes para llevarse a casa."))

    # ------------------------------------------------- Chequeos
    problemas = []
    for e in events:
        if len(e.get("instructores") or []) > MAX_INSTRUCTORES:
            problemas.append(f"{e['id']} {e['title']}: {len(e['instructores'])} instructores")

    json.dump(events, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\n".join(log))
    print(f"\nTotal: {len(events)} eventos")
    print("Instructores por encima del límite del formulario:", problemas or "ninguno")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
