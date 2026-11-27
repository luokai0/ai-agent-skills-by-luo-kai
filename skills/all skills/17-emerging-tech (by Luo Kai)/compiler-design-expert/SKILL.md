---
name: compiler-design-expert
version: 1.0.0
description: Expert-level compiler design covering lexical analysis, parsing, semantic analysis, intermediate representations, optimization passes, and code generation.
author: luo-kai
tags: [compilers, parsing, AST, optimization, code generation, LLVM]
---

# Compiler Design Expert

## Before Starting
1. Which compilation phase?
2. New language or existing compiler modification?
3. Optimization or correctness focus?

## Core Expertise Areas

### Lexical Analysis
Tokens: atomic units — keywords, identifiers, literals, operators.
Regular expressions: define token patterns.
Finite automata: DFA and NFA implement lexers.
Lexer generators: Lex, Flex, ANTLR — generate lexer from token rules.

### Parsing
Context-free grammars: productions defining language syntax.
Top-down: recursive descent, LL parsers — predictive, left-to-right.
Bottom-up: LR parsers — shift-reduce, more powerful, handles more grammars.
Parser generators: Yacc, Bison, ANTLR — generate parser from grammar.
Parse tree vs AST: AST removes redundant nodes, better for analysis.

### Semantic Analysis
Type checking: static vs dynamic typing, type inference.
Symbol table: scope management, variable binding, type lookup.
Attribute grammars: synthesized and inherited attributes on parse tree.
Name resolution: binding identifiers to declarations.

### Intermediate Representation
Three-address code: at most three operands per instruction.
SSA form: single static assignment, each variable defined exactly once.
LLVM IR: typed, SSA-based, platform-independent, widely used.
Control flow graph: basic blocks connected by edges.

### Optimization
Constant folding: evaluate constant expressions at compile time.
Dead code elimination: remove unreachable or unused code.
Common subexpression elimination: compute repeated expressions once.
Loop optimizations: unrolling, invariant code motion, vectorization.
Inlining: replace function call with function body.

### Code Generation
Instruction selection: map IR to target instructions.
Register allocation: map variables to physical registers, spill to stack.
Instruction scheduling: reorder instructions to minimize pipeline stalls.

## Best Practices
- Separate phases clearly for maintainability
- Use SSA form for most optimization passes
- Test with both valid and invalid input programs
- Profile optimization passes on real workloads

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Shift-reduce conflicts | Refactor grammar or use precedence declarations |
| Missing phi nodes in SSA | Compute dominance frontiers correctly |
| Unsafe optimizations | Prove correctness of each transformation |
| Register spill storm | Improve register allocator or reduce register pressure |

## Related Skills
- compiler-expert
- algorithms-cs-expert
- computer-architecture-expert
