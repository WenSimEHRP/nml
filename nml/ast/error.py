from nml import generic, expression
from nml.actions import actionB

class Error(object):
    """
    An error has occured while parsing the GRF. This can be anything ranging from
    an imcompatible GRF file that was found or a game setting that is set to the
    wrong value to a wrong combination of parameters. The action taken by the host
    depends on the severity level of the error.
    NML equivalent: error(level, message[, extra_text[, parameter1[, parameter2]]]).

    @ivar params: Extra expressions whose value can be used in the error string.
    @type params: C{list} of L{Expression}

    @ivar severity: Severity level of this error, value between 0 and 3.
    @type severity: L{Expression}

    @ivar msg: The string to be used for this error message. This can be either
               one of the predifined error strings or a custom string from the
               language file.
    @type msg: L{Expression}

    @ivar data: Optional extra message that is inserted in place of the second
                {STRING}-code of msg.
    @type data: C{None} or L{String} or L{StringLiteral}

    @ivar pos: Position information of this error block.
    @type pos: L{Position}
    """
    def __init__(self, param_list, pos):
        self.params = []
        self.pos = pos
        if not 2 <= len(param_list) <= 5:
            raise generic.ScriptError("'error' expects between 2 and 5 parameters, got " + str(len(param_list)), self.pos)
        self.severity = param_list[0].reduce([actionB.error_severity])
        self.msg      = param_list[1].reduce([actionB.default_error_msg])
        self.data     = param_list[2].reduce() if len(param_list) >= 3 else None
        self.params.append(param_list[3].reduce() if len(param_list) >= 4 else None)
        self.params.append(param_list[4].reduce() if len(param_list) >= 5 else None)

    def pre_process(self):
        pass

    def debug_print(self, indentation):
        print indentation*' ' + 'Error message'
        print (indentation+2)*' ' + 'Message:'
        self.msg.debug_print(indentation + 4)
        print (indentation+2)*' ' + 'Severity:'
        self.severity.debug_print(indentation + 4)
        print (indentation+2)*' ' + 'Data: '
        if self.data is not None: self.data.debug_print(indentation + 4)
        print (indentation+2)*' ' + 'Param1: '
        if self.params[0] is not None: self.params[0].debug_print(indentation + 4)
        print (indentation+2)*' ' + 'Param2: '
        if self.params[1] is not None: self.params[1].debug_print(indentation + 4)

    def get_action_list(self):
        return actionB.parse_error_block(self)

    def __str__(self):
        sev = str(self.severity)
        if isinstance(self.severity, expression.ConstantNumeric):
            for s in actionB.error_severity:
                if self.severity.value == actionB.error_severity[s]:
                    sev = s
                    break
        res = 'error(%s, %s' % (sev, self.msg)
        if self.data is not None:
            res += ', %s' % self.data
        if self.params[0] is not None:
            res += ', %s' % self.params[0]
        if self.params[1] is not None:
            res += ', %s' % self.params[1]
        res += ');\n'
        return res
