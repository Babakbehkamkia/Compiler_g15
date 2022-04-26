from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class DSCmetric(JavaParserLabeledListener):
    def __init__(self, file_name):
        self.file_name = file_name
        # self.typed = []
        self.typedBy = []
        # self.use = []
        self.useBy = []


    @property
    def get_use(self):
        d = {}
        # d['use'] = self.use
        d['useBy'] = self.useBy
        return d

    @property
    def get_type(self):
        d = {}
        # d['typed'] = self.typed
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

    def enterPrimary4(self, ctx: JavaParserLabeled.Primary4Context):
        # ==========used/usedby=============
        is_None = False
        VI = ctx

        while (type(ctx) != JavaParserLabeled.ClassDeclarationContext and type(
                ctx) != JavaParserLabeled.MethodDeclarationContext):
            if(ctx.parentCtx):
                ctx = ctx.parentCtx
            else:
                is_None = True
                break
            # print(ctx.IDENTIFIER().getText())
            # print(VI.getText())

        if(not is_None):
            line1 = VI.IDENTIFIER().symbol.line
            column1 = VI.IDENTIFIER().symbol.column
            line2 = ctx.IDENTIFIER().symbol.line
            column2 = ctx.IDENTIFIER().symbol.column

            # self.use.append((ctx.IDENTIFIER().getText(), VI.getText()))
            self.useBy.append((VI.getText(), ctx.IDENTIFIER().getText(), line1, column1, line2, column2))


    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        # ==========typed/typedby=============
        ctx1 = ctx.variableDeclarators()
        ctx11 = ctx1.variableDeclarator()[0].variableDeclaratorId()
        # print(ctx11)
        # print(ctx11)
        # ctx12 = ctx11.variableDeclaratorId()
        ctx2 = ctx.typeType()

        line2 = ctx2.children[0].children[0].symbol.line
        column2 = ctx2.children[0].children[0].symbol.column
        line1 = ctx11.IDENTIFIER().symbol.line
        column1 = ctx11.IDENTIFIER().symbol.column

        # print(ctx1.getText())
        # print(ctx2.getText())
        self.typedBy.append((ctx11.getText(), ctx2.getText(), line1, column1, line2, column2))
        # self.typed.append((ctx2.getText(), ctx11.getText()))



