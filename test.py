import subprocess as sp
#stdout=sp.PIPE,
def main():

    #server
    client_init = ["./chess_client", "127.0.0.1", "8080"]
    p = sp.Popen(client_init, stdin=sp.PIPE, stderr=sp.STDOUT)
    server_move = p.communicate(input="chessB\r")
    print "server move: ", server_move
    server_move = p.communicate()
    p.terminate()



    
main()

