# Verified releases and Zenodo

The workflows belong only to this repository. They do not call workflows in
trureturing and do not depend on a private Mac Studio or other personal runner.

1. Push a change to main or open a pull request. Verification checks saved
   evidence, fresh finite computations, the Lean theorem, and the paper build.
2. Choose an intentional version and push its tag, for example `v0.1.0`.
   The release workflow runs the same complete verification for that tag.
3. Only after all jobs succeed, the workflow builds source/research ZIPs and
   publishes a GitHub Release with the PDF, archives and SHA256 checksums.
   A failed verification prevents release publication.
4. Enable this repository once in the authenticated Zenodo GitHub settings:
   https://zenodo.org/account/settings/github/
   GitHub organization authorization alone does not enable a new repository.
5. Zenodo receives future published releases, imports the tagged repository
   and its `.zenodo.json`, and creates the archive/DOI. Verify its record before
   adding the version DOI to citations. Record both version and concept DOI.

The `.zenodo.json` describes this software/research artifact, not an approved
joint journal manuscript. Never add a guessed DOI or someone as an author
solely because they proposed a problem. The current creator is Wenlin Zhang;
Sahbi's work is a related reference.

If Zenodo is enabled after a release, publish a new patch release after the
connection is active. Existing published tags and deposited records remain
immutable. DOI archival is driven by explicit version releases, not every commit.
