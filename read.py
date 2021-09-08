from xml.dom import minidom
import xml.etree.ElementTree as ET


def multiplechoice(raiz):

    preguntas = []
    respuestasAll = []

    for nodoPregunta in raiz.findall("question")[1:]:
        respuestas = []
        pregunta = []
        preguntaRaw = nodoPregunta.find("questiontext")[0].text
        pregunta.append(preguntaRaw[preguntaRaw.find(">") + 1:preguntaRaw.rfind("<")])
        preguntas.append(pregunta)

        for respuesta in nodoPregunta.iter("answer"):
            respuestaAct = []
            respuestaRaw = respuesta[0].text
            if respuesta.get("fraction") == "100":
                respuestas.insert(0, respuestaRaw[respuestaRaw.find(">") + 1:respuestaRaw.rfind("<")])
            else:
                respuestas.append(respuestaRaw[respuestaRaw.find(">") + 1:respuestaRaw.rfind("<")])

        respuestasAll.append(respuestas)
        print([respuestas[0]])
    print(list(zip(preguntas, respuestasAll)))
    return list(zip(preguntas, respuestasAll))


def readXMLFile():
    arbol = ET.parse('preguntasXML.xml')
    raiz = arbol.getroot()
    return multiplechoice(raiz)


if __name__ == "__main__":
    raiz = readXMLFile()
