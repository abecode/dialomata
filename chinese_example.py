#!/usr/bin/env python3

"""a simple automaton that has the following states
     - 傻瓜 (stupid)
     - 聪明 (smart)

and consumes the following symbols:
     - 学习，练习 (studying, practicing)
     - 电视，喝啤酒 (TV, drinking beer)
     - 睡觉，休息 (sleeping, resting)

The basic idea is that you can get smart from studying or practicing
and get stupid from watching TV or drinking beer.  However, you can't
study or practice too much in a row without sleeping or taking a
break.

The disable directives for pylint are needed because of the monkey
patched approach.

"""

from functools import reduce

from dialomata import gpda


machine = gpda.GPDA()

dumb = machine.add_state(gpda.State("傻瓜"))
smart = machine.add_state(gpda.State("聪明"))

def is_okay_to_have_fun(inp):
    #pylint: disable=undefined-variable
    """checks to see if it's okay to have fun

    I.e., if the current state is not stupidity and input is something
    fun like drinking beer or watching tv.

    Note: the 'self' variable becomes available when the function is
    monkey patched to the State class

    """
    print("is okay to have fun")
    if machine.state.name != "傻瓜" and inp in ("啤酒", "电视"):
        return True
    return False

def is_trying_to_get_smart(inp):
    #pylint: disable=undefined-variable
    """checks to see if the automaton is trying to get smart

    I.e., current state is stupidity and input is studying or
    practicing

    """
    print("is trying to get smart")
    if machine.state.name == "傻瓜"  and inp in ("学习", "练习") and reduce(sum, machine.stack) < 3:
        #self.stack.append(1)
        return True
    return False

def needs_a_break(inp):
    #pylint: disable=undefined-variable
    #pylint: disable=unused-argument
    """check to see if the automaton needs a break

    I.e. if the previous 4 stack items are studying or practicing

    Note: the stack is added to when there is a transition between
    states via the function get_smarter

    """
    print("needs a break")
    if machine.stack[-3:] == [1, 1, 1]:
        return True
    return False

def get_stupider(inp):
    #pylint: disable=undefined-variable
    #pylint: disable=unused-argument
    """When you drink beer or watch TV, -1 is appended to the stack
    """
    machine.append(-1)
    return "%s makes you stupider, try studying or practicing"%inp

def get_smarter(inp):
    #pylint: disable=undefined-variable
    #pylint: disable=unused-argument
    """When you study or practice, 1 is appended to the stack

    Note: 0 is added to the stack when sleeping or resting.  This is
    done in a lambda function in a transition

    """
    machine.append(1)
    return "%s makes you smarter, good!"

machine.add_transition(dumb, dumb,
                       test=lambda inp: not is_okay_to_have_fun(inp),
                       function=get_stupider)

machine.add_transition(dumb, dumb,
                       test=lambda inp: is_trying_to_get_smart(inp) and \
                       not needs_a_break(inp),
                       function=get_smarter)

machine.add_transition(dumb, dumb,
                       test=lambda inp: inp in ("睡觉", "休息"),
                       function=lambda inp: machine.append(0) and "Ah, I feel refreshed")

machine.add_transition(smart, smart,
                       test=lambda inp: inp in ("睡觉", "休息"),
                       function=lambda inp: machine.append(0) and "Ah, I feel refreshed")

machine.add_transition(smart, smart,
                       test=lambda inp: inp in ("学习", "练习") and \
                                      needs_a_break(inp),
                       function=lambda inp: machine.append(1) and "Ouch, my head hurts, I need a break")

machine.add_transition(smart, smart,
                       test=lambda inp: inp in ("学习", "练习") and \
                                      not needs_a_break,
                       function=lambda inp: machine.append(1) and "Ah, I feel smarter")

machine.add_transition(dumb, smart,
                       test=lambda inp: inp in ("学习", "练习") and \
                                      reduce(sum, machine.stack, 0) >= 0,
                       function=lambda inp: machine.append(1) and "Good, now I'm smart")

machine.add_transition(smart, dumb,
                       test=lambda inp: inp in ("啤酒", "电视") and \
                                      reduce(sum, machine.stack, 0) <= 0,
                       function=lambda inp: "%s made me stupid, I need to study or practice")


if __name__ == "__main__":
    machine.set_state(dumb)
    #machine.state.name
    print("Hello, I am an automaton that can study, practice, drink beer, watch TV, ",
          "sleep, and rest, (学习，练习，喝啤酒，电视，睡觉，and 休息，respectively)")
    while True:
        print(machine(input("what should I do now\n")))
        print(machine.state, machine.stack)
