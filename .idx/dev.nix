{ pkgs, ... }: {
  channel = "stable-23.11"; # or "unstable"

  packages = [
    pkgs.nodejs_20
  ];

  env = {
    MONGODB_CONNECTION_STRING = "mongodb://localhost:27017/library";
  };

  services.mongodb = {
    enable = true;
  };

  idx = {
    extensions = [
      # TODO: Add MongoDB Extension
    ];

    workspace = {
      onCreate = {
        npm-install = "npm install";
        default.openFiles = [
          "index.js" "README.md"
        ];
      };
      onStart = {
        run-index = "node index.js";
      };
    };

    previews = {
      enable = true;
      previews = {
      };
    };
  };
}
