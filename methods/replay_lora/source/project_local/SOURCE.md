# Replay LoRA Project-Local Source

No separate official Replay LoRA repository was verified. This directory adds the project-local baseline implementation and published-setting configs from `/root/autodl-tmp/Lora-code` commit `d711d912926c58c13acc02b3c3e4cfddd9f2c969`. The official O-LoRA paper baseline source remains vendored at `methods/o_lora/source`.

This directory is one closest reproducible path. The ACL software package for "Unlocking Continual Learning Abilities in Language Models" is also vendored at `../acl_software_unlocking_cl` as a paper/software source for LoRA Replay and LoRA Replay + MIGU. See `../../REPRODUCIBILITY.md` for the required replay-buffer modifications and source caveats.
