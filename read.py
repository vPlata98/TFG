import sys
from xml.dom import minidom
import xml.etree.ElementTree as ET


def shortAnswer(nodoPregunta):
    preguntas = []
    respuestasAll = []
    respuestas = []

    pregunta = nodoPregunta.find("questiontext")[0].text

    preguntas.append([pregunta])

    for respuesta in nodoPregunta.iter("answer"):
        respuestaRaw = respuesta[0].text
        if respuesta.get("fraction") == "100":
            respuestas.insert(0, respuestaRaw)
        else:
            respuestas.append(respuestaRaw)

    respuestasAll.append(respuestas)
    return list(zip(preguntas, respuestasAll))


def trueFalse(nodoPregunta):
    preguntas = []
    respuestasAll = []

    # if nodoPregunta.get("type") == "truefalse":
    respuestas = []
    pregunta = []
    preguntaRaw = nodoPregunta.find("questiontext")[0].text
    pregunta.append(preguntaRaw[preguntaRaw.find(">") + 1:preguntaRaw.rfind("<")])
    preguntas.append(pregunta)

    for respuesta in nodoPregunta.iter("answer"):
        respuestaRaw = respuesta[0].text
        if respuesta.get("fraction") == "100" and respuestaRaw == "true":
            respuestas.insert(0, "Verdadero")
        else:
            respuestas.append("Falso")

    respuestasAll.append(respuestas)
    return list(zip(preguntas, respuestasAll))


def multiplechoice(nodoPregunta):
    preguntas = []
    respuestasAll = []

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
    return list(zip(preguntas, respuestasAll))


def gapSelect(nodoPregunta):
    preguntas = []
    respuestasAll = []

    respuestas = []
    pregunta = []
    preguntaRaw = nodoPregunta.find("questiontext")[0].text
    correcta = int(preguntaRaw[preguntaRaw.find("[[") + 2]) - 1
    newPregunta = preguntaRaw.replace(str(correcta + 1), "_")
    pregunta.append(newPregunta[newPregunta.find(">") + 1:newPregunta.rfind("<")])
    preguntas.append(pregunta)

    for indx, respuesta in enumerate(nodoPregunta.iter("selectoption")):
        respuestaRaw = respuesta[0].text
        if indx == correcta:
            respuestas.insert(0, respuestaRaw)
        else:
            respuestas.append(respuestaRaw)

    respuestasAll.append(respuestas)
    # print(list(zip(preguntas, respuestasAll)))
    return list(zip(preguntas, respuestasAll))


def conseguirNotas(file):
    arbol = ET.parse(file)
    raiz = arbol.getroot()
    respuestas = {}
    for nodoPregunta in raiz.findall("question")[1:]:
        for index, respuesta in enumerate(nodoPregunta.iter("selectoption")):
            preguntaRaw = nodoPregunta.find("questiontext")[0].text
            correcta = int(preguntaRaw[preguntaRaw.find("[[") + 2]) - 1
            if respuesta[0].text.find(">") != -1:
                if index == correcta:
                    respuestas[respuesta[0].text[respuesta[0].text.find(">") + 1:respuesta[0].text.rfind("<")]] = 100
                else:
                    respuestas[respuesta[0].text[respuesta[0].text.find(">") + 1:respuesta[0].text.rfind("<")]] = 0
            else:
                if index == correcta:
                    respuestas[respuesta[0].text] = 100
                else:
                    respuestas[respuesta[0].text] = 0
        for respuesta in nodoPregunta.iter("answer"):
            if nodoPregunta.get("type") == "truefalse":
                if respuesta[0].text == "true":
                    respuestas["Verdadero"] = int(respuesta.get("fraction"))
                else:
                    respuestas["Falso"] = int(respuesta.get("fraction"))
            elif respuesta[0].text.find(">") != -1:
                respuestas[respuesta[0].text[respuesta[0].text.find(">") + 1:respuesta[0].text.rfind("<")]] = \
                    int(respuesta.get("fraction"))
            else:
                respuestas[respuesta[0].text] = int(respuesta.get("fraction"))
    return respuestas

def readXMLFile(file):
    arbol = ET.parse(file)
    raiz = arbol.getroot()
    preguntas = []
    for nodoPregunta in raiz.findall("question")[1:]:
        if nodoPregunta.get("type") == "multichoice":
            preguntas.append(multiplechoice(nodoPregunta))
        elif nodoPregunta.get("type") == "truefalse":
            preguntas.append(trueFalse(nodoPregunta))
        elif nodoPregunta.get("type") == "shortanswer":
            preguntas.append(shortAnswer(nodoPregunta))
        elif nodoPregunta.get("type") == "gapselect":
            preguntas.append(gapSelect(nodoPregunta))
    #print(sum(preguntas, []))
    return sum(preguntas, [])


if __name__ == "__main__":
    raiz = readXMLFile(sys.argv[1])
    print(conseguirNotas(sys.argv[1]))
