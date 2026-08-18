#!/usr/bin/env python3
"""
Actualiza la agenda del congreso con los cronogramas oficiales publicados en
congresoanestesiologia.uy (PDFs de Drive), leidos el 17/08/2026.

Cambios:
  A. Talleres de Enfermeria: horarios 08:00-12:00 / 14:00-18:00 + coord/cupos/instructores
  B. Modulo 10 Posters: se parte en Posters LASRA (14:30-15:30) y Posters CUA (15:30-16:30)
  C. Programa LASRA completo: modulos, talleres Regional 1-4, Cafes con Expertos,
     Live Demonstration, con salas reales (Salon LASRA / Salon Anexo / Caballerizas)
  D. Se fusionan los duplicados del Taller de Simulacion en Anestesia Regional (viernes 16)
  E. Se eliminan los contenedores genericos "Cafe con Expertos" y "Talleres de
     Anestesia Regional", reemplazados por sus eventos concretos

Uso:  python3 update-lasra-2026-08-17.py entrada.json salida.json
"""
import json
import sys

SALON = "Salón LASRA (Chacra Lacrosse)"
ANEXO = "Salón Anexo LASRA (Chacra Lacrosse)"
CABALLERIZA = "Caballeriza (Chacra Lacrosse)"
SIM_SAU = "Centro de Simulación SAU – Av. Bolivia 2000"

DAY_LABELS = {
    "sabado": "Sábado 3/10",
    "domingo": "Domingo 4/10",
    "lunes": "Lunes 12/10",
    "martes": "Martes 13/10",
    "miercoles": "Miércoles 14/10",
    "jueves": "Jueves 15/10",
    "viernes": "Viernes 16/10",
}

NOTA_CAFE = ("Café con Expertos: duración 1 h, grupos muy reducidos. "
             "Horario tomado de la grilla del programa LASRA — confirmar con organización.")
NOTA_REGIONAL = ("Taller rotativo: 5 estaciones de 30 min. Los instructores por estación "
                 "están publicados en el PDF 'Talleres LASRA' pero la grilla no permite "
                 "asignarlos con certeza — cargar a mano tras revisar el PDF.")


def hours(time_str):
    """'08:30-13:00' -> (8.5, 13.0). '' -> (0, 0)."""
    if not time_str:
        return 0, 0
    parts = time_str.split("-")

    def to_f(t):
        h, m = t.strip().split(":")
        return int(h) + int(m) / 60

    start = to_f(parts[0])
    end = to_f(parts[1]) if len(parts) > 1 else start
    return start, end


def ev(eid, day, time, title, etype, location, coordinators=None, speakers=None,
       cupos="", notes="", instructores=None, tecnico=""):
    start, end = hours(time)
    return {
        "id": eid,
        "day": day,
        "dayLabel": DAY_LABELS.get(day, "LASRA · a confirmar"),
        "time": time,
        "startHour": start,
        "endHour": end,
        "title": title,
        "type": etype,
        "location": location,
        "coordinators": coordinators or [],
        "speakers": speakers or [],
        "cupos": cupos,
        "notes": notes,
        "instructores": instructores or [],
        "asistentes": [],
        "tecnicoSim": tecnico,
    }


def main(src, dst):
    events = json.load(open(src, encoding="utf-8"))
    by_id = {e["id"]: e for e in events}
    log = []

    def touch(eid, **kw):
        e = by_id[eid]
        for k, v in kw.items():
            if k == "time":
                e["startHour"], e["endHour"] = hours(v)
            if e.get(k) != v:
                log.append(f"  #{eid} {e['title'][:45]!r}: {k}: {e.get(k)!r} -> {v!r}")
            e[k] = v
        if "day" in kw:
            e["dayLabel"] = DAY_LABELS.get(kw["day"], e["dayLabel"])

    # ---------------------------------------------------------------- A. Enfermería
    log.append("A. Talleres de Enfermería")
    enf_instructores = [
        "Dra. Adriana López (Vía Aérea)",
        "Dra. Julieta Carreño (Vía Aérea)",
        "Dra. Beatriz Noya (Seguridad / Humanización)",
        "Dr. Martin Abelleira (Seguridad / Humanización)",
        "Dra. Lucía Devera (RCP)",
        "Dra. Andrea Gastelú (RCP)",
        "Dr. Alexeeivksz Tourn (RCP)",
    ]
    nota_enf_am = ("Acreditaciones 07:30-08:00. Bienvenida 08:00-08:10. "
                   "Módulo 1 08:10-09:20, Módulo 2 09:25-10:35, coffee 10:35-10:45, "
                   "Módulo 3 10:45-11:55, cierre 11:55-12:00. "
                   "Grupos A (17) / B (17) / C (16) rotan por Vía Aérea (subsuelo), "
                   "RCP (primer piso) y Seguridad-Humanización (planta baja).")
    nota_enf_pm = ("Acreditaciones 13:30-14:00. Bienvenida 14:00-14:10. "
                   "Módulo 1 14:10-15:20, Módulo 2 15:25-16:35, coffee 16:35-16:45, "
                   "Módulo 3 16:45-17:55, cierre 17:55-18:00. "
                   "Grupos A (17) / B (17) / C (16) rotan por Vía Aérea (subsuelo), "
                   "RCP (primer piso) y Seguridad-Humanización (planta baja).")
    for eid, time, nota in ((1, "08:00-12:00", nota_enf_am), (2, "14:00-18:00", nota_enf_pm),
                            (3, "08:00-12:00", nota_enf_am), (4, "14:00-18:00", nota_enf_pm)):
        touch(eid, time=time, location="Sede SAU – Av. Bolivia 2000",
              coordinators=["Dra. Leticia Duarte"], cupos="máx. 50",
              instructores=enf_instructores, notes=nota)

    # ---------------------------------------------------------------- B. Pósters
    log.append("B. Módulo 10 · Pósters (se parte en dos sesiones)")
    touch(38, time="14:30-15:30",
          title="Módulo 10 · Presentación de Pósters – XXIII Congreso Internacional LASRA",
          coordinators=["Comité Científico"])

    # ---------------------------------------------------------------- C/D. LASRA existentes
    log.append("C. Talleres LASRA que estaban 'a confirmar'")
    touch(43, day="jueves", time="08:30-11:30", location=CABALLERIZA,
          notes="5 estaciones de 30 min (180 min en total). La web publica 'Jueves 14', "
                "pero el 14 es miércoles: se toma jueves 15 según el programa LASRA.")
    touch(44, day="viernes", time="08:00-13:00", location=SIM_SAU,
          title="LASRA · Taller de Simulación en Anestesia Regional",
          notes="Fusiona el evento duplicado que estaba como 'Taller Simulación Crítica en "
                "Anestesia Regional'. ATENCIÓN: la grilla de Talleres LASRA publica "
                "14:30-18:30 para este taller — confirmar horario.")
    touch(45, day="jueves", time="14:00-17:00", location=CABALLERIZA)
    touch(46, day="viernes", time="14:00-17:00", location=CABALLERIZA)
    touch(47, day="jueves", time="", location=CABALLERIZA,
          notes="Idiomas: inglés, español y portugués. El programa LASRA lo ubica el "
                "jueves 15 en el bloque de mañana; horario exacto a confirmar.")
    touch(48, day="miercoles", time="14:00-17:00", location=CABALLERIZA)

    # ---------------------------------------------------------------- E. Bajas
    borrar = {40, 41, 42}
    for eid in sorted(borrar):
        log.append(f"E. Se elimina #{eid} {by_id[eid]['title']!r} (reemplazado por eventos concretos)")
    events = [e for e in events if e["id"] not in borrar]

    # ---------------------------------------------------------------- F. Altas
    nid = max(e["id"] for e in events) + 1

    def add(*a, **kw):
        nonlocal nid
        e = ev(nid, *a, **kw)
        events.append(e)
        log.append(f"  + #{nid} {e['dayLabel']} {e['time'] or '(s/h)':<11} {e['title']}")
        nid += 1

    log.append("F. Eventos nuevos")

    # Pósters CUA (segunda mitad del módulo 10)
    add("viernes", "15:30-16:30",
        "Módulo 10 · Presentación de Pósters – XXIV Congreso Uruguayo de Anestesiología",
        "poster", "Salón Principal", coordinators=["Comité Científico"])

    # --- Módulos LASRA
    add("miercoles", "08:30-13:00", "LASRA · Módulo Anestesia Regional", "conferencia", SALON,
        coordinators=["Dr. Gonzalo Irizaga"],
        speakers=["Dra. Anahí Perlas", "Dr. Fernando Altermatt", "Dr. Philip Peng",
                  "Dra. Sidonia Suazo", "Dra. Daniela Bravo", "Dr. Hipólito Labandeyra",
                  "Dra. Rous Atton", "Dr. Juan Carlos de la Cuadra"],
        notes="Acreditaciones 08:00-08:30. Inauguración 08:30-09:00. Coffee 10:30-11:00. "
              "Panel interactivo de preguntas 12:40-13:00.")
    add("miercoles", "14:30-18:30", "LASRA · Módulo Obstetricia", "conferencia", SALON,
        coordinators=["Dra. Gabriela Castro"],
        speakers=["Dra. Andrea Gastelú", "Dr. Mauricio Vasco", "Dra. Anahí Perlas",
                  "Dra. Leticia Duarte"],
        notes="Coffee 16:30-17:00. Paneles interactivos 16:00-16:30 y 18:00-18:30.")
    add("jueves", "08:30-13:00", "LASRA · Módulo Medicina del Dolor", "conferencia", SALON,
        coordinators=["Dr. Pablo Castromán", "Dra. Marta Surbano"],
        speakers=["Dra. María Eugenia Seijas", "Dra. María Patricia González",
                  "Dr. Olympio Chacon", "Dr. Andrés Rocha", "Dr. Eduardo Vega",
                  "Dr. Philip Peng"],
        notes="Coffee 10:30-11:00. Panel interactivo de preguntas 12:30-13:00.")
    add("jueves", "14:30-18:30", "LASRA · Módulo PoCUS", "conferencia", SALON,
        coordinators=["Dra. Paola Alcarraz"],
        speakers=["Dr. Alejandro Corujo", "Dr. Tiago Rossi", "Dra. Anahí Perlas",
                  "Dr. Oscar Ledezma"],
        notes="Coffee 16:30-17:00.")
    add("viernes", "08:30-13:00", "LASRA · Módulo Pediatría", "conferencia", SALON,
        coordinators=["Dra. Carolina de León"],
        speakers=["Dr. Julio Lapalma", "Dr. Walid Alrayashi", "Dra. Deepa Kattail",
                  "Dr. Can Aksu", "Dr. Vinícius Quintão", "Dr. John Hagen"],
        notes="Acreditaciones 08:00-08:30. Coffee 10:30-11:00. Paneles interactivos "
              "de preguntas al cierre de cada bloque.")
    add("viernes", "14:00-16:30", "LASRA · Anestesia Regional – Live Demonstration",
        "conferencia", SALON, coordinators=["Dr. Gonzalo Irizaga"],
        speakers=["Dra. María Patricia González", "Dr. Hipólito Labandeyra",
                  "Dra. Daniela Bravo", "Dr. José Ramón Saucillo", "Dra. Rous Atton"],
        notes="Demostración en vivo. 14:00 mama (González) · 14:20 clavícula (Labandeyra) · "
              "14:40 preservadores de diafragma (Bravo) · 15:00 cuadrado lumbar (Saucillo) · "
              "15:20 preservadores de rodilla (Saucillo) · 15:40 preservadores de cadera "
              "(Atton) · 16:00-16:30 panel.")

    # --- Talleres Regional 1-4
    for dia, hora, nombre, extra in (
        ("miercoles", "14:00-17:00", "LASRA · Taller de Anestesia Regional 4", ""),
        ("jueves", "14:00-17:00", "LASRA · Taller de Anestesia Regional 1", ""),
        ("viernes", "08:30-13:00", "LASRA · Taller de Anestesia Regional 2",
         " El día de este taller es el menos claro en la grilla — confirmar."),
        ("viernes", "14:00-16:30", "LASRA · Taller de Anestesia Regional 3", ""),
    ):
        add(dia, hora, nombre, "taller-habilidades", CABALLERIZA,
            coordinators=["Dra. Catalina Bellolio"], notes=NOTA_REGIONAL + extra)

    # --- Cafés con Expertos
    cafes = [
        ("miercoles", "11:00-12:00",
         "LASRA · Café con BabyBlocks: learning in the dark, how to master what no one around you knows?",
         ["Dr. Walid Alrayashi", "Dra. Deepa Kattail", "Dr. John Hagen"]),
        ("miercoles", "14:30-15:30",
         "LASRA · Café con el Dr. Philip Peng: bloqueo PENG y analgesia de cadera",
         ["Dr. Philip Peng"]),
        ("miercoles", "17:00-18:00",
         "LASRA · Café con la Dra. María Eugenia Seijas: lumbalgia sin resolver, ¿estamos olvidando el multífido?",
         ["Dra. María Eugenia Seijas"]),
        ("jueves", "08:30-09:30",
         "LASRA · Café con la Dra. Anahí Perlas: ultrasonido gástrico en pacientes con GLP-1",
         ["Dra. Anahí Perlas"]),
        ("jueves", "11:30-12:30",
         "LASRA · Café con el Dr. Alejandro Corujo: ultrasonido de columna lumbar en procedimientos centrales",
         ["Dr. Alejandro Corujo"]),
        ("jueves", "14:30-15:30",
         "LASRA · Café con el Dr. Alberto Sánchez: modelos farmacocinéticos para la sedación en anestesia regional",
         ["Dr. Alberto Sánchez"]),
        ("viernes", "08:30-09:30",
         "LASRA · Café con el Dr. Juan Carlos de la Cuadra: fundamentos del ultrasonido en anestesia regional",
         ["Dr. Juan Carlos de la Cuadra"]),
        ("viernes", "10:30-11:30",
         "LASRA · Café con el Dr. Olympio Chacon: medicina regenerativa en dolor",
         ["Dr. Olympio Chacon"]),
        ("viernes", "14:00-15:00",
         "LASRA · Café con expertos: inyecciones de ozono y viscosuplementación en dolor musculoesquelético",
         ["Dr. Pablo Castromán", "Dra. Marta Surbano", "Dra. María José Otero"]),
    ]
    for dia, hora, titulo, gente in cafes:
        add(dia, hora, titulo, "taller-casos", ANEXO,
            coordinators=["Dr. Emiliano Landín"], speakers=gente,
            cupos="grupos muy reducidos", notes=NOTA_CAFE)

    order = ["sabado", "domingo", "lunes", "martes", "miercoles", "jueves", "viernes"]
    events.sort(key=lambda e: (order.index(e["day"]) if e["day"] in order else 99,
                               e["startHour"], e["title"]))

    json.dump(events, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\n".join(log))
    print(f"\nTotal: {len(events)} eventos (antes 48)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
