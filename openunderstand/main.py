"""

"""

import os
from fnmatch import fnmatch

from antlr4 import *

from analysis_passes.used_usedby import UsedAndUsedByListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaLexer import JavaLexer

from oudb.models import KindModel, EntityModel, ReferenceModel
from oudb.api import open as db_open, create_db
from oudb.fill import main

# from analysis_passes.couple_coupleby import ImplementCoupleAndImplementByCoupleBy
# from analysis_passes.create_createby import CreateAndCreateBy
# from analysis_passes.declare_declarein import DeclareAndDeclareinListener
from analysis_passes.class_properties import ClassPropertiesListener, InterfacePropertiesListener
from metric import DSCmetric

class Project():
    tree = None

    def Parse(self, fileAddress):
        file_stream = FileStream(fileAddress)
        lexer = JavaLexer(file_stream)
        tokens = CommonTokenStream(lexer)
        parser = JavaParserLabeled(tokens)
        tree = parser.compilationUnit()
        self.tree = tree
        return tree

    def Walk(self, listener, tree):
        walker = ParseTreeWalker()
        walker.walk(listener=listener, t=tree)

    def getListOfFiles(self, dirName):
        listOfFile = os.listdir(dirName)
        allFiles = list()
        for entry in listOfFile:
            # Create full path
            fullPath = os.path.join(dirName, entry)
            if os.path.isdir(fullPath):
                allFiles = allFiles + self.getListOfFiles(fullPath)
            elif fnmatch(fullPath, "*.java"):
                allFiles.append(fullPath)

        return allFiles

    def getFileEntity(self, path):
        # kind id: 1
        path = path.replace("/", "\\")
        name = path.split("\\")[-1]
        file = open(path, mode='r')
        file_ent = EntityModel.get_or_create(_kind=1, _name=name, _longname=path, _contents=file.read())[0]
        file.close()
        print("processing file:", file_ent)
        return file_ent


    def getPackageEntity(self, file_ent, name, longname):
        # package kind id: 72
        ent = EntityModel.get_or_create(_kind=72, _name=name, _parent=file_ent,
                                        _longname=longname, _contents="")
        return ent[0]

    def getUnnamedPackageEntity(self, file_ent):
        # unnamed package kind id: 73
        ent = EntityModel.get_or_create(_kind=73, _name="(Unnamed_Package)", _parent=file_ent,
                                        _longname="(Unnamed_Package)", _contents="")
        return ent[0]

    def getClassProperties(self, class_longname, file_address):
        listener = ClassPropertiesListener()
        listener.class_longname = class_longname.split(".")
        listener.class_properties = None
        self.Walk(listener, self.tree)
        return listener.class_properties

    def getInterfaceProperties(self, interface_longname, file_address):
        listener = InterfacePropertiesListener()
        listener.interface_longname = interface_longname.split(".")
        listener.interface_properties = None
        self.Walk(listener, self.tree)
        return listener.interface_properties

    def getCreatedClassEntity(self, class_longname, class_potential_longname, file_address):
        props = p.getClassProperties(class_potential_longname, file_address)
        if not props:
            return self.getClassEntity(class_longname, file_address)
        else:
            return self.getClassEntity(class_potential_longname, file_address)

    def getClassEntity(self, class_longname, file_address):
        props = p.getClassProperties(class_longname, file_address)
        if not props:  # This class is unknown, unknown class id: 84
            ent = EntityModel.get_or_create(_kind=84, _name=class_longname.split(".")[-1],
                                            _longname=class_longname, _contents="")
        else:
            if len(props["modifiers"]) == 0:
                props["modifiers"].append("default")
            kind = self.findKindWithKeywords("Class", props["modifiers"])
            ent = EntityModel.get_or_create(_kind=kind, _name=props["name"],
                                            _longname=props["longname"],
                                            _parent=props["parent"] if props["parent"] is not None else file_ent,
                                            _contents=props["contents"])
        return ent[0]

    def getInterfaceEntity(self, interface_longname, file_address):  # can't be of unknown kind!
        props = p.getInterfaceProperties(interface_longname, file_address)
        if not props:
            return None
        else:
            kind = self.findKindWithKeywords("Interface", props["modifiers"])
            ent = EntityModel.get_or_create(_kind=kind, _name=props["name"],
                                            _longname=props["longname"],
                                            _parent=props["parent"] if props["parent"] is not None else file_ent,
                                            _contents=props["contents"])
        return ent[0]

    def getImplementEntity(self, longname, file_address):
        ent = self.getInterfaceEntity(longname, file_address)
        if not ent:
            ent = self.getClassEntity(longname, file_address)
        return ent

    def findKindWithKeywords(self, type, modifiers):
        if len(modifiers) == 0:
            modifiers.append("default")
        leastspecific_kind_selected = None
        for kind in KindModel.select().where(KindModel._name.contains(type)):
            if self.checkModifiersInKind(modifiers, kind):
                if not leastspecific_kind_selected \
                        or len(leastspecific_kind_selected._name) > len(kind._name):
                    leastspecific_kind_selected = kind
        return leastspecific_kind_selected

    def checkModifiersInKind(self, modifiers, kind):
        for modifier in modifiers:
            if modifier.lower() not in kind._name.lower():
                return False
        return True


if __name__ == '__main__':
    p = Project()
    create_db("../benchmark2_database.oudb",
              project_dir="../benchmark")
    main()
    db = db_open("../benchmark2_database.oudb")

    # path = "D:/Term 7/Compiler/Final proj/github/OpenUnderstand/benchmark"
    path = "D:/term 6/compiler/proje/Compiler_g15/openunderstand/benchmark"
    files = p.getListOfFiles(path)
    ########## AGE KHASTID YEK FILE RO RUN KONID:
    # files = ["D:/term 6/compiler/proje/Compiler_g15/openunderstand/benchmark/calculator_app/src/com/calculator/app/method/fibonacci.java"]

    for file_address in files:
        try:
            file_ent = p.getFileEntity(file_address)
            tree = p.Parse(file_address)
        except Exception as e:
            print("An Error occurred in file:" + file_address + "\n" + str(e))

        stream = FileStream(file_address, encoding="utf8")
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(token_stream)
        parse_tree = parser.compilationUnit()
        my_listener = DSCmetric(file_address)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)
        # ==========typed/typedby=============
        d_type = my_listener.get_type
        for type_tuple in d_type['typedBy']:
            ent, h_c1 = EntityModel.get_or_create(_kind=224, _parent=None, _name=type_tuple[1], _longname=file_address, _value=None,
                                            _type=None, _contents=stream)
            scope, h_c2 = EntityModel.get_or_create(_kind=225, _parent=None, _name=type_tuple[0], _longname=file_address, _value=None,
                                            _type=None, _contents=stream)
            ref1 = ReferenceModel.get_or_create(_kind=224, _file=scope, _line=type_tuple[4], _column=type_tuple[5], _ent=ent, _scope=scope)
            ref2 = ReferenceModel.get_or_create(_kind=225, _file=ent, _line=type_tuple[2], _column=type_tuple[3], _ent=scope, _scope=ent)
        # print(d_type)

        # ==========used/usedby=============
        d_use = my_listener.get_use
        for use_tuple in d_use['useBy']:
            ent, h_c1 = EntityModel.get_or_create(_kind=226, _parent=None, _name=use_tuple[1], _longname=file_address, _value=None,
                                            _type=None, _contents=stream)
            scope, h_c2 = EntityModel.get_or_create(_kind=227, _parent=None, _name=use_tuple[0], _longname=file_address, _value=None,
                                              _type=None, _contents=stream)
            ref1 = ReferenceModel.get_or_create(_kind=226, _file=scope, _line=use_tuple[4], _column=use_tuple[5], _ent=ent,
                                                _scope=scope)
            ref2 = ReferenceModel.get_or_create(_kind=227, _file=ent, _line=use_tuple[2], _column=use_tuple[3], _ent=scope,
                                                _scope=ent)
            # print(d_use)


#     kind id
# 224		Java Typed
# 225    	Java Typedby
# 226		Java Use
# 227	 	Java Useby