# Third-party notices and license boundaries

This repository is a curated library. Inclusion does not mean Luo Kai authored or owns every included skill.

## Ownership classes

| Class | Meaning | Rights treatment |
|---|---|---|
| Original | Independently written for this repository by Luo Kai | Covered by the repository LICENSE unless a file says otherwise |
| Adapted | Based on upstream material under a license permitting the specific adaptation and redistribution | Keep upstream attribution, license text, notices, and source reference; identify the adaptation |
| Third-party | Imported or mirrored without substantive original authorship | Keep the original author's copyright and license unchanged |
| Unverified | Provenance or redistribution rights are unclear | Do not claim ownership, remove notices, or redistribute further until reviewed |

## Collection boundaries

- ai-agent-skills/21-external-registries/ contains material collected from external projects and registries.
- ai-agent-skills/22-clawhub-skills/ contains skills from the ClawHub ecosystem. Each entry must retain its original author, source, and license information where supplied.
- Numbered subject collections are organizational categories. A parent folder containing “by Luo Kai” is not, by itself, proof that every nested work is original.
- Git submodules remain separate upstream projects at their pinned commits. Their upstream licenses and notices continue to apply.

## Rules for maintainers

1. Never replace an upstream copyright holder with Luo Kai.
2. Never add a proprietary or All Rights Reserved notice to third-party material unless the rights holder explicitly authorizes it.
3. Before adapting an entry, verify the license in the upstream repository at the relevant revision. A missing license is not permission.
4. Preserve required attribution, license copies, NOTICE files, source links, and modification notices.
5. If the license does not permit redistribution or adaptation, do not copy or modify the work. Prefer an independently written implementation based on general ideas and public documentation, without copying protected expression.
6. Record original work as provenance: original; adapted work as provenance: adapted with source and license; imported work as provenance: third-party.
7. If provenance cannot be established, record provenance: unverified and keep it out of any claim that the entire library is exclusively owned by Luo Kai.

## Per-skill metadata

New original skills use this metadata pattern:

    license: Proprietary. See repository LICENSE
    metadata:
      author: Luo Kai
      provenance: original
      version: "1.0.0"

This metadata is a provenance statement, not a substitute for reviewing copied code, assets, or text. Keep separate third-party notices whenever a skill includes third-party material.
