import java.io.BufferedInputStream;
import java.net.Socket;
import java.util.Scanner;

public class ClientHandler extends Thread {

    Socket socket;
    String film;

    public ClientHandler(Socket socket){
        this.socket = socket;
    }

    @Override
    public void run(){
        try{
            BufferedInputStream bis = new BufferedInputStream(socket.getInputStream());
            Scanner in = new Scanner(bis);
            String message = in.nextLine();
            System.out.println(message);
        } catch (Exception a){
            System.err.println(a);
        }
    }

}
