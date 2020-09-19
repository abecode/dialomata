"""the following test an advanced case where the agent has the same
two states as the simple example, smart and dumb, and like the
intermediate example they can't transition immediately between smart
and dumb, but now the agent needs a break when studying: it cannot
study three times in a row without watching tv at least once.

Note: it may be better to simulate such an agent using two machines,
one for smart/dumb and another for rested/tired.  This is just an
illustration.

"""

from functools import reduce
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


def global_command(inp):
    if machine.stack[-2:] == [1, 1] and inp == "学习":
        raise(gpda.GPDAError(f"Too much {inp} makes me tired") )

def test_dumb_requires_studying_three_times_not_in_a_row():
    machine.state = dumb
    machine.stack = []
    # monkey patch the process_global_command
    machine.process_global_command = global_command
    output = machine("学习")
    assert machine.state == dumb
    assert output == "学习 makes me smart but I'm not smart yet"
    output = machine("学习")
    assert machine.state == dumb
    assert output == "学习 makes me smart but I'm not smart yet"
    with pytest.raises(gpda.GPDAError) as e:
        output = machine("学习")
    assert e.value.args[0] == 'Too much 学习 makes me tired'
    output = machine("电视")
    assert machine.state == dumb
    output = machine("学习")
    assert machine.state == dumb
    output = machine("学习")
    assert machine.state == smart    



    
