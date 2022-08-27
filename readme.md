# MP1 Design document
Yicheng Lu, Zhaoyang Wang

## How to use && Performance evaluation graphs
1,just use the shell script we provide to run the four scenarios. They are: scenarios1.sh,scenarios2.sh,scenarios3.sh,scenarios4.sh
2,The output of each node will store in out+"node #"+.txt
3,the stats data  will store under dic:stats(csv format)
4,The output data of four scenarios we ran before is  store under ./stats/scenarios1,./stats/scenario21,./stats/scenarios3,./stats/scenarios4
5,Performance evaluation graphs we created before are under the dic:Plots.

## General Protocol Design
we implement a modified ISIS algorithm with R-multicast. Here is a brief pseudo code to show how it works:
```
Node:
    if receieve a imcoming message:
        if message's(ID, priority,sender) has been before:
            ignore this message # R-multicast implementation
        else:
            multicast the message without changeing anything  # R-multicast implementation
            if message's ID has been so seen before: # incoming message contain proposal priority case 
                handle the message
            else: # node need to reply proposal priority case
                load proposal priority to message
                handle the message
                change message's sender
                multicast the message
    
    if itself get a message:
        handle the message
        multicast the message
Note: here handle may means fun: deliver and fun: deliver_queue_head
```
## Design ensures total ordering  
We use decentralized ISIS algorithm to  ensure ordering.
Meaning instead of unicast the reply to the sender, we multicast the proposal priority to every node in the group. In this case, every node seems to be a sender and have the info of all messages. And every node just need to update the priority queue and pop only if the poped message get all other nodes' replies.

Also, since we use R-multicast, we can ensure that even some nodes failes, all other nodes will have the same message priority eventually(ensures total ordering ). This is becasue with R-multicast, a message can only have two cases:
not know by all alive nodes or known by all alive nodes.

## Design ensures reliable delivery under failures
since we use R-multicast, we can ensure that even some nodes failes, all other nodes will have the same message priority eventually. This is becasue with R-multicast, a message can only have two cases:
not know by all alive nodes or known by all alive nodes. So that we handle the failures.

Also, as mentioned in document, we directly use TCP errors to detect failures. Once detected, node can pop its priority queue when all other alive nodes' replies.