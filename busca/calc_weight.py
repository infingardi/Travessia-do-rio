from busca.helpers import get_rule_from_states


def get_state_weight(state):
  left, right, boat_side = state
  return len(right)

def get_rule_weight(state_before, state_after):
  boat = get_rule_from_states(state_before, state_after)
  base_value = 1 if state_before[2] == "esquerda" else -1
  value = len(boat) * base_value
  for p in boat:
    if p in ["prisioneira", "policial"]:
      value += 1
  return value