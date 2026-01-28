export function processSlot(state: BeaconState): void {
  const previousStateRoot = hashTreeRoot(state);
  state.stateRoots[state.slot % SLOTS_PER_HISTORICAL_ROOT] = previousStateRoot;
  if (byteArrayEquals(state.latestBlockHeader.stateRoot, ZERO_HASH)) {
    state.latestBlockHeader.stateRoot = previousStateRoot;
  }
  const previousBlockRoot = hashTreeRoot(state.latestBlockHeader);
  state.blockRoots[state.slot % SLOTS_PER_HISTORICAL_ROOT] = previousBlockRoot;
}

export function getActiveValidatorIndices(state: BeaconState, epoch: Epoch): ValidatorIndex[] {
  const indices: ValidatorIndex[] = [];
  for (let i = 0; i < state.validators.length; i++) {
    if (isActiveValidator(state.validators[i], epoch)) {
      indices.push(i);
    }
  }
  return indices;
}

function internalHelper(): void {
  // not exported
}
