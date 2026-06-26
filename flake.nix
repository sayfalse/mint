{
  description = "MINT — The Unified OSINT & Media Command Center";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python3;
      in
      rec {
        packages.default = python.pkgs.buildPythonApplication {
          pname = "mint-osint";
          version = "1.0.0";
          src = ./.;

          propagatedBuildInputs = [
            python.pkgs.colorama
          ];

          # Disable tests since we don't have python tests configured in the package yet
          doCheck = false;

          meta = with pkgs.lib; {
            description = "The Unified OSINT & Media Command Center";
            homepage = "https://github.com/sayfalse/mint";
            license = licenses.mit;
            platforms = platforms.all;
          };
        };

        apps.default = flake-utils.lib.mkApp {
          drv = packages.default;
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [
            python
            python.pkgs.colorama
          ];
        };
      });
}
