from pysmt.smtlib.parser import SmtLibParser, SmtLibCommand, SmtLibScript
from pysmt.exceptions import UnknownSmtLibCommandError, PysmtSyntaxError
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.CRITICAL)

class Z3Parser(SmtLibParser):
    def __init__(self, env=None, interactive = False):
        SmtLibParser.__init__(self, env, interactive)

        # Add new commands
        self.commands["act-lvl"] = self._cmd_act_lvl
        self.commands["ind-gen"] = self._cmd_ind_gen
        self.commands["push-cube"] = self._cmd_push_cube
        self.commands[":added-eqs"] = self._cmd_ignore
        self.commands["params"] = self._cmd_ignore

    def _cmd_ignore(self, current, tokens):
        _ = self.parse_check_sat_expr_list(tokens, current)
        return SmtLibCommand(current, [])

    def _cmd_check_sat(self, current, tokens):
        args = self.parse_check_sat_expr_list(tokens, current)
        return SmtLibCommand(current, args)
    def _cmd_declare_fun(self, current, tokens):
        """(declare-fun <symbol> (<sort>*) <sort>)"""
        var = self.parse_atom(tokens, current)
        params = self.parse_params(tokens, current)
        typename = self.parse_type(tokens, current)
        self.consume_closing(tokens, current)

        if params:
            typename = self.env.type_manager.FunctionType(typename, params)

        v = self._get_var(var, typename)
        if v.symbol_type().is_function_type():
            self.cache.bind(var, \
                    functools.partial(self._function_call_helper, v))
        else:
            self.cache.bind(var, v)
        return SmtLibCommand(current, [v, var, params, typename])

    def _cmd_act_lvl(self, current, tokens):
        lvl = int(self.parse_atom(tokens, current))
        self.consume_closing(tokens, current)
        return SmtLibCommand(current, lvl)
        pass

    def _cmd_ind_gen(self, current, tokens):
        expr = self.get_expression(tokens)
        self.consume_closing(tokens, current)
        return SmtLibCommand(current, expr)

    def _cmd_push_cube(self, current, tokens):
        pass

    def get_script(self, script):
        """
        Takes a file object and returns a SmtLibScript object representing
        the file
        Turn off reset to remember state
        """
#         self._reset() # prepare the parser
        res = SmtLibScript()
        for cmd in self.get_command_generator(script):
            res.add_command(cmd)
        res.annotations = self.cache.annotations
        return res

    
    def parse_check_sat_expr_list(self, tokens, command):
        """Parses a list of expressions form the tokens"""
        res = []
        while True:
            try:
                current = self.get_expression(tokens)
                res.append(current)
                logger.debug(current)
            except PysmtSyntaxError:
                return res
