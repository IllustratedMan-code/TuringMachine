{
  description = "";
  inputs = { flake-utils.url = "github:numtide/flake-utils"; };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages."${system}"; in
      rec {
        packages = flake-utils.lib.flattenTree {
          default = with pkgs.python3.pkgs; buildPythonPackage {
            name = "turing-1.0.0";
            src = ./.;
            format = "pyproject";
            propagatedBuildInputs = [ setuptools graphviz matplotlib ];
          };
        };
        devShells = {
          default = with pkgs; mkShell {
            packages = [ (pkgs.python3.withPackages (p: with p; [ packages.default ])) ];
          };
        };
      }
    );
}

