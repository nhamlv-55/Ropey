import os
import argparse

class Lemma:
    def __init__(self, exp_folder, new_folder):
        self.lemma = ""
        self.level = -1
        self.smtfile = None
        self.new_folder = new_folder
        self.exp_folder = exp_folder

    def to_smt2(self):
        if not os.path.exists(self.new_folder):
            os.makedirs(self.new_folder)

        if self.smtfile is None: return
        with open(os.path.join(self.exp_folder, self.smtfile), "r") as f:
            old_file_lines = f.readlines()
            params = old_file_lines[-1]
            if "dump_threshold 5.00 " in params:
                return
        new_filename = self.smtfile + ".with_lemma.smt2"
        with open(os.path.join(self.exp_folder, self.new_folder, new_filename), "w") as f:
            f.writelines(old_file_lines)
            f.write("\n")
            f.write("(act-lvl %s)\n"%(self.level))
            f.write("(ind-gen %s)\n"%(self.lemma))



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-input', help='could be a smt2 file or a folder')
    parser.add_argument("-l", "--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='CRITICAL', help="Set the logging level")
    args = parser.parse_args()

    exp_folder = args.input
    new_folder = "ind_gen_files"
    with open(os.path.join(exp_folder, ".z3-trace"), "r") as f:
        lines = f.readlines()


    current_lemma = None


    for l in lines:
        if l.startswith("**"):
            continue
        elif l=="LEMMA:\n":
            if current_lemma is not None:
                current_lemma.to_smt2()
            current_lemma = Lemma(exp_folder, new_folder)
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

if __name__=="__main__":
    main()
