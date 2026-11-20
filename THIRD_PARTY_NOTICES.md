# Third-party notices and license boundaries

This repository is a curated library. Inclusion does not mean Luo Kai authored or owns every included skill.

## Ownership classes

| Class | Meaning | Rights treatment |
|---|---|---|
| Original | Independently written for this repository by Luo Kai | Covered by the repository COPYRIGHT.md notice unless a file says otherwise |
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

    metadata:
      author: Luo Kai
      provenance: original
      version: "1.0.0"

This metadata is a provenance statement, not a substitute for reviewing copied code, assets, or text. Keep separate third-party notices whenever a skill includes third-party material.


## PinkPixel source license audit (2026-11-19)

The PinkPixel entry was previously labeled MIT in SOURCES.md. Inspection of the upstream repository's LICENSE history found that its Apache-2.0 LICENSE was added in commit ddcadf5896a9cce6f79e296d8b070e5224690e6e on 2026-08-09. The current upstream repository declares Apache-2.0. A copy of that LICENSE is preserved at ai-agent-skills/21-external-registries/08-pinkpixel-collection/LICENSE.

The exact upstream commit from which this repository's imported snapshot was copied is not recorded. Individual files may also contain separate notices. Do not assume that this collection-level license overrides a more specific third-party notice; verify per-entry provenance before adapting any file.

## 2026 source license audit summary

The repository-level COPYRIGHT.md notice identifies Luo Kai's ownership of original material. It does not relicense third-party skills or grant a license to original work.

- Verified collection-level license files have been copied into their corresponding source directories. Nested per-skill licenses override collection-level terms.
- Anthropic, Replicate, and Strativd have per-skill licensing only; no blanket license has been applied.
- The Rushikeshpol source could not be retrieved and has no verified license.
- The Travisvn source has no explicit license grant in the checked repository contents.
- Hesreallyhim is CC BY-NC-ND 4.0: non-commercial use only, no derivatives or adaptations, attribution required.
- MicrosoftDocs is CC BY 4.0; SkillsDirectory is CC0 1.0.
- Apache-2.0 and MIT sources retain their upstream notices. Luo Kai's changes are marked as modifications, not exclusive ownership of upstream work.

Unverified material must not be sold, adapted, or described as exclusively owned by Luo Kai until its rights are confirmed.

## Luo Kai original-work scope

The repository's COPYRIGHT.md notice applies to original Luo Kai material at the 18 Luo Kai-labeled collection roots. It does not apply to source-linked, adapted, unattributed, or independently licensed material. Original skills carry no license field; per-skill `LICENSE_STATUS.md` files and upstream notices preserve third-party rights.

ClawSkills/ClawHub community imports have no blanket collection-level license. Their licenses must be verified per skill; unverified entries must not be adapted, sold, or redistributed as Luo Kai-owned work.
