
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from oudb.api import create_db, open as db_open
from oudb.models import *

db_path = 'C:/Users/babak/Desktop/source/OpenUnderstand-master/openunderstand/oudb/database.db'
create_db(
    dbname=db_path,
    project_dir='C:/Users/babak/Desktop/source/OpenUnderstand-master/openunderstand'
)
db = db_open(db_path)

def create_Ref(kind, file, line, column, ent, scope):
    obj, has_crated = ReferenceModel.get_or_create(_kind=kind, _file=file, _line=line, _column=column, _ent=ent, _scope=scope)
    return obj

def create_Entity(id, kind, parent, name, longname, value, type, contents):
    obj, has_crated = EntityModel.get_or_create(_id=id, _kind=kind, _parent=parent, _name=name, _longname=longname, _value=value, _type=type, _contents=contents)
    return obj

class UsedAndUsedByListener(JavaParserLabeledListener):
    def __init__(self, longname, name):
        self.longname=longname
        self.used = []
        self.usedBy = []
        self.method_Name = None
        self.longnames = []
        self.is_unknown_class = []
        self.parents = []
        self.line = []
        self.col = []
        self.file = create_Entity(name=name, longname=longname, kind="Java File", value=None, parent=None, entity_type=None, contents=None)

    def enterMethodDeclaration(self, ctx:JavaParserLabeled.MethodDeclarationContext):
        if ctx.parentCtx == '':
            self.modifiers = ctx.parentCtx
        self.method_Name = str(ctx.IDENTIFIER())

    def exitMethodDecelration(self, ctx:JavaParserLabeled.MethodDeclarationContext):
        self.method_Name = None

    def enterPrimary4(self, ctx: JavaParserLabeled.Primary4Context):
        if self.method_Name != None:
            self.used.append(ctx.getText())
            self.usedby.append(self.method_Name)
            self.line.append(ctx.IDENTIFIER().symbol.line)
            self.col.append(ctx.IDENTIFIER().symbol.column)
            ent = create_Entity(self.method_Name, self.longname + '.' + self.method_Name, self.longname, 'Java Method', None, None, None)
            scope = create_Entity(str(ctx.IDENTIFIER()), self.longname + '.' + self.method_Name + '.' + str(ctx.IDENTIFIER()), self.method_Name, 'Java Variable', None, None, None)
            ref1 = create_Ref('Use', self.file, ctx.IDENTIFIER().symbol.line, ctx.IDENTIFIER().symbol.column)
            ref1 = create_Ref('UsedBy', self.file, ctx.IDENTIFIER().symbol.line, ctx.IDENTIFIER().symbol.column)
