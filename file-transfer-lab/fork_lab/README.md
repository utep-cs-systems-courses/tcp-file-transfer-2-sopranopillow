# Tcp file transfer
---

## Simple use

To use the file transfer demo, you first need to turn on the file server. If you have any questions about the arguments you can use, you can use the following command for help:

```
$ ./fileServer.py -? 
```

Otherwise we can start the server by simply entering the following command:

```
$ ./fileServer.py
```

Once the server is running, you can open another terminal and use the fileClient as follows:

```
$ ./fileClient.py put <input> <output>
```

If you have any questions about how to use the command you can type the following command:

```
$ ./fileClient.py -?
```

## Deeper use

If you want to use the proxy, you can add -p after the files so that it points to ```127.0.0.1:50000``` just as follows:

```
$ ./fileClient.py put <input> <output> -p
```

If you want to use a different listener port you can use the following command:

```
$ put <source> <output> -s <addess>:<port>
