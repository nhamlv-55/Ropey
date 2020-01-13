import os

exp_folder = "Exp55"
new_folder = "ind_gen_files"
with open(os.path.join(exp_folder, ".z3-trace"), "r") as f:
    lines = f.readlines()

class Lemma:
    def __init__(self, new_folder):
        self.lemma = ""
        self.level = -1
        self.smtfile = None
        self.new_folder = os.path.join(exp_folder, new_folder)

    def to_smt2(self):
        if not os.path.exists(self.new_folder):
            os.makedirs(self.new_folder)

        if self.smtfile is None: return
        with open(os.path.join(exp_folder, self.smtfile), "r") as f:
            old_file_lines = f.readlines()
            params = old_file_lines[-1]
            if "dump_threshold 5.00 " in params:
                return
        new_filename = self.smtfile + ".with_lemma.smt2"
        with open(os.path.join(self.new_folder, new_filename), "w") as f:
            f.writelines(old_file_lines)
            f.write("\n")
            f.write("(act-lvl %s)\n"%(self.level))
            f.write("(ind-gen %s)\n"%(self.lemma))


current_lemma = None


for l in lines:
    if l=="LEMMA:\n":
        if current_lemma is not None:
            current_lemma.to_smt2()
        current_lemma = Lemma(new_folder)
    elif "LEVEL:" in l:
        lvl = int(l.strip().split(":")[1])
        current_lemma.level = lvl
    elif "Dumping" in l:
        if current_lemma.smtfile is not None:
            continue
        filename = l.strip().split()[-1]
        current_lemma.smtfile = filename
    else:
        current_lemma.lemma+=l
