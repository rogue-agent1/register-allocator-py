#!/usr/bin/env python3
"""Register allocator — graph coloring with spilling."""
def allocate_registers(interference, num_regs):
    """interference = {var: set of conflicting vars}. Returns {var: reg} or None for spills."""
    vars_list=list(interference);alloc={};stack=[]
    remaining=dict(interference)
    # Simplify: remove nodes with degree < num_regs
    changed=True
    while changed:
        changed=False
        for v in list(remaining):
            if len(remaining[v]&set(remaining))<num_regs:
                stack.append(v);del remaining[v];changed=True
    # Remaining are potential spills
    spills=set(remaining)
    for v in remaining:stack.append(v)
    # Color
    for v in reversed(stack):
        used={alloc[n] for n in interference.get(v,set()) if n in alloc}
        for r in range(num_regs):
            if r not in used:alloc[v]=r;break
        else:alloc[v]=-1  # spill
    return alloc
def main():
    ig={"a":{"b","c"},"b":{"a","c","d"},"c":{"a","b"},"d":{"b"}}
    alloc=allocate_registers(ig,3)
    print(f"Allocation: {alloc}")
if __name__=="__main__":main()
