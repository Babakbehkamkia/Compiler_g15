from gen.JavaParserLabeled import JavaParserLabeled
from gen.JavaParserLabeledListener import JavaParserLabeledListener


class DSCmetric(JavaParserLabeledListener):
    def __init__(self, file_name):
        self.file_name = file_name
        self.typed = []
        self.typedBy = []
        self.use = []
        self.useBy = []


    @property
    def get_use(self):
        d = {}
        d['use'] = self.use
        d['useBy'] = self.useBy
        return d

    @property
    def get_type(self):
        d = {}
        d['typed'] = self.typed
        d['typedBy'] = self.typedBy
        return d

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        # self.method_names.append(ctx.IDENTIFIER().getText())
        # ctx = ctx.
        # ctx = ctx.
        # print(ctx.getText())
        pass
    def enterBlock(self, ctx:JavaParserLabeled.BlockContext):
        pass
        # i =0;
        # while(True):
        #     try:
        #         c = ctx.blockStatement(i)
        #         # print(c.getText())
        #         i+=1
        #     except:
        #         break

    def enterVariableDeclarator(self, ctx: JavaParserLabeled.VariableDeclaratorContext):
        # ==========use/useBy=============
        VI = ctx.variableInitializer()
        if VI != None:
            for i in range(6):
                ctx = ctx.parentCtx
            # print(ctx.IDENTIFIER().getText())
            # print(VI.getText())
            self.use.append((ctx.IDENTIFIER().getText(), VI.getText()))
            self.useBy.append((VI.getText(), ctx.IDENTIFIER().getText()))


        # for i in range(5):
        #     ctx = ctx.variableDeclarator(i)
        #     print(f'{i} = ',ctx.getText())

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):

        # ==========typed/typedby=============
        ctx1 = ctx.variableDeclarators()
        ctx2 = ctx.typeType()
        # print(ctx1.getText())
        # print(ctx2.getText())
        self.typedBy.append((ctx1.getText(), ctx2.getText()))
        self.typed.append((ctx2.getText(), ctx1.getText()))