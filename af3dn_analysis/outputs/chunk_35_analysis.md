## Analysis Summary

**Chunk 35 contains 30 functions (addresses 1003DF40–1003E645), all compiler-generated C++ runtime support code.**

### Key Patterns Identified

1. **Exception Handler Initialization Chain** (6 functions): sub_1003DF90 through sub_1003DFE0 - These register cleanup functions via `atexit()` for various exception handlers.

2. **Dynamic Object Initialization** (3 functions): sub_1003DF40, sub_1003DFF0, sub_1003E040 - Allocate 4-byte objects and register atexit cleanup handlers.

3. **String Buffer Management** (11 functions): sub_1003E100, sub_1003E3A0 through sub_1003E4E0, sub_1003E610 - Implement C++ std::string Small String Optimization (SSO) cleanup with thresholds at 8 or 16 bytes.

4. **Resource Cleanup Sequences** (9 functions): sub_1003E0B0 through sub_1003E5E0 - Call cleanup functions before deallocating associated memory blocks.

5. **Standard Library Support** (1 function): sub_1003E645 - Initializes std::bad_alloc exception object with vftable.

### Technical Observations

- All functions are callback wrappers for C++ static object destruction
- Repetitive patterns indicate compiler code generation for multiple template instantiations
- SSO (Small String Optimization) buffers managed with size thresholds (8-byte or 16-byte limits)
- Cleanup functions called before deallocation suggest wrapped C++ objects with destructors
- This is the final shutdown phase of the AF3DN.P DLL - program-exit cleanup code
