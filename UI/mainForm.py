from tkinter import *
import xml.etree.cElementTree as ET


#xml = None
      
class mainForm():
    def selectItemOfCanvas(event):
        print('selectItemOfCanvas')
        global selectedItemOfCanvas
        if selectedItemOfCanvas == None:
            selectedItemOfCanvas = xml.find('.//node')
        for item in xml.iter('node'):
            x0,y0,x1,y1 =int(item.get('x0')),int(item.get('y0')),int(item.get('x1')),int(item.get('y1')) 
            wOfItem = x1-x0
            hOfItem = y1-y0
            dXOfItem = abs((x0+x1)/2-event.x)
            dYOfItem = abs((y0+y1)/2-event.y)
            if dXOfItem <= wOfItem and dYOfItem <= hOfItem:
                x0,y0,x1,y1 = int(selectedItemOfCanvas.get('x0')), int(selectedItemOfCanvas.get('y0')), int(selectedItemOfCanvas.get('x1')), int(selectedItemOfCanvas.get('y1'))
                wOfSelectItem = x1-x0
                hOfSelectItem = y1-y0
                dXOfSelectItem = abs((x1+x0)/2-event.x)
                dYOfSelectItem = abs((y1+y0)/2-event.y)
                if dXOfItem + dYOfItem < dXOfSelectItem + dYOfSelectItem:
                    selectedItemOfCanvas = item

    def moveItem(event):
        if selectedItemOfCanvas != None:
            x0,y0,x1,y1 = getX0Y0X1Y1OfNodeXML(selectedItemOfCanvas)
            w2=(x1-x0)/2
            h2=(y1-y0)/2
            x0,y0,x1,y1 = event.x-w2,event.y-h2,event.x+w2,event.y+h2
            setNodeXML(selectedItemOfCanvas,x0,y0,x1,y1)
            canvas.coords(selectedItemOfCanvas.get('id'), x0,y0,x1,y1)                        

    def setNodeXML(node,x0,y0, x1, y1):
        node.set('x0',str(int(x0))) 
        node.set('y0',str(int(y0)))
        node.set('x1',str(int(x1)))
        node.set('y1',str(int(y1)))

    def getX0Y0X1Y1OfNodeXML(node):
        return int(node.get('x0')),int(node.get('y0')),int(node.get('x1')),int(node.get('y1')),

    def loadXMLProject(fileName):
        print('loadXMLProject')
        global xml
        root = ET.parse(fileName)
        xml = root.getroot()

    def updateCanvas():
        print('updateCanvas')
        for item in xml.iter('transition'):
            x0,y0,x1,y1 =getX0Y0X1Y1OfNodeXML(item)
            item.set('id',str(canvas.create_line(x0,y0,x1,y1)))
        for item in xml.iter('node'):
            x0,y0,x1,y1 =getX0Y0X1Y1OfNodeXML(item)
            item.set('id', str(canvas.create_oval(x0,y0,x1,y1,fill="white")))


    def selectCircleOfCanvas(event):
        print('selectCircleOfCanvas')

    @staticmethod
    def load(): 
        global canvas
        global selectedItemOfCanvas
        global xml

        selectedItemOfCanvas = None
        root = Tk()
        instrumentPanel = Frame(root, height = 25, bg = 'gray')
        circle = Canvas(instrumentPanel, height = 25, width = 25)
        circle.create_oval(2,2,24,24)
        circle.bind('<1>', selectCircleOfCanvas)
        circle.pack(side = 'left', fill = 'y')

        canvas = Canvas(root, height = 400, width = 600)
        canvas.bind('<B1-Motion>', moveItem)
        canvas.bind('<1>', selectItemOfCanvas)

        loadXMLProject(fileName=r"C:\tmp\filename.xml")
        updateCanvas()

        instrumentPanel.pack(side = 'top', fill = 'x')
        canvas.pack(side = 'bottom', fill = 'both', expand = 1)

        root.mainloop()
        tree = ET.ElementTree(xml)
        tree.write(r"C:\tmp\filename.xml")
        print('END')