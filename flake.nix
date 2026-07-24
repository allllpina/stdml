{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
    in {
      devShells."x86_64-linux" = {
        
        default = pkgs.mkShell {
          packages = with pkgs; [
            # Base utils
            git
            just
            
            # Python ecosystem
            python312
            uv
            
            # K8s infrastructure
            k3d
            kubectl
            kubernetes-helm
            
            # Hot Reload tool
            tilt
          ];

          shellHook = ''
            export UV_PYTHON_PREFERENCE="system"
          '';
        };

        ml = pkgs.mkShell {
          packages = with pkgs; [
          ];
        };
      };
    };
}