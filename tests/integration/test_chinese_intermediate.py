"""the following test an intermediate case where the agent has the
same two states as the simple example, smart and dumb, but now a dumb
agent can't get smart right away, and a smart agent can't get dumb
right away.  Rather, they require studying or watching TV three times
to get smart or dumb, respectively.  This illustrates the use of the
stack.  Note: a similar example could have been created with a signed
counter instead of a stack.  While the signed counter is a good
example of automaton theory, we aren't using it because for our dialog
agent, the stack will be more useful.

"""

import pytest

from dialomata import gpda

machine = gpda.GPDA()
dumb = machine.add_state(gpda.State("傻瓜"))
smart = machine.add_state(gpda.State("聪明"))
machine.add_transition(smart, dumb,
                       test=lambda inp: inp == "电视" and \
                       sum(machine.stack) <= -2,
                       function= lambda inp: machine.append(-1) and \
                       f"{inp} made me dumb")
machine.add_transition(dumb, smart,
                       test=lambda inp: inp == "学习" and \
                       sum(machine.stack) >= 2,
                       function= lambda inp: machine.append(1) and \
                       f"{inp} made me smart")
machine.add_transition(dumb, dumb,
                       test=lambda inp: inp == "电视",
                       function= lambda inp: machine.append(-1) and \
                       f"{inp} makes me dumb")
machine.add_transition(smart, smart,
                       test=lambda inp: inp == "学习",
                       function= lambda inp: machine.append(1) and \
                       f"{inp} makes me smart")
# now the agent can study while dumb and won't get smart right away
# until the sum of the stack is >=3.  Note: there are now two
# dumb->dumb transitions.  This means that the underlying graph
# structure is a multidigraph (i.e. networkx.MultiDiGraph)
machine.add_transition(dumb, dumb,
                       test=lambda inp: inp == "学习" and \
                       sum(machine.stack) < 3,
                       function= lambda inp: machine.append(1) and \
                       f"{inp} makes me smart but I'm not smart yet")
machine.add_transition(smart, smart,
                       test=lambda inp: inp == "电视" and \
                       sum(machine.stack) > -3,
                       function= lambda inp: machine.append(-1) and \
                       f"{inp} makes me dumb but I'm not dumb yet")

def test_dumb_and_smart_self_transitions():
    """ These transitions should still work as before"""
    machine.state = smart
    machine("学习")
    assert machine.state == smart
    machine.state = dumb
    machine("电视")
    assert machine.state == dumb
    
def test_dumb_requires_studying_three_times():
    machine.state = dumb
    machine.stack = []
    output = machine("学习")
    assert machine.state == dumb
    assert output == "学习 makes me smart but I'm not smart yet"
    output = machine("学习")
    assert machine.state == dumb
    assert output == "学习 makes me smart but I'm not smart yet"
    output = machine("学习")
    assert machine.state == smart
    assert output == "学习 made me smart"

def test_smart_requires_tv_three_times():
    machine.state = smart
    machine.stack = []
    output = machine("电视")
    assert machine.state == smart
    assert output == "电视 makes me dumb but I'm not dumb yet"
    output = machine("电视")
    assert machine.state == smart
    assert output == "电视 makes me dumb but I'm not dumb yet"
    output = machine("电视")
    assert machine.state == dumb
    assert output == "电视 made me dumb"

    
