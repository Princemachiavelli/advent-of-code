{
    description = "Advent of Code Shell for NixOS";
    inputs = {
      nixpkgs.url = "github:nixos/nixpkgs/release-21.11";
      flake-utils.url = "github:numtide/flake-utils";
    };

    outputs = { self, nixpkgs, flake-utils }:
      flake-utils.lib.simpleFlake {
        name = "advent-of-code-flake";
        inherit self nixpkgs;
        shell = ./shell.nix;
      };
}
