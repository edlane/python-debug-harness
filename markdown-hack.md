
```.                 _ENVIRONMENT_                      .
```


| *life cycle*          | dev | demo | qa |   | enterprise |
|-----------------------|-----|:----:|----|---|------------|
| repo                  |     |   x  |    |   |            |
| create cluster        |     |   x  |    |   |            |
| install packages      |     |   x  |    |   |            |
| configure/orchestrate |     |   x  |    |   |            |
| startup cluster       |     |   x  |    |   |            |
| stop cluster          |     |   x  |    |   |            |
|                       |     |      |    |   |            |
| destroy cluster       |     |   x  |    |   |            |

```
├── raas-repo-local
└── salt
    ├── apache
    │   └── init.sls
    ├── deploy
    │   ├── cluster-config.sls
    │   ├── cluster-create.sls
    │   ├── cluster-destroy.sls
    │   ├── cluster-down.sls
    │   ├── cluster-install.sls
    │   ├── cluster-raas-repo-mount.sls
    │   ├── cluster-repo.sls
    │   ├── cluster-start.sls
    │   ├── cluster-stop.sls
    │   ├── cluster-test.sls
    │   ├── cluster-up.sls
    │   ├── install
    │   │   ├── files
    │   │   │   ├── etc.cassandra.cassandra.yaml
    │   │   │   ├── etc.cassandra.cassandra.yaml.bak
    │   │   │   └── sedit.sh
    │   │   ├── raas-db-cassandra.sls
    │   │   ├── raas-db-sqlite.sls
    │   │   ├── raas-repo.sls
    │   │   ├── raas-salt-master.sls
    │   │   ├── raas-server.sls
    │   │   ├── salt-master.sls
    │   │   └── ubu-npm.sls
    │   └── xtras
    │       ├── firewall.sls
    │       ├── keys.sls
    │       └── users.sls
    ├── filetest_old.sls
    ├── filetest.sls
    ├── orchestrate
    │   └── raas.sls
    ├── repo
    │   └── ubu.tar
    ├── test
    │   └── filetest
    ├── top.sls
    └── xtras
        ├── firewall.sls
        ├── keys.sls
        └── users.sls
```
> Blockquotes are very handy in email to emulate reply text.
> This line is part of the same quote.

Quote break.

> This is a very long line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can *put* **Markdown** into a blockquote. 
