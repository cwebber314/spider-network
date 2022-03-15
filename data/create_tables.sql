-- Code to create database tables
CREATE TABLE edge (
    edgeid INTEGER GENERATED ALWAYS AS IDENTITY,
    networkid int,
    edgename varchar(50),
    frombusnum varchar(12),
    tobusnum varchar(12),
    ckt varchar(2),
    PRIMARY KEY (edgeid),
    CONSTRAINT fk_edge_networkid 
        FOREIGN KEY (networkid) REFERENCES network(networkid)    
);


CREATE TABLE node (
    nodeid INTEGER GENERATED ALWAYS AS IDENTITY,
    networkid int,
    nodename varchar(50),
    kv float,
    busnum varchar(12),
    PRIMARY KEY (nodeid),
    CONSTRAINT fk_node_networkid 
        FOREIGN KEY (networkid) REFERENCES network(networkid)    
);

CREATE TABLE network (
    networkid INTEGER PRIMARY KEY,
    networkname varchar(50)
);

