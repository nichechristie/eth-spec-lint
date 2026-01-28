# Beacon Chain Spec (Sample)

## Constants

```python
SLOTS_PER_EPOCH = 32
MAX_VALIDATORS_PER_COMMITTEE = 2048
BASE_REWARD_FACTOR = 64
```

## Containers

```python
class BeaconBlockHeader:
    slot: Slot
    proposer_index: ValidatorIndex
    parent_root: Root
    state_root: Root
    body_root: Root
```

## State Transition

```python
def process_slot(state: BeaconState) -> None:
    # Cache state root
    previous_state_root = hash_tree_root(state)
    state.state_roots[state.slot % SLOTS_PER_HISTORICAL_ROOT] = previous_state_root
    # Cache latest block header state root
    if state.latest_block_header.state_root == Bytes32():
        state.latest_block_header.state_root = previous_state_root
    # Cache block root
    previous_block_root = hash_tree_root(state.latest_block_header)
    state.block_roots[state.slot % SLOTS_PER_HISTORICAL_ROOT] = previous_block_root
```

```python
def get_active_validator_indices(state: BeaconState, epoch: Epoch) -> Sequence[ValidatorIndex]:
    return [i for i, v in enumerate(state.validators) if is_active_validator(v, epoch)]
```
