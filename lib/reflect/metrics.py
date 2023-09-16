import math

from lib.reflect.sr_statement import SRIFStatement, SRFORStatement, SRWhileStatement, SRTRYStatement, SRSwitchStatement


class ClassLevelMetrics:
    def __init__(self, sr_class):
        self.sr_class = sr_class
        self.field_name_list = []
        self.method_name_list = []

    def get_method_cc(self, sr_method):
        result = 0
        total_statement = sr_method.get_all_statement(exclude_special=False)
        condition_nodes = []
        for st in total_statement:
            if type(st) == SRIFStatement:
                condition_nodes.append(st)
        result = len(condition_nodes) + 1
        return result

    def get_method_loc(self, sr_method):
        result = 0
        result = sr_method.end_line - sr_method.start_line + 1
        return result

    def get_method_pc(self, sr_method):
        result = 0
        result = len(sr_method.param_list)
        return result

    def get_method_LCOM1(self, sr_method):
        fstl = []
        P=0
        all_statement = sr_method.get_all_statement(exclude_special=False)
        for st in all_statement:
            method_name_l, var_name_l = self.statement_special_key_filter(st.to_node_word_list())
            object = {
                "method_name_l": method_name_l,
                "var_name_l": var_name_l
            }
            fstl.append(object)

        for i in range(0, len(fstl)):
            for j in range(i+1, len(fstl)):
                if self.check_common_word(
                    l1=list(fstl[i]["var_name_l"]),
                    l2=list(fstl[j]["var_name_l"]),
                ) is False:
                    P += 1


        # print(fstl)
        # print(P)
        return P

    def get_method_LCOM2(self, sr_method):
        fstl = []
        P = 0
        Q = 0
        all_statement = sr_method.get_all_statement(exclude_special=False)
        for st in all_statement:
            method_name_l, var_name_l = self.statement_special_key_filter(st.to_node_word_list())
            object = {
                "method_name_l": method_name_l,
                "var_name_l": var_name_l
            }
            fstl.append(object)

        for i in range(0, len(fstl)):
            for j in range(i + 1, len(fstl)):
                if self.check_common_word(
                        l1=list(fstl[i]["var_name_l"]),
                        l2=list(fstl[j]["var_name_l"]),
                ) is False:
                    P += 1
                else:
                    Q += 1

        # print(Q)
        # print(P)
        lcom2 = P - Q

        if lcom2 < 0:
            lcom2 = 0
        return lcom2

    def get_method_LCOM3(self, sr_method):
        fstl = []
        compnent_count = []
        all_statement = sr_method.get_all_statement(exclude_special=False)
        for st in all_statement:
            method_name_l, var_name_l = self.statement_special_key_filter(st.to_node_word_list())
            object = {
                "method_name_l": method_name_l,
                "var_name_l": var_name_l
            }
            fstl.append(object)

        for i in range(0, len(fstl)):
            for j in range(i + 1, len(fstl)):
                if self.check_common_word(
                        l1=list(fstl[i]["var_name_l"]),
                        l2=list(fstl[j]["var_name_l"]),
                ) is True:
                    if i not in compnent_count:
                        compnent_count.append(i)
                    if j not in compnent_count:
                        compnent_count.append(j)
        return len(compnent_count)

    def get_method_LCOM4(self, sr_method):
        fstl = []
        method_call_count = []
        component_count = 0
        all_statement = sr_method.get_all_statement(exclude_special=False)
        for st in all_statement:
            method_name_l, var_name_l = self.statement_special_key_filter(st.to_node_word_list())
            object = {
                "method_name_l": method_name_l,
                "var_name_l": var_name_l
            }
            fstl.append(object)

        for i in range(0, len(fstl)):
            if len(fstl[i]["method_name_l"]) > 0:
                component_count += 1
                for m in fstl[i]["method_name_l"]:
                    if m not in method_call_count:
                        method_call_count.append(m)
                        component_count+=1


        return component_count

    def get_method_LCOM5(self, sr_method):
        fstl = []
        var_used_count = []
        var_total_number = []
        all_statement = sr_method.get_all_statement(exclude_special=False)
        for st in all_statement:
            method_name_l, var_name_l = self.statement_special_key_filter(st.to_node_word_list())
            object = {
                "method_name_l": method_name_l,
                "var_name_l": var_name_l
            }
            fstl.append(object)

        for i in range(0, len(fstl)):
            if len(fstl[i]["var_name_l"]) > 0:
                for var in fstl[i]["var_name_l"]:
                    var_used_count.append(var)
                    if var not in var_total_number:
                        var_total_number.append(var)
        a = len(var_used_count)
        l = len(var_total_number)
        n = sr_method.get_method_LOC()
        if (l - n * l) == 0:
            return 0
        lcom5 = (a - n * l) / (l - n * l)
        return lcom5

    def get_method_COH(self, sr_method):
        fstl = []
        var_used_count = []
        var_total_number = []
        all_statement = sr_method.get_all_statement(exclude_special=False)
        for st in all_statement:
            method_name_l, var_name_l = self.statement_special_key_filter(st.to_node_word_list())
            object = {
                "method_name_l": method_name_l,
                "var_name_l": var_name_l
            }
            fstl.append(object)

        for i in range(0, len(fstl)):
            if len(fstl[i]["var_name_l"]) > 0:
                for var in fstl[i]["var_name_l"]:
                    var_used_count.append(var)
                    if var not in var_total_number:
                        var_total_number.append(var)
        a = len(var_used_count)
        l = len(var_total_number)
        n = sr_method.get_method_LOC()
        if (l - n * l) == 0:
            return 0
        lcom5 = (a - n * l) / (l - n * l)
        coh = 1- (1 - 1/n)*lcom5
        return coh

    def get_method_CC(self, sr_method):
        fstl = []
        IVt = 0
        IVc = 0
        all_statement = sr_method.get_all_statement(exclude_special=False)
        for st in all_statement:
            method_name_l, var_name_l = self.statement_special_key_filter(st.to_node_word_list())
            object = {
                "method_name_l": method_name_l,
                "var_name_l": var_name_l
            }
            fstl.append(object)

        for i in range(0, len(fstl)):
            for j in range(i + 1, len(fstl)):
                l1 = list(fstl[i]["var_name_l"])
                l2 = list(fstl[j]["var_name_l"])
                IVt += (len(l1) + len(l2))
                IVc += (len(self.get_common_words(l1, l2)))
        # print("IVt",IVt)
        # print("IVc",IVc)

        n = sr_method.get_method_LOC()
        nt = n-2
        if nt < 0:
            nt = 0
        l = 1*math.factorial(nt)/math.factorial(n)
        r = 0
        rl = math.factorial(n)/(2*math.factorial(nt))

        for i in range(1, int(rl)+1):
            if IVt == 0:
                r += (IVc / 1) * i
                continue
            r += (IVc/IVt)*i
        cc = l * r
        # print("l", l)
        # print("rl", rl)
        # print("r",r)
        return cc

    def get_method_NOAV(self, sr_method):
        fstl = []
        total_var_l = []
        all_statement = sr_method.get_all_statement(exclude_special=False)
        for st in all_statement:
            method_name_l, var_name_l = self.statement_special_key_filter(st.to_node_word_list())
            object = {
                "method_name_l": method_name_l,
                "var_name_l": var_name_l
            }
            fstl.append(object)

        for obj in fstl:
            for var in obj["var_name_l"]:
                if var not in total_var_l:
                    total_var_l.append(var)
        noav = len(total_var_l) + len(sr_method.param_list)
        return noav

    def get_method_CD(self, sr_method, class_name_list):
        fstl = []
        total_var_l = []
        all_statement = sr_method.get_all_statement(exclude_special=False)
        for st in all_statement:
            method_name_l, var_name_l = self.statement_special_key_filter(st.to_node_word_list())
            object = {
                "method_name_l": method_name_l,
                "var_name_l": var_name_l
            }
            fstl.append(object)

        for obj in fstl:
            for var in obj["var_name_l"]:
                if var in class_name_list:
                    if var not in total_var_l:
                        total_var_l.append(var)
        cd = len(total_var_l)
        return cd

    def get_common_words(self, l1, l2):
        lr = []
        if len(l1) > len(l2):
            for w in l1:
                if w in l2:
                    lr.append(w)
        else:
            for w in l2:
                if w in l1:
                    lr.append(w)

        return lr


    def check_common_word(self, l1, l2):
        if len(l1) > len(l2):
            for w in l1:
                if w in l2:
                    return True
        else:
            for w in l2:
                if w in l1:
                    return True
        return False

    def get_statement_abcl(self, sr_statement):
        result = 0
        a_feat = ["=", "*=", "/=", "%=", "+=", "-=", "<<=", ">>=", "&=", "!=", "^=", ">>>=", "++", "--"]

        if type(sr_statement) == SRIFStatement or type(sr_statement) == SRTRYStatement:
            result = 3
        elif type(sr_statement) == SRFORStatement or type(sr_statement) == SRWhileStatement:
            result = 4
        else:
            if "(" in sr_statement.word_list or "new" in sr_statement.word_list:
                result = 2
            else:
                for word in sr_statement.word_list:
                    if word in a_feat:
                        result = 1
                        break
        return result

    def statement_special_key_filter(self, word_list):
        new_st_l = []
        method_name_l = []
        var_name_l = []
        java_keywords = ["boolean", "int", "long", "short", "byte", "float", "double", "char", "class", "interface",
                         "if", "else", "do", "while", "for", "switch", "case", "default", "break", "continue", "return",
                         "try", "catch", "finally", "public", "protected", "private", "final", "void", "static",
                         "strict", "abstract", "transient", "synchronized", "volatile", "native", "package", "import",
                         "throw", "throws", "extends", "implements", "this", "supper", "instanceof", "new", "true",
                         "false", "null", "goto", "const", "=", "*=", "/=", "%=", "+=", "-=", "<<=", ">>=", "&=", "!=", "^=", ">>>=", "++", "--", "=="]
        special_key = "[\n`~!@#$%^&*()+=\\-_|{}':;',\\[\\].<>/?~！@#￥%……&*（）——+|{}【】‘；：”“’。， 、？]"
        for i, w in enumerate(word_list):
            if w not in java_keywords and w not in special_key and not str(w).isdigit():
                if i < (len(word_list)-1) and word_list[i+1] == "(":
                    method_name_l.append(w)
                else:
                    var_name_l.append(w)
        return method_name_l, var_name_l

    def get_statement_fuc(self, sr_statement):
        result = 0
        if len(self.field_name_list) == 0:
            for field in self.sr_class.field_list:
                self.field_name_list.append(field.field_name)
        for word in sr_statement.to_node_word_list():
            if word in self.field_name_list:
                result += 1
        return result

    def get_method_fuc(self, sr_method):
        result = 0
        for statement in sr_method.statement_list:
            s_re = self.get_statement_fuc(statement)
            result += s_re
        return result

    def get_method_lmuc(self, sr_method):
        result = 0
        for statement in sr_method.statement_list:
            s_re = self.get_statement__lmuc(statement)
            result += s_re
        return result

    def get_statement__lmuc(self, sr_statement):
        result = 0
        if len(self.method_name_list) == 0:
            for m in self.sr_class.method_list:
                self.method_name_list.append(m.method_name)
        for word in sr_statement.to_node_word_list():
            if word in self.method_name_list:
                result += 1
        return result

    def get_statement_puc(self, sr_statement, param_name_list):
        puc = 0
        method_name_l, var_name_l = self.statement_special_key_filter(sr_statement.to_node_word_list())
        for var in var_name_l:
            if var in param_name_list:
                puc+=1
        return puc

    def get_statement_vuc(self, sr_statement):
        method_name_l, var_name_l = self.statement_special_key_filter(sr_statement.to_node_word_list())
        return len(var_name_l)

    def get_statement_wc(self, sr_statement):
        node_word_list = sr_statement.to_node_word_list()
        return len(node_word_list)

    def get_method_block_depth(self, sr_method):
        self.calculate_depth(sr_method=sr_method)
        dp = 0
        for st in sr_method.get_all_statement():
            if st.block_depth > dp:
                dp = st.block_depth
        return dp

    def get_statement_block_depth(self, sr_method, sr_statement):
        if sr_statement.block_depth == -1:
            self.calculate_depth(sr_method=sr_method)
            return sr_statement.block_depth
        else:
            return sr_statement.block_depth

    def calculate_depth(self, sr_method):
        self.__calculate_depth(statement_list=sr_method.statement_list, current_depth=0)

    def __calculate_depth(self, statement_list, current_depth):
        depth = current_depth
        for st in statement_list:
            st.block_depth = depth
            if type(st) == SRIFStatement:
                self.__calculate_depth(statement_list=st.pos_statement_list, current_depth=depth+1)
                self.__calculate_depth(statement_list=st.neg_statement_list, current_depth=depth+1)
            elif type(st) == SRFORStatement:
                self.__calculate_depth(statement_list=st.child_statement_list, current_depth=depth+1)
            elif type(st) == SRWhileStatement:
                self.__calculate_depth(statement_list=st.child_statement_list, current_depth=depth + 1)
            elif type(st) == SRTRYStatement:
                self.__calculate_depth(statement_list=st.try_statement_list, current_depth=depth + 1)
                for cb in st.catch_block_list:
                    self.__calculate_depth(statement_list=cb.child_statement_list, current_depth=depth + 1)
                self.__calculate_depth(statement_list=st.final_block_statement_list, current_depth=depth + 1)
            elif type(st) == SRSwitchStatement:
                for sc in st.switch_case_list:
                    self.__calculate_depth(statement_list=sc.statement_list, current_depth=depth + 1)