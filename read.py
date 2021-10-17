import sys
import re
from xml.dom import minidom
import xml.etree.ElementTree as ET
from HTMLParser import MyHTMLParser


def shortAnswer(nodoPregunta):
    preguntas = []
    respuestasAll = []
    respuestas = []

    pregunta = nodoPregunta.find("questiontext")[0].text
    parser = MyHTMLParser()
    parser.feed(pregunta)

    preguntas.append([pregunta])

    for indx, respuesta in enumerate(nodoPregunta.iter("answer")):
        respuestaRaw = respuesta[0].text
        if respuesta.get("fraction") == "100":
            respuestas.append(respuestaRaw)
        else:
            respuestas.append(respuestaRaw)
    img = [parser.imgInfo["src"] + parser.imgInfo["alt"]]
    respuestasAll.append(respuestas)
    return list(zip(preguntas, respuestasAll, ["shortAnswer"], img))


def trueFalse(nodoPregunta):
    preguntas = []
    respuestasAll = []

    # if nodoPregunta.get("type") == "truefalse":
    respuestas = []
    pregunta = []
    preguntaRaw = nodoPregunta.find("questiontext")[0].text
    parser = MyHTMLParser()
    parser.feed(preguntaRaw)
    pregunta.append(parser.data)
    preguntas.append(pregunta)

    for indx, respuesta in enumerate(nodoPregunta.iter("answer")):
        respuestaRaw = respuesta[0].text
        if respuesta.get("fraction") == "100" and respuestaRaw == "true":
            respuestas.append(str(indx+1) + ") " + "Verdadero")
        else:
            respuestas.append(str(indx+1) + ") " + "Falso")

    respuestasAll.append(respuestas)
    img = [parser.imgInfo["src"] + parser.imgInfo["alt"]]
    return list(zip(preguntas, respuestasAll, ["trueFalse"], img))


def multiplechoice(nodoPregunta):
    preguntas = []
    respuestasAll = []

    respuestas = []
    pregunta = []
    preguntaRaw = nodoPregunta.find("questiontext")[0].text
    parser = MyHTMLParser()
    parser.feed(preguntaRaw)
    pregunta.append(parser.data)
    preguntas.append(pregunta)

    for indx, respuesta in enumerate(nodoPregunta.iter("answer")):
        respuestaAct = []
        respuestaRaw = respuesta[0].text
        if respuesta.get("fraction") == "100":
            respuestas.append(str(indx+1) + ") " + respuestaRaw[respuestaRaw.find(">") + 1:respuestaRaw.rfind("<")])
        else:
            respuestas.append(str(indx+1) + ") " + respuestaRaw[respuestaRaw.find(">") + 1:respuestaRaw.rfind("<")])

    print("DIC")
    print(parser.imgInfo)
    respuestasAll.append(respuestas)
    img = [parser.imgInfo["src"] + parser.imgInfo["alt"]]
    return list(zip(preguntas, respuestasAll, ["multichoice"], img))


def gapSelect(nodoPregunta):
    preguntas = []
    respuestasAll = []

    respuestas = []
    pregunta = []
    preguntaRaw = nodoPregunta.find("questiontext")[0].text
    parser = MyHTMLParser()
    parser.feed(preguntaRaw)
    correcta = int(preguntaRaw[preguntaRaw.find("[[") + 2]) - 1
    pregunta.append(parser.data[:parser.data.find("[[") + 2] + "_" + parser.data[parser.data.find("[[") + 3:])
    preguntas.append(pregunta)
    preguntas.append(pregunta)

    for indx, respuesta in enumerate(nodoPregunta.iter("selectoption")):
        respuestaRaw = respuesta[0].text
        if indx == correcta:
            respuestas.append(str(indx+1) + ") " + respuestaRaw)
        else:
            respuestas.append(str(indx+1) + ") " + respuestaRaw)

    respuestasAll.append(respuestas)
    # print(list(zip(preguntas, respuestasAll)))
    img = [parser.imgInfo["src"] + parser.imgInfo["alt"]]
    return list(zip(preguntas, respuestasAll, ["gapSelect"], img))


def conseguirNotas(file):
    arbol = ET.parse(file)
    raiz = arbol.getroot()
    respuestas = {}
    for nodoPregunta in raiz.findall("question")[1:]:
        # Para conseguir la nota de las preguntas en la que se debe seleccionar la palabra que falta
        for index, respuesta in enumerate(nodoPregunta.iter("selectoption")):
            preguntaRaw = nodoPregunta.find("questiontext")[0].text
            parser = MyHTMLParser()
            parser.feed(respuesta[0].text)
            correcta = int(preguntaRaw[preguntaRaw.find("[[") + 2]) - 1
            if index == correcta:
                respuestas[str(index+1) + ") " + parser.data] = 100
            else:
                respuestas[parser.data] = 0
        # Para los demas tipos de preguntas, cada respuesta tiene una nota asociada
        for index, respuesta in enumerate(nodoPregunta.iter("answer")):
            parser = MyHTMLParser()
            parser.feed(respuesta[0].text)
            if nodoPregunta.get("type") == "truefalse":
                if respuesta[0].text == "true":
                    respuestas[str(index+1) + ") " + "Verdadero"] = int(respuesta.get("fraction"))
                else:
                    respuestas[str(index+1) + ") " + "Falso"] = int(respuesta.get("fraction"))
            elif nodoPregunta.get("type") == "shortanswer":
                respuestas[parser.data] = int(respuesta.get("fraction"))
            else:
                respuestas[str(index+1) + ") " + parser.data] = int(respuesta.get("fraction"))
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
    print(sum(preguntas, []))
    return sum(preguntas, [])


if __name__ == "__main__":
    raiz = readXMLFile(sys.argv[1])
    print(conseguirNotas(sys.argv[1]))
