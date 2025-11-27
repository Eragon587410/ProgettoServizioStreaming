import java.net.ServerSocket;
import java.net.Socket;

public class Server {

    ServerSocket sSocket;
    int port;

    public Server(int port){
        this.port = port;
    }

    public void start(){
        try{
            sSocket = new ServerSocket(port);
            while (true){
                Socket sk = sSocket.accept();
                ClientHandler handler = new ClientHandler(sk);
                handler.start();
            }
        } catch (Exception e){
            System.err.println(e);
        }
    }
    public static void main(String args[]){
        Server server = new Server(2160);
        server.start();
    }

}