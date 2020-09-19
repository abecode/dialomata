#!/usr/bin/env python3

"""a generalized pushdown automaton is a pushdown automaton that can look
at its whole stack.

in the case of a dialog agent, the stack like an episodic buffer
(short term memory)

"""
from collections import OrderedDict
import networkx as nx

class GPDAError(Exception):
    """ An error for a GPDA"""


class State(): # pylint: disable=too-few-public-methods
    """a state in a generalized push down automata"""
    def __init__(self, name):
        """ set the state name """
        self.name = name
        self.neighbors = OrderedDict()

    def __repr__(self):
        return "State:%s" %self.name


class GPDA(nx.MultiDiGraph):
    """
    a generalized push down automata

    # create the machine
    >>> machine = GPDA()

    # add states...
    >>> machine.add_state("perdition")
    Traceback (most recent call last):
    ...
    TypeError

    # oops, states must be states
    # do it the right way
    >>> s = State("salvation")
    >>> machine.add_state(s)
    State:salvation
    >>> p = State("perdition")
    >>> machine.add_state(p)
    State:perdition

    # add transitions
    >>> machine.add_transition(s, p,
    ...   test=lambda x: True if x=="TV" or x=="high fructose corn syrup" else False,
    ...   function=lambda x: "%s makes your brain rot. you are going to hell."%str(x) )


    # set state
    >>> machine.set_state(s)

    # give input "TV" and print the output:
    >>> print(machine("TV"))
    TV makes your brain rot. you are going to hell.
    >>> print(machine.state.name)
    perdition

    # the new state doesn't accept the same inputs as the old state
    >>> print(machine("TV"))
    Traceback (most recent call last):
    ...
    GPDAError: no valid transition using input TV
    given current state perdition
    and neighbors: 
    with stack 

    # get back into shape
    >>> machine.add_transition(p, s,
    ...   test=lambda x: True \
                if (x == "carrots" or x == "exercise") and len(machine.stack) > 5\
                else False,
    ...   function=lambda x: "congratulations, you attained salvation")
    >>> def getInShape(x):
    ...   machine.stack.append(x)
    ...   return "that helps but it's not enough"
    >>> machine.add_transition(p, p,
    ...   test=lambda x: True \
                if (x == "carrots" or x == "exercise") and len(machine.stack) <= 5\
                else False,
    ...   function=getInShape)
    >>> print(machine("carrots"))    # one
    that helps but it's not enough
    >>> print(machine("carrots"))    # two
    that helps but it's not enough
    >>> print(machine("exercise"))   # three
    that helps but it's not enough
    >>> print(machine("carrots"))    # four
    that helps but it's not enough
    >>> print(machine("carrots"))    # five
    that helps but it's not enough
    >>> print(machine("carrots"))
    that helps but it's not enough
    >>> print(machine("carrots"))
    congratulations, you attained salvation

    # we don't want to be too healthy
    >>> print(machine("carrots"))
    Traceback (most recent call last):
    ...
    GPDAError: no valid transition using input carrots
    given current state salvation
    and neighbors: perdition
    with stack carrots, carrots, exercise, carrots, carrots, carrots


    # oops, need a valid transition
    >>> machine.add_transition(s, s,
    ...   test = lambda x: True if x=="carrots" or x=="exercise"  else False,
    ...   function = lambda x: "don't overdo it")
    >>> print(machine("carrots"))
    don't overdo it


    """
    stack = []

    def __call__(self, input_):
        """this is where the gpda consumes input"""
        #catch special commands here
        self.process_global_command(input_)
        for neighbor in self[self.state]:   #check neighbor states
            for edge in self[self.state][neighbor]:
                if self[self.state][neighbor][edge]['test'](input_):
                    #print(self.state, neighbor, edge)
                    output = self[self.state][neighbor][edge]['function'](input_)
                    self.set_state(neighbor)
                    return output
        raise GPDAError("no valid transition using input %s\n"
                        "given current state %s\n" 
                        "and neighbors: %s\n"
                        "with stack %s" %
                        (input_,
                         self.state.name,
                         ", ".join([x.name for x in self.neighbors(self.state)]),
                         ", ".join([str(x) for x in self.stack]),
                        ))
        # raise GPDAError("no valid transition using this input, "
        #                 "given current state %s " 
        #                 "and neighbors: %s" %
        #                 (self.state.name,
        #                  ", ".join([x.name for x in self.neighbors(self.state)])))

    def process_global_command(self, input_):
        """placeholder to respond to input in any state"""

    def __init__(self):
        super(GPDA, self).__init__()

    def add_state(self, state):
        """add a state to the gpda"""
        if not isinstance(state, State):
            raise TypeError()
        self.add_node(state)
        return state

    def add_transition(self, state1, state2,
                       test=lambda *args: True,
                       function=lambda *args: ""):
        """add transitions between gpda states

        the test must return true for the state to be considered

        the function provides the states output
        """
        if not isinstance(state1, State):
            raise TypeError()
        if not isinstance(state2, State):
            raise TypeError()
        self.add_edge(state1, state2, test=test, function=function)

    def set_state(self, state):
        """set's the  current state of the gpda"""
        if state not in self.nodes():
            raise GPDAError()
        self.state = state
    def append(self, value):
        """this appends a value to the machine's stack.

        It returns True always, which is useful when using in a lambda
        statement in add_transition

        """
        self.stack.append(value)
        return True

if __name__ == "__main__":
    import doctest
    doctest.testmod()
