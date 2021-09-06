from xml.dom import minidom
import xml.etree.ElementTree as ET


def readXMLFile():
    arbol = ET.parse('preguntasXML.xml')
    raiz = arbol.getroot()
    preguntas = []
    respuestas = []
    for nodoPregunta in raiz.findall("question")[1:]:
        preguntaRaw = nodoPregunta.find("questiontext")[0].text
        pregunta = preguntaRaw[preguntaRaw.find(">") + 1:preguntaRaw.rfind("<")]
        preguntas.append(pregunta)

        for respuesta in nodoPregunta.iter("answer"):
            if respuesta.get("fraction") == "100":
                respuestaRaw = respuesta[0].text
                respuestas.append(respuestaRaw[respuestaRaw.find(">") + 1:respuestaRaw.rfind("<")])

    return list(zip(preguntas, respuestas))


if __name__ == "__main__":
    readXMLFile()
