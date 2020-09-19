"""The following test presents a simple example of an agent with two
states, smart and dumb, and transitions between the two based on
consuming TV/电视 or studying/学习 as input

"""

import pytest

# the dialomata agent is a generalized pushdown automaton (GPDA)
from dialomata import gpda
machine = gpda.GPDA()



# One component of the GPDA is states.  This GPDA agent can be either
# smart or dumb

dumb = machine.add_state(gpda.State("傻瓜"))
smart = machine.add_state(gpda.State("聪明"))

def test_is_state():
    """Test the types of the states"""
    assert isinstance(smart, gpda.State)
    assert isinstance(dumb, gpda.State)

# Another component of the GPDA is transitions.  TV (电视) makes the
# agent dumb, studying (学习) makes it smart.  Transitions are
# dependent on the current state and the input

machine.add_transition(smart, dumb,
                       test=lambda inp: inp == "电视",
                       function= lambda inp: f"{inp} made me dumb")
def test_tv_makes_smart_agent_dumb():
    machine.set_state(smart)
    machine("电视")
    assert machine.state == dumb

machine.add_transition(dumb, smart,
                       test=lambda inp: inp == "学习",
                       function= lambda inp: f"{inp} made me dumb")

def test_tv_makes_dumb_agent_smart():
    machine.set_state(dumb)
    machine("学习")
    assert machine.state == smart

# To be complete, we should have self transitions, if not, there is no
# valid transition when a dumb agent watches TV, or for a smart agent
# studying:
    
# when a dumb agent watches more tv, they stay dumb
machine.add_transition(dumb, dumb,
                       test=lambda inp: inp == "电视",
                       function= lambda inp: f"{inp} made me dumb")

# when a smart agent studies more, they stay smart
machine.add_transition(smart, smart,
                       test=lambda inp: inp == "学习",
                       function= lambda inp: f"{inp} made me dumb")

def test_dumb_and_smart_self_transitions():
    machine.state = smart
    machine("学习")
    assert machine.state == smart
    machine.state = dumb
    machine("电视")
    assert machine.state == dumb
    
    
# the agent doesn't know that practicing also makes you smart and
# drinking beer also makes you dumb
def test_no_valid_transition_for_unknown_input():
    machine.set_state(smart)
    with pytest.raises(gpda.GPDAError):
        machine("练习")
    machine.set_state(dumb)
    with pytest.raises(gpda.GPDAError):
        machine("啤酒")
