class Recorder:
    Counter = 0
    nlist = []
    instances = []
    def __init__(self):
        Recorder.Counter += 1

    class NodeRecorder:
        Counter = 0
        def __init__(self, DofList, RecordedNodeTags, RecordedContent, OutFile, TimeInterval = 0.0, ShowTime = True):
            # dofs in DofList begins from 0, the largest is 5
            Recorder.NodeRecorder.Counter += 1

            self.DofList = DofList
            self.RecordedNodeTags = RecordedNodeTags
            self.RecordedContent = RecordedContent
            self.OutFile = OutFile
            self.TimeInterval = TimeInterval
            if ShowTime:
                self.ShowTime = 'true'
            else:
                self.ShowTime = 'false'

            self.name = "NodeRecorder%d" % Recorder.NodeRecorder.Counter

            self.command = '''OPS_Stream *NodeOut%d = new FileStream("%s", OVERWRITE, 2);\n''' % (Recorder.NodeRecorder.Counter, self.OutFile)

            self.command += "ID RecorededDOFs%d(%d);\n" % (Recorder.NodeRecorder.Counter, len(self.DofList))
            for i, obj in enumerate(self.DofList):
                self.command += "RecorededDOFs%d(%d) = %d;\n" % (Recorder.NodeRecorder.Counter, i, obj)

            self.command += "ID RecordedNodes%d(%d);\n" % (Recorder.NodeRecorder.Counter, len(self.RecordedNodeTags))
            for i, obj in enumerate(self.RecordedNodeTags):
                self.command += "RecordedNodes%d(%d) = %d;\n" % (Recorder.NodeRecorder.Counter, i, obj)

            self.command += '''NodeRecorder *%s = new NodeRecorder(RecorededDOFs%d, &RecordedNodes%d, 0, "%s", *theDomain, *NodeOut%d, %f, %s, 0);\n''' % (self.name, Recorder.NodeRecorder.Counter, Recorder.NodeRecorder.Counter, self.RecordedContent, Recorder.NodeRecorder.Counter, self.TimeInterval, self.ShowTime)
            self.command += "theDomain->addRecorder(*%s);\n" % self.name

            Recorder.instances.append(self)

        def DofList(self):
            return self.DofList
        def RecordedNodeTags(self):
            return self.RecordedNodeTags
        def RecordedContent(self):
            return self.RecordedContent
        def OutFile(self):
            return self.OutFile
        def TimeInterval(self):
            return self.TimeInterval
        def name(self):
            return self.name
        def command(self):
            return self.command
        def include(self):
            return ["NodeRecorder.h"]

    class ElementRecorder:
        Counter = 0
        def __init__(self, RecordedElementTags, RecordedContent, OutFile, TimeInterval = 0.0, ShowTime = True):
            Recorder.ElementRecorder.Counter += 1
            self.RecordedElementTags = RecordedElementTags
            self.RecordedContent = RecordedContent
            self.OutFile = OutFile
            self.TimeInterval = TimeInterval
            if ShowTime:
                self.ShowTime = 'true'
            else:
                self.ShowTime = 'false'

            self.name = "ElementRecorder%d" % Recorder.ElementRecorder.Counter

            self.command = '''OPS_Stream *EleOut%d = new FileStream("%s", OVERWRITE, 2);\n''' % (Recorder.ElementRecorder.Counter, self.OutFile)
            self.command += "ID RecordedEles%d(%d);\n" % (Recorder.ElementRecorder.Counter, len(self.RecordedElementTags))

            for i, obj in enumerate(self.RecordedElementTags):
                self.command += "RecordedEles%d(%d) = %d;\n" % (Recorder.ElementRecorder.Counter, i, obj)

            self.command += "const char *ForceType%d;\n" % Recorder.ElementRecorder.Counter
            self.command += '''ForceType%d = "%s";\n''' % (Recorder.ElementRecorder.Counter, self.RecordedContent)
            self.command += "ElementRecorder *%s = new ElementRecorder(&RecordedEles%d, &ForceType%d, 1, %s, *theDomain, *EleOut%d, %f, 0);\n" % (self.name, Recorder.ElementRecorder.Counter, Recorder.ElementRecorder.Counter, self.ShowTime, Recorder.ElementRecorder.Counter, self.TimeInterval)
            self.command += "theDomain->addRecorder(*%s);\n" % self.name

            Recorder.instances.append(self)

        def RecordedElementTags(self):
            return self.RecordedElementTags
        def RecordedContent(self):
            return self.RecordedContent
        def OutFilee(self):
            return self.OutFile
        def TimeInterval(self):
            return self.TimeInterval
        def name(self):
            return self.name
        def command(self):
            return self.command
        def include(self):
            return ["ElementRecorder.h"]





