{
    description = "Advent of Code Shell for NixOS";
    inputs = {
      nixpkgs.url = "github:Princemachiavelli/nixpkgs/nixos-unstable";
      flake-utils.url = "github:numtide/flake-utils";
    };

    outputs = { self, nixpkgs, flake-utils }:
      flake-utils.lib.simpleFlake {
        name = "advent-of-code-flake";
        inherit self nixpkgs;
        shell = ./shell.nix;
      };
}
