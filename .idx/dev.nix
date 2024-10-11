{ pkgs, ... }: {
  channel = "stable-23.11";

  packages = [
    pkgs.nodejs_22
  ];

  env = {
    MONGODB_CONNECTION_STRING = "mongodb://localhost:27017/";
  };

  services.mongodb = {
    enable = true;
  };

  idx = {
    extensions = [
      "mongodb.mongodb-vscode"
    ];

    workspace = {
      onCreate = {
        npm-install = "npm install";
        default.openFiles = [
          "index.js" "README.md"
        ];
      };
      onStart = {
        start-database = "mongod --port 27017 --fork --logpath ./.idx/database.log --dbpath ./.idx/.data";
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
