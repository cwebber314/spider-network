-- This is a little fragile and doesn't play well with heroku
COPY network(networkid,networkname)
FROM '/home/cwebber/spider-network/data/network.csv'
DELIMITER ','
CSV HEADER;

COPY edge(networkid,edgename,frombusnum,tobusnum,ckt)
FROM '/home/cwebber/spider-network/data/edge_test.csv'
DELIMITER ','
CSV HEADER;

COPY node(networkid,nodename,kv,busnum)
FROM '/home/cwebber/spider-network/data/node_test.csv'
DELIMITER ','
CSV HEADER;