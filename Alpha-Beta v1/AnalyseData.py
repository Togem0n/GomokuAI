import xml.sax

class DataHandler( xml.sax.ContentHandler ):
   def __init__(self):
      self.file = open('source/dataset.txt','w+')
      self.move = ""
      self.rule = ""
      self.flag = ''

   # 元素开始调用
   def startElement(self, tag, attributes):
      self.CurrentData = tag
      if tag == "game":
        if attributes['rule'] =='1':
          self.flag = '1'
        else:
           self.flag = '2'

   # 元素结束调用
   def endElement(self, tag):
      if self.CurrentData == 'move' and self.flag == '1':
          self.file.writelines(self.move)
          print(self.move)
      self.CurrentData = ''

   # 读取字符时调用
   def characters(self, content):
      if self.CurrentData == "move":
         self.move = content
      elif self.CurrentData == "rule":
         self.rule = content



if (__name__ == "__main__"):
    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = DataHandler()
    parser.setContentHandler(Handler)

    parser.parse("source/dataset.xml")